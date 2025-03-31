import pandas as pd
import ast  

def classify_location(row):
    categories = row['category']
    duration = row['duration']

    if duration > 37000:
        return 'home'
    for category_list in categories:
        if isinstance(category_list, str):
            category_list = ast.literal_eval(category_list)
        if 'library' in category_list:
            return 'library'
        elif 'meal_takeaway' in category_list and (duration > 7600 and duration < 8400):
            return 'gym'
        elif 'lodging' in category_list:
            return 'home'
        elif 'restaurant' in category_list and 'bus_station' in category_list:
            return 'school'
        elif 'real_estate_agency' in category_list:
            return 'friends'
        elif 'train_station' in category_list:
            return 'train'
        elif 'pharmacy' in category_list:
            return 'shopping'
        elif 'university' in category_list:
            return 'school'
        elif 'shopping_mall' in category_list:
            return 'shopping'
        elif 'restaurant' in category_list:
            if (duration > 4800 and duration < 5400):
                return 'school'
            return 'restaurant'
        elif 'gas_station' in category_list:
            return 'gas'
        elif 'bus_station' in category_list:
            return 'bus stop'
        elif 'grocery_or_supermarket' in category_list:
            return 'shopping'
    return 'friends'

df = pd.read_csv('location_assigned_data.csv')

df['category'] = df['category'].apply(ast.literal_eval)
df['location_type'] = df.apply(classify_location, axis=1)

df.to_csv('classified_locations.csv', index=False)
print(df[['latitude', 'longitude', 'category', 'location_type']])
aggregated_df = df.groupby('cluster').agg(
    latitude=('latitude', 'mean'),
    longitude=('longitude', 'mean'),
    duration=('duration', 'sum'),
    location_type=('location_type', lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
).reset_index()
aggregated_df.to_csv("comb_clusters.csv", index=False)
