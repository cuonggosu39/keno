const fs = require("fs");
const axios = require("axios");
const cheerio = require("cheerio");

const DATA_PATH = "data/keno.json";
const SOURCE_URL = "https://xoso.com.vn/ket-qua-xs-keno.html";
const MAX_KY = 20; // 20 kỳ gần nhất

async function main() {
  try {
    const res = await axios.get(SOURCE_URL);
    const $ = cheerio.load(res.data);

    const results = [];

    $(".result-table tbody tr").each((i, el) => {
      if (i >= MAX_KY) return false;

      const ky = $(el).find("td:nth-child(1)").text().trim();
      const date = $(el).find("td:nth-child(2)").text().trim();
      const numbersText = $(el).find("td:nth-child(3)").text().trim();
      const numbers = numbersText.split(" ").map(n => parseInt(n)).filter(n => !isNaN(n));

      if (ky && numbers.length === 20) {
        results.push({ ky, date, numbers });
      }
    });

    if (!fs.existsSync("data")) fs.mkdirSync("data");
    fs.writeFileSync(DATA_PATH, JSON.stringify(results, null, 2));

    console.log("✅ Keno data updated! Lấy được", results.length, "kỳ gần nhất.");
  } catch (err) {
    console.error("❌ Lỗi khi fetch Keno:", err.message);
  }
}

main();
