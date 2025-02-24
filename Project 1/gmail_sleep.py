import pandas as pd
import pytz

df = pd.read_csv("Activities.csv")
df['Activity Timestamp'] = pd.to_datetime(df['Activity Timestamp'], utc=True)

#change to est
est = pytz.timezone("US/Eastern")
df['Activity Timestamp'] = df['Activity Timestamp'].dt.tz_convert(est)

#only gmail
filtered_df = df[df['Product Name'].str.contains("Gmail", case=False, na=False)]

# Filter times between 00:00 and 06:00
filtered_df = filtered_df[(filtered_df['Activity Timestamp'].dt.hour >= 0) & (filtered_df['Activity Timestamp'].dt.hour < 5)]

filtered_df['Date'] = filtered_df['Activity Timestamp'].dt.date

# Find the latest timestamp for each date
latest_times_per_day = filtered_df.groupby('Date')['Activity Timestamp'].max().reset_index()

latest_times_per_day.to_csv("gmail_sleep.csv", index=False)

print("Saved latest timestamps per day to 'latest_times_per_day.csv'")
