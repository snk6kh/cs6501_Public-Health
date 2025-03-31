import json
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import ast
import requests

def load_location_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    locations = []

    for entry in data:
        if 'visit' in entry:
            lat, lon = map(float, entry['visit']['topCandidate']['placeLocation'].split(':')[-1].split(','))
            start_time = entry['startTime']
            end_time = entry['endTime']
            if(lat > 37.5 and lat < 38.5):
                duration = pd.to_datetime(end_time) - pd.to_datetime(start_time)
                locations.append([lat, lon, duration.total_seconds(),start_time,end_time])
    
    return pd.DataFrame(locations, columns=['latitude', 'longitude', 'duration','start','end'])

def cluster_locations(df, eps=0.00001, min_samples=1):
    coords = df[['latitude', 'longitude']].values
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean').fit(np.radians(coords))
    df['cluster'] = clustering.labels_
    return df

def get_place_category(lat, lon, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=50&key={api_key}"
    response = requests.get(url).json()
    if 'results' in response and response['results']:
        types = [result.get("types", []) for result in response["results"]]
        return types
    return 'Unknown'

def main():
    filename = 'location-history.json'
    api_key = '<ommited key from public repo>' 
    df = load_location_data(filename)
    df = cluster_locations(df)
    df['cluster'] = df['cluster'].replace({6: 2})
    df['category'] = df.apply(lambda row: get_place_category(row['latitude'], row['longitude'], api_key), axis=1)
    df.to_csv('location_assigned_data.csv',index=False, encoding='utf-8')

if __name__ == "__main__":
    main()
