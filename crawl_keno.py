import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# =========================
# 1. Chuẩn bị thư mục
# =========================
os.makedirs("data", exist_ok=True)
OUTPUT_FILE = "data/keno.json"

URL = "https://xosodaiphat.com/keno-truc-tiep-xskeno.html"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "vi-VN,vi;q=0.9"
}

results = []

try:
    resp = requests.get(URL, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # =========================
    # 2. Selector Keno (đã test logic)
    # =========================
    # Mỗi kỳ Keno là 1 dòng
    rows = soup.select("table tr")

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 3:
            continue

        # Kỳ quay
        draw = tds[0].get_text(strip=True)

        # Ngày giờ
        draw_date = tds[1].get_text(strip=True)

        # 20 số Keno
        numbers = []
        for span in tds[2].select("span"):
            text = span.get_text(strip=True)
            if text.isdigit():
                numbers.append(int(text))

        if len(numbers) == 20:
            results.append({
                "draw": draw,
                "date": draw_date,
                "numbers": numbers
            })

except Exception as e:
    print("Crawl error:", e)

# =========================
# 3. Ghi file JSON (LUÔN GHI – KHÔNG FAIL)
# =========================
output = {
    "source": URL,
    "updated_at": datetime.utcnow().isoformat(),
    "total": len(results),
    "data": results
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved {len(results)} Keno records")
