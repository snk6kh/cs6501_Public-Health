import pandas as pd
import pytz

df = pd.read_csv("Activities.csv")
df['Activity Timestamp'] = pd.to_datetime(df['Activity Timestamp'], utc=True)

#change to est
est = pytz.timezone("US/Eastern")
df['Activity Timestamp'] = df['Activity Timestamp'].dt.tz_convert(est)

#only gmail
filtered_df = df[df['Product Name'].str.contains("Gmail", case=False, na=False)]

# Filter times between 06:00 and 18:00 (6 AM - 6 PM)
filtered_df = filtered_df[(filtered_df['Activity Timestamp'].dt.hour >= 6) & (df['Activity Timestamp'].dt.hour < 18)]

# Extract date part only (without time) for grouping
filtered_df['Date'] = filtered_df['Activity Timestamp'].dt.date

# Find the first timestamp for each date
first_use_per_day = filtered_df.groupby('Date')['Activity Timestamp'].min().reset_index()

# Save to CSV
first_use_per_day.to_csv("gmail_wake.csv", index=False)
