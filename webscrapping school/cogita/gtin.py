import requests
import csv
import time
import os
import random
import pandas as pd
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Session variables
access_token = None
headers = {}
cart_qid = None

# CSV path
csv_path = '/home/dragon/DATA/variants_sellers.csv'
csv_lock = threading.Lock()
gtin_lock = threading.Lock()

# Ensure CSV file and write headers if missing
if not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0:
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'GTIN', 'Variant Name', 'Category Name', 'Brand Name', 'Price (€)', 'Inventory', 'Image URL',
            'Seller', 'Seller Price (€)', 'MOV (€)', 'Stock', 'Ordering Qty', 'Total Price (€)', 'Unit', 'Sellers Returned'
        ])

# Read existing GTINs
def get_existing_gtins():
    existing_gtins = set()
    if os.path.exists(csv_path) and os.stat(csv_path).st_size > 0:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                existing_gtins.add(row[0])
    return existing_gtins

existing_gtins = get_existing_gtins()

def login():
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
    global headers
    backoff = 5
    max_backoff = 120

    while True:
        try:
            response = requests.request(method, url, headers=headers, **kwargs)

            if 'application/json' not in response.headers.get('Content-Type', ''):
                print(f"⚠️ Non-JSON response from {url}. Retrying after {backoff}s...")
                time.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)
                continue

            if response.status_code == 401 and retry > 0:
                print("🔁 Token expired. Re-authenticating...")
                if login():
                    return safe_request(method, url, retry=retry - 1, **kwargs)
                else:
                    return None

            response.raise_for_status()

            if response.status_code == 400:
                error_message = response.json().get('message', '')
                if 'quantity' in error_message and "Ensure this value is greater than or equal to 1." in error_message:
                    print(f"⚠️ Quantity error: {error_message}")
                    return None

            return response

        except requests.exceptions.HTTPError as http_err:
            print(f"❌ HTTP error: {http_err} | {http_err.response.text}")
            return None
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
    with gtin_lock:
        if gtin in existing_gtins:
            print(f"🔄 Skipping already processed GTIN: {gtin}")
            return

    variant = get_variant_by_gtin(gtin)
    if not variant:
        print(f"⚠️ Skipping GTIN {gtin}: Variant not found.")
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

        print(f"📊 Sellers for {variant_name} (GTIN: {gtin}): {len(offers)}")

        if not offers:
            print(f"❌ No offers for {variant_name}")
            return

        requested_quantity = 100
        valid_offers = [
            offer for offer in offers
            if requested_quantity * float(offer["price"]) >= float(offer["mov"])
        ]

        if not valid_offers:
            print(f"⚠️ No valid offers meet MOV for {variant_name}")
            return

        with csv_lock, open(csv_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            for offer in valid_offers:
                offer_qid = offer["qid"]
                available_quantity = offer.get("inventory", 0)
                quantity_to_order = min(requested_quantity, available_quantity)
                total_price = float(offer["price"]) * quantity_to_order

                writer.writerow([
                    gtin, variant_name, category_name, brand_name, price, inventory, image_url,
                    offer['seller'], offer['price'], offer['mov'], available_quantity, quantity_to_order,
                    f"{total_price:.2f}", offer["unit"], len(offers)
                ])

                print(f"📦 Offer:")
                print(f"    Seller: {offer['seller']}")
                print(f"    Price: €{offer['price']}")
                print(f"    Seller Stock: {available_quantity}")
                print(f"    Ordering Qty: {quantity_to_order}")
                print(f"    Total: €{total_price:.2f}")

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

        with gtin_lock:
            existing_gtins.add(gtin)

    except Exception as e:
        print(f"❌ Exception on GTIN {gtin}: {e}")

# Login first
if not login():
    print("❌ Cannot proceed without login.")
    exit()

# Read GTINs
file_path = '~/DATA/variants.csv'
file_path = os.path.expanduser(file_path)
df = pd.read_csv(file_path)
gtins_to_process = df['GTIN'].dropna().astype(str).unique().tolist()

# Process using ThreadPool
with ThreadPoolExecutor(max_workers=1) as executor:
    futures = {executor.submit(process_gtin, gtin): gtin for gtin in gtins_to_process}
    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing GTINs"):
        pass

print("💾 All data saved to variants_sellers.csv")
