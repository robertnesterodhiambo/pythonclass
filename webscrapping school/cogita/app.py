import requests
import time
import csv

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

# Step 0: Load previously collected GTINs
collected_gtins = set()
try:
    with open("products.csv", mode="r", encoding="utf-8") as f:
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
with open("products.csv", mode="a", newline='', encoding="utf-8") as file:
    # Define CSV writer
    fieldnames = ["gtin", "name", "categoryName", "brandName", "price", "inventory", "imageUrl"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write header only if file is new
    if len(collected_gtins) == 0:
        writer.writeheader()

    # Step 2: Paginate through all results
    page = 1
    size = 500000  # Keep your size as-is
    total_count = 0

    while True:
        print(f"Fetching page {page}...")

        search_url = (
            f"{QOGITA_API_URL}/variants/search/?"
            f"page={page}&size={size}"
        )

        response_raw = requests.get(url=search_url, headers=headers)

        # Handle token expiration (401)
        if response_raw.status_code == 401:
            print("🔁 Token expired. Re-authenticating...")
            access_token, cart_qid = authenticate()
            headers = {"Authorization": f"Bearer {access_token}"}
            response_raw = requests.get(url=search_url, headers=headers)

        if response_raw.status_code != 200:
            print(f"❌ Error fetching page {page}: {response_raw.status_code} - {response_raw.text}")
            break

        response = response_raw.json()
        results = response.get("results", [])

        if not results:
            print("No more results. Done.")
            break

        for variant in results:
            gtin = variant.get('gtin', '')
            if gtin in collected_gtins:
                continue  # Skip duplicates

            # Write each new result to the CSV file
            writer.writerow({
                "gtin": gtin,
                "name": variant.get('name', ''),
                "categoryName": variant.get('categoryName', ''),
                "brandName": variant.get('brandName', ''),
                "price": variant.get('price', ''),
                "inventory": variant.get('inventory', ''),
                "imageUrl": variant.get('imageUrl', '')
            })

            print(f"Saved: {gtin} | {variant['name']} | {variant['categoryName']} | "
                  f"{variant['brandName']} | {variant['price']} | {variant['inventory']} | {variant['imageUrl']}")

            collected_gtins.add(gtin)
            total_count += 1

        page += 1
        time.sleep(0.5)  # Sleep to avoid rate limits

    print(f"\n✅ Total new products retrieved: {total_count}")
