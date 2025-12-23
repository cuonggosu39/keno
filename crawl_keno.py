import requests
from bs4 import BeautifulSoup
import json

URL = "https://xosodaiphat.com/keno-truc-tiep-xskeno.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=HEADERS, timeout=15).text
soup = BeautifulSoup(html, "html.parser")

results = []

# mỗi block kỳ Keno
for block in soup.select(".kqxskeno-item")[:50]:
    try:
        # kỳ
        draw = block.select_one(".keno-ky").get_text(strip=True)

        # ngày
        date = block.select_one(".keno-ngay").get_text(strip=True)

        # 20 số
        nums = []
        for n in block.select(".keno-ball span"):
            nums.append(int(n.get_text()))

        if len(nums) == 20:
            results.append({
                "draw": draw if draw.startswith("#") else f"#{draw}",
                "date": date,
                "nums": nums
            })
    except Exception as e:
        continue

# sort kỳ mới → cũ
results = results[::-1]

with open("keno.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Saved {len(results)} Keno results")
