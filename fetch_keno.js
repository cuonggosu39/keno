const fs = require("fs");
const axios = require("axios");

const MAX_KY = 50; // giữ tối đa 50 kỳ
const DATA_PATH = "data/keno.json";
const SOURCE_URL = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/master/data/keno.json";

async function main() {
  try {
    const res = await axios.get(SOURCE_URL);
    const allResults = res.data;

    if (!Array.isArray(allResults) || allResults.length === 0) {
      console.log("⚠️ Không lấy được dữ liệu từ vietvudanh JSON");
      return;
    }

    // Giữ tối đa MAX_KY kỳ
    const combined = allResults.slice(0, MAX_KY);

    // Tạo folder nếu chưa có
    if (!fs.existsSync("data")) fs.mkdirSync("data");

    // Ghi file JSON
    fs.writeFileSync(DATA_PATH, JSON.stringify(combined, null, 2));

    console.log("✅ Keno data updated from vietvudanh! Kỳ mới nhất:", combined[0]?.ky);
  } catch (e) {
    console.error("❌ Error fetching Keno JSON:", e.message);
  }
}

main();
