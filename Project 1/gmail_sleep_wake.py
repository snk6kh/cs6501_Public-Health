import pandas as pd
import pytz

df = pd.read_csv("Activities.csv")  
df['Activity Timestamp'] = pd.to_datetime(df['Activity Timestamp'], utc=True)

#change to est
est = pytz.timezone("US/Eastern")
df['Activity Timestamp'] = df['Activity Timestamp'].dt.tz_convert(est)

df['Date'] = df['Activity Timestamp'].dt.date

#only gmail
df_filtered = df[df['Product Name'].str.contains("Gmail", case=False, na=False)]

# Group by 'Gaia ID' and 'Date', then find first and last timestamps
summary = df_filtered.groupby(['Gaia ID', 'Date']).agg(
    first_use=('Activity Timestamp', 'min'),
    last_use=('Activity Timestamp', 'max')
).reset_index()

output_file = "gmail_first_last_use.csv"
summary.to_csv(output_file, index=False)
