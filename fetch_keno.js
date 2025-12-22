const fs = require("fs");
const axios = require("axios");
const cheerio = require("cheerio");

const MAX_KY = 50;

async function main() {
  try {
    const url = "https://www.minhchinh.com/truc-tiep-xo-so-tu-chon-keno.html";
    const res = await axios.get(url);
    const $ = cheerio.load(res.data);

    let newResults = [];

    $(".board-item").each((i, el) => {
      const ky = $(el).find(".draw-number").text().trim();
      const time = $(el).find(".draw-time").text().trim();
      const numbers = [];
      $(el).find(".board-number span").each((j, num) => {
        numbers.push(parseInt($(num).text().trim()));
      });
      newResults.push({ ky, time, numbers });
    });

    // load dữ liệu cũ
    let oldResults = [];
    if (fs.existsSync("data/keno.json")) {
      oldResults = JSON.parse(fs.readFileSync("data/keno.json"));
    }

    // kết hợp + loại trùng
    const combined = [...newResults, ...oldResults].filter(
      (v, i, a) => a.findIndex(x => x.ky === v.ky) === i
    );

    // giữ tối đa MAX_KY
    combined.splice(MAX_KY);

    // ghi JSON
    if (!fs.existsSync("data")) fs.mkdirSync("data");
    fs.writeFileSync("data/keno.json", JSON.stringify(combined, null, 2));

    console.log("✅ Keno data updated! Kỳ mới nhất:", combined[0]?.ky);
  } catch (e) {
    console.error("❌ Error fetching Keno:", e.message);
  }
}

main();
