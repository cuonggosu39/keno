import os
import json
from datetime import datetime

print("TEST: crawl_keno.py is running")

os.makedirs("data", exist_ok=True)

data = {
    "status": "ok",
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open("data/keno.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("TEST: data/keno.json created")
