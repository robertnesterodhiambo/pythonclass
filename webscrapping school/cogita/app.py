import requests
import time
import csv
import random
from requests.exceptions import RequestException

# Base URL and credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Authentication function
def authenticate():
    print("🔐 Logging in...")
    auth_response = requests.post(
        f"{QOGITA_API_URL}/auth/login/",
        json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
    )
    if auth_response.status_code == 200:
        data = auth_response.json()
        token = data["accessToken"]
        cart = data["user"]["activeCartQid"]
        print("✅ Login successful.\n")
        return token, cart
    else:
        print(f"❌ Login failed: {auth_response.status_code} - {auth_response.text}")
        exit()

# Retry wrapper for GET requests
def make_request_with_retries(url, headers, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 401:
                return "unauthorized"
            response.raise_for_status()
            return response
        except RequestException as e:
            wait_time = (10 ** attempt) + random.uniform(0, 1)
            print(f"⚠️ Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            print(f"⏳ Retrying in {wait_time:.2f} seconds...\n")
            time.sleep(wait_time)
    print("❌ Max retries reached. Skipping this request.\n")
    return None

# Step 0: Load previously collected GTINs
collected_gtins = set()
try:
    with open("/home/dragon/DATA/products.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            collected_gtins.add(row["gtin"])
    print(f"✅ Loaded {len(collected_gtins)} existing GTINs.\n")
except FileNotFoundError:
    print("ℹ️ No existing CSV found. A new one will be created.\n")

# Step 1: Initial authentication
access_token, cart_qid = authenticate()
headers = {"Authorization": f"Bearer {access_token}"}

print(f"Active Cart QID: {cart_qid}\n")

# Open CSV in append mode
with open("/home/dragon/DATA/products.csv", mode="a", newline='', encoding="utf-8") as file:
    fieldnames = ["gtin", "name", "categoryName", "brandName", "price", "inventory", "imageUrl"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if len(collected_gtins) == 0:
        writer.writeheader()

    page = 1
    size = 500000
    total_count = 0

    while True:
        print(f"Fetching page {page}...")
        search_url = f"{QOGITA_API_URL}/variants/search/?page={page}&size={size}"

        response_raw = make_request_with_retries(search_url, headers)
        
        # Re-authenticate if token expired
        if response_raw == "unauthorized":
            print("🔁 Token expired. Re-authenticating...\n")
            access_token, cart_qid = authenticate()
            headers = {"Authorization": f"Bearer {access_token}"}
            response_raw = make_request_with_retries(search_url, headers)

        if response_raw is None or not response_raw.ok:
            print(f"❌ Failed to fetch page {page}. Moving to next.")
            break

        response = response_raw.json()
        results = response.get("results", [])

        if not results:
            print("✅ No more results. Finished.\n")
            break

        for variant in results:
            gtin = variant.get('gtin', '')
            if gtin in collected_gtins:
                continue

            writer.writerow({
                "gtin": gtin,
                "name": variant.get('name', ''),
                "categoryName": variant.get('categoryName', ''),
                "brandName": variant.get('brandName', ''),
                "price": variant.get('price', ''),
                "inventory": variant.get('inventory', ''),
                "imageUrl": variant.get('imageUrl', '')
            })

            print(f"Saved: {gtin} | {variant.get('name')}")

            collected_gtins.add(gtin)
            total_count += 1

        page += 1
        time.sleep(0.5)

    print(f"\n✅ Total new products retrieved: {total_count}")
