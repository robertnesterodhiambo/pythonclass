import requests
import time
import csv
import random
from requests.exceptions import RequestException

# === Configuration ===
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"
CSV_PATH = "/home/dragon/DATA/products2.csv"
GTIN_TO_ADD = "3349668614608"

# === Authentication Function ===
def authenticate():
    print("🔐 Logging in...")
    response = requests.post(
        f"{QOGITA_API_URL}/auth/login/",
        json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
    )
    if response.status_code == 200:
        data = response.json()
        token = data["accessToken"]
        cart = data["user"]["activeCartQid"]
        print("✅ Login successful.")
        return token, cart
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        exit()

# === Add Product to Cart ===
def add_to_cart(gtin, cart_qid, headers):
    print(f"🛒 Adding GTIN {gtin} to cart...")
    url = f"{QOGITA_API_URL}/cart/add-product/"
    payload = {"cartQid": cart_qid, "gtin": gtin}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"✅ GTIN {gtin} added to cart.\n")
    else:
        print(f"❌ Failed to add GTIN {gtin}: {response.status_code} - {response.text}\n")

# === Resilient GET Request ===
def get_with_retries(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 401:
                return "unauthorized"
            return response
        except RequestException as e:
            wait = (2 ** attempt) + random.random()
            print(f"⚠️ Error: {e} - retrying in {wait:.2f} sec...")
            time.sleep(wait)
    return None

# === Load Previously Collected GTINs ===
collected_gtins = set()
try:
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            collected_gtins.add(row["gtin"])
    print(f"✅ Loaded {len(collected_gtins)} existing products.\n")
except FileNotFoundError:
    print("ℹ️ No existing file found. A new CSV will be created.\n")

# === Start Scraping ===
access_token, cart_qid = authenticate()
headers = {"Authorization": f"Bearer {access_token}"}

# Add specific GTIN to cart once after login
add_to_cart(GTIN_TO_ADD, cart_qid, headers)

with open(CSV_PATH, mode="a", newline='', encoding="utf-8") as file:
    fieldnames = ["gtin", "name", "categoryName", "brandName", "price", "inventory", "imageUrl"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if len(collected_gtins) == 0:
        writer.writeheader()

    page = 1
    size = 500000
    total_saved = 0

    while True:
        print(f"📄 Fetching page {page}...")
        url = f"{QOGITA_API_URL}/variants/search/?page={page}&size={size}"

        response = get_with_retries(url, headers)
        if response == "unauthorized":
            print("🔁 Token expired. Re-authenticating...\n")
            access_token, cart_qid = authenticate()
            headers = {"Authorization": f"Bearer {access_token}"}
            response = get_with_retries(url, headers)

        if response is None:
            print("❌ Skipping due to repeated errors.\n")
            break

        if response.text.startswith("<"):
            print("⚠️ Detected HTML response (likely Cloudflare). Retrying...\n")
            time.sleep(2)
            continue

        try:
            data = response.json()
        except Exception as e:
            print(f"❌ Failed to parse JSON: {e}")
            break

        results = data.get("results", [])
        if not results:
            print("✅ No more results. Done.\n")
            break

        print(f"🔍 Found {len(results)} products.")
        if len(results) < 5:
            print("⚠️ Less than 5 results. Assuming end of data.")
            break

        for product in results:
            gtin = product.get("gtin", "")
            if gtin in collected_gtins:
                continue

            writer.writerow({
                "gtin": gtin,
                "name": product.get("name", ""),
                "categoryName": product.get("categoryName", ""),
                "brandName": product.get("brandName", ""),
                "price": product.get("price", ""),
                "inventory": product.get("inventory", ""),
                "imageUrl": product.get("imageUrl", "")
            })

            print(f"💾 Saved GTIN: {gtin} - {product.get('name', '')}")
            collected_gtins.add(gtin)
            total_saved += 1

        page += 1
        time.sleep(1)

    print(f"\n✅ Total new products saved: {total_saved}")
