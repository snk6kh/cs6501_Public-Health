import json
import pandas as pd
from datetime import datetime
from pathlib import Path


with open("json_data/yr_liked_posts.json", "r") as f:
    data = json.load(f)
records = []
for entry in data.get("likes_media_likes", []):
    username = entry["title"]
    for like in entry["string_list_data"]:
        timestamp = like["timestamp"]
        records.append({
            "username": username,
            "timestamp": timestamp
        })


df = pd.DataFrame(records)
df['Timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern')
df['date'] = df['Timestamp'].dt.date
df['time'] = df['Timestamp'].dt.time
df.to_csv("raw_likes_log.csv", index=False)

likes_per_day = df.groupby('date').size().reset_index(name='like_count')
likes_per_day.to_csv("yr_likes_per_day.csv", index=False)
