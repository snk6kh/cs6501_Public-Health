import pandas as pd
import pytz

df = pd.read_csv("Activities.csv")  
df['Activity Timestamp'] = pd.to_datetime(df['Activity Timestamp'], utc=True)

#change to est
est = pytz.timezone("US/Eastern") # from ChatGPT
df['Activity Timestamp'] = df['Activity Timestamp'].dt.tz_convert(est)

# Extract date only
df['Date'] = df['Activity Timestamp'].dt.date

#avoid sheets data
df_filtered = df[~df['User Agent String'].str.startswith("App : SHEETS_APP", na=False)]

# Group by 'Gaia ID' and 'Date', then find first and last timestamps
summary = df_filtered.groupby(['Gaia ID', 'Date']).agg(
    first_use=('Activity Timestamp', 'min'),
    last_use=('Activity Timestamp', 'max')
).reset_index()


output_file = "general_first_last_use.csv"
summary.to_csv(output_file, index=False)

