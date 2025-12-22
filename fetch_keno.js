const fs = require("fs");
const axios = require("axios");
const cheerio = require("cheerio");

const MAX_KY = 50; // giữ tối đa 50 kỳ

async function main() {
  try {
    const url = "https://www.minhchinh.com/truc-tiep-xo-so-tu-chon-keno.html";
    const res = await axios.get(url);
    const $ = cheerio.load(res.data);

    let newResults = [];

    // Lấy tất cả các kỳ Keno trên trang
    $(".board-game").each((i, el) => {
      const ky = $(el).find(".draw-number").text().trim();
      const time = $(el).find(".draw-time").text().trim();
      const numbers = [];

      $(el).find(".board-number span").each((j, num) => {
        const n = parseInt($(num).text().trim());
        if (!isNaN(n)) numbers.push(n);
      });

      if (ky && numbers.length) {
        newResults.push({ ky, time, numbers });
      }
    });

    if (newResults.length === 0) {
      console.log("⚠️ Không lấy được dữ liệu mới từ trang minhchinh.com");
      return;
    }

    // Load dữ liệu cũ
    let oldResults = [];
    const dataPath = "data/keno.json";
    if (fs.existsSync(dataPath)) {
      oldResults = JSON.parse(fs.readFileSync(dataPath));
    }

    // Kết hợp + loại trùng
    const combined = [...newResults, ...oldResults].filter(
      (v, i, a) => a.findIndex(x => x.ky === v.ky) === i
    );

    // Giữ tối đa MAX_KY kỳ
    combined.splice(MAX_KY);

    // Tạo folder nếu chưa có
    if (!fs.existsSync("data")) fs.mkdirSync("data");

    // Ghi file JSON
    fs.writeFileSync(dataPath, JSON.stringify(combined, null, 2));

    console.log("✅ Keno data updated! Kỳ mới nhất:", combined[0]?.ky);
  } catch (e) {
    console.error("❌ Error fetching Keno:", e.message);
  }
}

main();
