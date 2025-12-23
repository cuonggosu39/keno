import os
import json
from datetime import datetime

# ======================
# BẮT BUỘC TẠO FILE TRƯỚC
# ======================
os.makedirs("data", exist_ok=True)
OUTPUT_FILE = "data/keno.json"

# GHI FILE RỖNG TRƯỚC (CHỐNG FAIL)
empty_output = {
    "source": "init",
    "updated_at": datetime.utcnow().isoformat(),
    "total": 0,
    "data": []
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(empty_output, f, ensure_ascii=False, indent=2)

print("Initialized empty keno.json")

# ======================
# PHẦN CRAWL (CÓ THÌ GHI ĐÈ)
# ======================
try:
    import requests

    URL = "https://appapi.xosodaiphat.com/api/Vietlott/GetKenoResult"
    resp = requests.get(URL, timeout=15)
    resp.raise_for_status()
    raw = resp.json()

    results = []

    for item in raw:
        nums = []
        for i in range(1, 21):
            n = item.get(f"Num{i}")
            if n is not None:
                nums.append(int(n))

        if len(nums) == 20:
            results.append({
                "draw": item.get("DrawCode"),
                "date": item.get("DrawDate"),
                "numbers": nums
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

except Exception as e:
    print("Crawl failed, keep empty file:", e)
