import requests
import csv
import time
import os
import random
import pandas as pd

# Credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Session variables
access_token = None
headers = {}
cart_qid = None

# Prepare CSV File
csv_path = '/home/dragon/DATA/variants_sellers.csv'
csv_file = open(csv_path, mode='a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# Check if CSV has headers, if not write headers
if os.stat(csv_path).st_size == 0:
    csv_writer.writerow([
        'GTIN', 'Variant Name', 'Category Name', 'Brand Name', 'Price (€)', 'Inventory', 'Image URL',
        'Seller', 'MOV (€)', 'Available Qty', 'Ordering Qty', 'Total Price (€)', 'Unit', 'Sellers Returned'
    ])

# Read existing GTINs from the CSV to avoid duplicates
def get_existing_gtins():
    existing_gtins = set()
    if os.path.exists(csv_path) and os.stat(csv_path).st_size > 0:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # skip header
            for row in csv_reader:
                existing_gtins.add(row[0])
    return existing_gtins

existing_gtins = get_existing_gtins()

def login():
    """Login to the API and set the access token and headers."""
    global access_token, headers, cart_qid
    print("🔐 Logging in...")
    try:
        auth_response = requests.post(
            f"{QOGITA_API_URL}/auth/login/",
            json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
        )
        if not auth_response.ok or 'application/json' not in auth_response.headers.get('Content-Type', ''):
            print("❌ Login failed (possibly blocked):", auth_response.text)
            return False

        auth_data = auth_response.json()
        access_token = auth_data.get("accessToken")
        if not access_token:
            print("❌ Login failed: No token found")
            return False

        headers = {"Authorization": f"Bearer {access_token}"}
        cart_qid = auth_data["user"]["activeCartQid"]
        print("✅ Authenticated successfully.")
        print(f"🛒 Active Cart QID: {cart_qid}")
        return True
    except Exception as e:
        print(f"❌ Login exception: {e}")
        return False

def safe_request(method, url, retry=1, **kwargs):
    """Wrapper to handle 401 and non-JSON responses with retry mechanism."""
    global headers
    try:
        response = requests.request(method, url, headers=headers, **kwargs)

        # Check if it's a valid JSON
        if 'application/json' not in response.headers.get('Content-Type', ''):
            raise ValueError("Response not JSON")

        if response.status_code == 401 and retry > 0:
            print("🔁 Token expired or unauthorized. Re-authenticating...")
            if login():
                return safe_request(method, url, retry=retry-1, **kwargs)
            else:
                return None

        response.raise_for_status()
        return response
    except ValueError:
        print(f"⚠️ Non-JSON response received from {url}. Possibly blocked by Cloudflare.")
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error: {http_err} | Response: {http_err.response.text}")
    except requests.exceptions.RequestException as err:
        print(f"❌ Request failed: {err}")
    return None

def get_variant_by_gtin(gtin):
    response = safe_request("GET", f"{QOGITA_API_URL}/variants/{gtin}/")
    return response.json() if response and response.ok else None

def get_offers(fid, slug):
    response = safe_request("GET", f"{QOGITA_API_URL}/variants/{fid}/{slug}/offers/")
    return response.json() if response and response.ok else None

def process_gtin(gtin):
    if gtin in existing_gtins:
        print(f"🔄 Skipping already processed GTIN: {gtin}")
        return

    variant = get_variant_by_gtin(gtin)
    if not variant:
        print(f"⚠️ Skipping GTIN {gtin}: Variant not found or error fetching.")
        return

    try:
        variant_name = variant.get("name", "")
        fid = variant.get("fid", "")
        slug = variant.get("slug", "")
        category_name = variant.get('categoryName', '')
        brand_name = variant.get('brandName', '')
        price = variant.get('price', '')
        inventory = variant.get('inventory', '')
        image_url = variant.get('imageUrl', '')

        offers_response = get_offers(fid, slug)
        offers = offers_response.get("offers", []) if offers_response else []

        print(f"📊 Sellers returned for {variant_name} (GTIN: {gtin}): {len(offers)}")

        if not offers:
            print(f"❌ No offers found for {variant_name}")
            return

        requested_quantity = 100
        valid_offers = [
            offer for offer in offers
            if requested_quantity * float(offer["price"]) >= float(offer["mov"])
        ]

        if not valid_offers:
            print(f"⚠️ No valid offers meet MOV requirement for {variant_name}")
            return

        for offer in valid_offers:
            offer_qid = offer["qid"]
            available_quantity = offer.get("availableQuantity", 0)
            quantity_to_order = min(requested_quantity, available_quantity)
            total_price = float(offer["price"]) * quantity_to_order

            csv_writer.writerow([
                gtin, variant_name, category_name, brand_name, price, inventory, image_url,
                offer['seller'], offer['mov'], available_quantity, quantity_to_order,
                f"{total_price:.2f}", offer["unit"], len(offers)
            ])
            csv_file.flush()

            print(f"📦 Selected Offer:")
            print(f"    Seller: {offer['seller']} | Qty: {quantity_to_order} | Total: €{total_price:.2f}")

            cart_response = safe_request(
                "POST",
                f"{QOGITA_API_URL}/carts/{cart_qid}/lines/",
                json={"offerQid": offer_qid, "quantity": quantity_to_order}
            )

            if cart_response and cart_response.ok:
                print(f"✅ Added to cart.\n")
            else:
                error = cart_response.json() if cart_response else "No response"
                print(f"❌ Add to cart failed: {error}")

        existing_gtins.add(gtin)
        sleep_duration = random.uniform(2, 5)
        print(f"⏳ Sleeping {sleep_duration:.2f} seconds...\n")
        time.sleep(sleep_duration)

    except Exception as e:
        print(f"❌ Exception while processing {gtin}: {e}")

# Initial login
if not login():
    print("❌ Cannot proceed without login.")
    exit()

# Example GTINs
#gtins_to_process = ["3349668614608", "0987654321", "1122334455"]  # Replace as needed
# Replace '~/DATA' with the full path or expand the '~' to your home directory
file_path = '~/DATA/variants.csv'
df = pd.read_csv(file_path)
# Extract the GTIN column and drop missing values
gtins_to_process = df['GTIN'].dropna().astype(str).unique().tolist()
# Read the CSV file
print(gtins_to_process)
print(df.head())

for gtin in gtins_to_process:
    process_gtin(gtin)

csv_file.close()
print("💾 Data saved to variants_sellers.csv")
