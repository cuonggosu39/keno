import requests
import json
import os
from datetime import datetime

URL = "https://appapi.xosodaiphat.com/api/Vietlott/GetHomeData"

def main():
    print("Fetching Keno data...")

    res = requests.get(URL, timeout=15)
    res.raise_for_status()

    data = res.json()

    # Tạo thư mục data nếu chưa có
    os.makedirs("data", exist_ok=True)

    output = {
        "source": URL,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "raw": data
    }

    with open("data/keno.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("Saved data/keno.json successfully")

if __name__ == "__main__":
    main()
