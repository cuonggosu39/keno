import requests
import json
import os

DATA_FILE = "data/keno.json"
URL = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/keno.json"

def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def fetch_latest_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return []

def merge_data(existing, new_data):
    existing_ids = set(d['draw'] for d in existing)
    merged = existing[:]
    for item in new_data:
        if item['draw'] not in existing_ids:
            merged.append(item)
    merged.sort(key=lambda x: x['draw'], reverse=True)
    return merged

existing_data = load_existing_data()
new_data = fetch_latest_data()
merged_data = merge_data(existing_data, new_data)

if merged_data != existing_data:
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    print(f"Updated Keno data. Total {len(merged_data)} records.")
else:
    print("No new data to update.")
