import json
import pandas as pd
from collections import Counter
from datetime import datetime
import pytz

def utc_to_et_date(utc_str):
    utc_dt = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S %Z")
    utc_dt = pytz.utc.localize(utc_dt)
    et_dt = utc_dt.astimezone(pytz.timezone("US/Eastern"))
    return et_dt.date()

# Memories
with open("json_data/memories_history.json",encoding="utf-8") as f:
    memories_data = json.load(f)["Saved Media"]

memory_dates = [utc_to_et_date(item["Date"]) for item in memories_data]
memories_df = pd.DataFrame(Counter(memory_dates).items(), columns=["Date", "Memories_Count"])

# Snaps Data
with open("json_data/snap_history.json",encoding="utf-8") as f:
    snap_data = json.load(f)

snap_dates = []
for friend, snaps in snap_data.items():
    for s in snaps:
        if s.get("IsSender") and "Created" in s:
            try:
                date = utc_to_et_date(s["Created"])
                snap_dates.append(date)
            except:
                continue

snaps_df = pd.DataFrame(Counter(snap_dates).items(), columns=["Date", "Snaps_Sent_Count"])

# Chat Data
with open("json_data/chat_history.json",encoding="utf-8") as f:
    chat_data = json.load(f)

chat_dates = []
for friend, chats in chat_data.items():
    for c in chats:
        if c.get("IsSender") and "Created" in c:
            try:
                date = utc_to_et_date(c["Created"])
                chat_dates.append(date)
            except:
                continue

chats_df = pd.DataFrame(Counter(chat_dates).items(), columns=["Date", "Chats_Sent_Count"])


combined_df = pd.DataFrame({"Date": pd.date_range(start="2024-10-01", end="2025-04-21")})
combined_df["Date"] = combined_df["Date"].dt.date

for df in [memories_df, snaps_df, chats_df]:
    combined_df = combined_df.merge(df, on="Date", how="left")

combined_df.fillna(0, inplace=True)

combined_df[["Memories_Count", "Snaps_Sent_Count", "Chats_Sent_Count"]] = \
    combined_df[["Memories_Count", "Snaps_Sent_Count", "Chats_Sent_Count"]].astype(int)
combined_df.to_csv("FullSnapchatActivityTimeline.csv", index=False)
