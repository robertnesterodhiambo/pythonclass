const puppeteer = require('puppeteer');
const fs = require('fs');
const csvParser = require('csv-parser');
const { parse } = require('json2csv');

const inputCsv = '100 Country list 20180621.csv';
const csvPath = '/home/dragon/DATA/fishisfast.csv';
const ll_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250];

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--window-size=1920,1080'
    ]
  });

  const page = await browser.newPage();
  let existingKeys = new Set();
  let tasks = [];

  // Load existing entries
  if (fs.existsSync(csvPath)) {
    const existingRows = fs.readFileSync(csvPath, 'utf-8').split('\n').slice(1);
    for (const row of existingRows) {
      const cols = row.split(',');
      if (cols.length >= 4) {
        existingKeys.add(`${cols[0]}|${cols[1]}|${cols[2]}|${cols[3]}`);
      }
    }
    console.log(`✅ Loaded ${existingKeys.size} previous entries.`);
  } else {
    fs.writeFileSync(csvPath, 'country,city,zipcode,weight,service_name,delivery_days,price\n');
    console.log("📄 Created new CSV.");
  }

  // Load input CSV
  const rows = [];
  fs.createReadStream(inputCsv)
    .pipe(csvParser())
    .on('data', (data) => rows.push(data))
    .on('end', async () => {
      for (const row of rows) {
        const country = row.countryname;
        const city = row.city || '';
        const zipcode = row.zipcode || '';
        for (const weight of ll_lbs) {
          const key = `${country}|${city}|${zipcode}|${weight}`;
          if (!existingKeys.has(key)) {
            tasks.push({ country, city, zipcode, weight });
          }
        }
      }

      console.log(`🚀 ${tasks.length} new combinations to scrape.`);

      let lastLocation = {};

      async function initializePage() {
        await page.goto("https://www.stackry.com/shipping-calculator", { waitUntil: 'domcontentloaded' });
        const iframeElement = await page.waitForSelector('#myIframe');
        const frame = await iframeElement.contentFrame();
        await frame.waitForSelector("label[for='boxes.[0].weightUnit-lb']");
        await frame.click("label[for='boxes.[0].weightUnit-lb']");
        return frame;
      }

      function sleep(ms) {
        return new Promise(res => setTimeout(res, ms));
      }

      const frame = await initializePage();

      for (let i = 0; i < tasks.length; i++) {
        const { country, city, zipcode, weight } = tasks[i];

        if (i % 20 === 0 && i > 0) {
          console.log("⏳ Sleeping to avoid rate-limiting...");
          await sleep(15000);
        }

        try {
          if (
            lastLocation.country !== country ||
            lastLocation.city !== city ||
            lastLocation.zipcode !== zipcode
          ) {
            const countryInput = await frame.waitForSelector('#react-select-4-input');
            await countryInput.click({ clickCount: 3 });
            await countryInput.press('Backspace');
            for (let ch of country) {
              await countryInput.type(ch);
              await sleep(200);
            }
            await sleep(1000);
            await countryInput.press('ArrowDown');
            await sleep(500);
            await countryInput.press('Enter');
            console.log(`🌍 ${country} | City: ${city} | Zip: ${zipcode}`);

            try {
              const cityInput = await frame.waitForSelector('#shipToCity', { timeout: 3000 });
              await cityInput.click({ clickCount: 3 });
              await cityInput.press('Backspace');
              await cityInput.type(city);
              await sleep(500);
              console.log(`🏙️ Entered city: ${city}`);
            } catch {
              console.log("⚠️ City input missing.");
            }

            try {
              const zipInput = await frame.waitForSelector('#shipToZip', { timeout: 3000 });
              await zipInput.click({ clickCount: 3 });
              await zipInput.press('Backspace');
              await zipInput.type(zipcode);
              await sleep(500);
              console.log(`🏷️ Entered zip: ${zipcode}`);
            } catch {
              console.log("⚠️ Zipcode input missing.");
            }

            lastLocation = { country, city, zipcode };
          }

          const weightInput = await frame.waitForSelector('#weight');
          await weightInput.click({ clickCount: 3 });
          await weightInput.press('Backspace');
          await weightInput.type(weight.toString());
          await weightInput.press('Enter');
          console.log(`⚖️ ${weight} lbs`);

          await sleep(5000);

          const error = await frame.$("p.text-red-450.mt-2");
          if (error) {
            const errorText = await frame.evaluate(el => el.textContent, error);
            if (errorText.includes("Try again later")) {
              console.log("🔁 'Try again later' - refreshing and retrying...");
              await frame.goto("https://www.stackry.com/shipping-calculator", { waitUntil: 'domcontentloaded' });
              continue;
            }
          }

          const outerFrame = await page.mainFrame();
          const results = await outerFrame.$$("div[style*='justify-content: space-between; padding: 0.75rem;']");
          if (!results.length) {
            console.log("⚠️ No shipping results found.");
          }

          for (const res of results) {
            try {
              const serviceName = await res.$eval("p[style*='font-size']", el => el.textContent.trim());
              const deliveryDays = await res.$eval("span[style*='text-align: end']", el => el.textContent.trim());
              const price = await res.$eval("strong[style*='font-weight']", el => el.textContent.trim());

              console.log(`💸 ${serviceName} | ${deliveryDays} | ${price}`);

              const entry = {
                country,
                city,
                zipcode,
                weight,
                service_name: serviceName,
                delivery_days: deliveryDays,
                price
              };

              fs.appendFileSync(csvPath, `${country},${city},${zipcode},${weight},${serviceName},${deliveryDays},${price}\n`);
            } catch (e) {
              console.log(`⚠️ Error parsing result: ${e}`);
            }
          }

        } catch (err) {
          console.log(`❌ Error for ${country}, ${city}, ${zipcode}, ${weight} lbs: ${err}`);
        }
      }

      await browser.close();
      console.log("✅ Scraping complete.");
    });
})();
