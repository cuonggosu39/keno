import requests
import json

# URL raw JSON từ repo vietlott-data
url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/keno.json"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    with open("data/keno.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Fetched {len(data)} Keno records")
else:
    print("Failed to fetch data, status code:", response.status_code)
