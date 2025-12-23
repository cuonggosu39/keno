import requests
import json
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)
OUTPUT_FILE = "data/keno.json"

URL = "https://appapi.xosodaiphat.com/api/Vietlott/GetKenoResult"

try:
    resp = requests.get(URL, timeout=20)
    resp.raise_for_status()
    raw = resp.json()
except Exception as e:
    print("Fetch API error:", e)
    raw = []

results = []

for item in raw:
    numbers = []
    for i in range(1, 21):
        n = item.get(f"Num{i}")
        if n is not None:
            numbers.append(int(n))

    if len(numbers) == 20:
        results.append({
            "draw": item.get("DrawCode"),
            "date": item.get("DrawDate"),
            "numbers": numbers
        })

output = {
    "source": URL,
    "updated_at": datetime.utcnow().isoformat(),
    "total": len(results),
    "data": results
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Saved", len(results), "Keno records")
