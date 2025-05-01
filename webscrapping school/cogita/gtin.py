import requests
import csv
import time
import os
import random

# Credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Session variables
access_token = None
headers = {}
cart_qid = None

# Prepare CSV File (open in append mode so data is added incrementally)
csv_file = open('/home/dragon/DATA/variants_sellers.csv', mode='a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# Check if CSV has headers, if not write headers
if os.stat('variants_sellers.csv').st_size == 0:
    csv_writer.writerow([
        'GTIN', 'Variant Name', 'Category Name', 'Brand Name', 'Price (€)', 'Inventory', 'Image URL',
        'Seller', 'MOV (€)', 'Available Qty', 'Ordering Qty', 'Total Price (€)', 'Unit', 'Sellers Returned'
    ])

# Read existing GTINs from the CSV to avoid duplicates
def get_existing_gtins():
    existing_gtins = set()
    if os.path.exists('variants_sellers.csv') and os.stat('variants_sellers.csv').st_size > 0:
        with open('variants_sellers.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader, None)
            if header:
                for row in csv_reader:
                    existing_gtins.add(row[0])
    return existing_gtins

existing_gtins = get_existing_gtins()

def login():
    """Login to the API and set the access token and headers."""
    global access_token, headers, cart_qid
    print("🔐 Logging in...")
    auth_response = requests.post(
        f"{QOGITA_API_URL}/auth/login/",
        json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
    ).json()

    if "accessToken" not in auth_response:
        print("❌ Login failed:", auth_response)
        exit()

    access_token = auth_response["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    cart_qid = auth_response["user"]["activeCartQid"]
    print("✅ Authenticated successfully.")
    print(f"🛒 Active Cart QID: {cart_qid}")

def safe_request(method, url, **kwargs):
    """Wrapper to handle 401 errors by re-logging in and retrying once."""
    global headers
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
        print(f"Response body: {http_err.response.text}")
        if http_err.response.status_code == 401:
            print("🔁 Token expired, re-authenticating...")
            login()
            response = requests.request(method, url, headers=headers, **kwargs)
        else:
            return None
    except requests.exceptions.RequestException as err:
        print(f"❌ Request error occurred: {err}")
        return None
    return response

def get_variant_by_gtin(gtin):
    """Fetch variant by GTIN."""
    response = safe_request("GET", f"{QOGITA_API_URL}/variants/{gtin}/")
    if response and response.ok:
        return response.json()
    return None

def get_offers(fid, slug):
    offers_url = f"{QOGITA_API_URL}/variants/{fid}/{slug}/offers/"
    print(f"🔄 Fetching offers for variant {fid} - {slug}...")
    offers_raw_response = safe_request("GET", offers_url)
    if offers_raw_response and offers_raw_response.ok:
        return offers_raw_response.json()
    return []

def process_gtin(gtin):
    if gtin in existing_gtins:
        print(f"🔄 Skipping already processed GTIN: {gtin}")
        return

    variant = get_variant_by_gtin(gtin)
    if not variant:
        return

    try:
        variant_name = variant["name"]
        fid = variant["fid"]
        slug = variant["slug"]
        category_name = variant.get('categoryName', '')
        brand_name = variant.get('brandName', '')
        price = variant.get('price', '')
        inventory = variant.get('inventory', '')
        image_url = variant.get('imageUrl', '')

        offers_response = get_offers(fid, slug)
        offers = offers_response.get("offers", []) if offers_response else []

        # 🔢 Print how many sellers returned
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
            print(f"⚠️ No valid offers for {variant_name} meet the MOV requirement.")
            return

        for offer in valid_offers:
            best_offer = offer
            offer_qid = best_offer["qid"]
            available_quantity = best_offer.get("availableQuantity", 0)
            quantity_to_order = min(requested_quantity, available_quantity)
            total_price = float(best_offer["price"]) * quantity_to_order

            csv_writer.writerow([
                gtin, variant_name, category_name, brand_name, price, inventory, image_url,
                best_offer['seller'], best_offer['mov'], available_quantity, quantity_to_order,
                f"{total_price:.2f}", best_offer["unit"], len(offers)  # Sellers count added here
            ])
            csv_file.flush()

            print(f"📦 Selected Offer for {variant_name}:")
            print(f"    GTIN: {gtin}")
            print(f"    Category: {category_name}")
            print(f"    Brand: {brand_name}")
            print(f"    Price: €{price}")
            print(f"    Inventory: {inventory}")
            print(f"    Image URL: {image_url}")
            print(f"    Seller: {best_offer['seller']}")
            print(f"    MOV: €{best_offer['mov']}")
            print(f"    Available: {available_quantity}")
            print(f"    Ordering: {quantity_to_order} units | Total: €{total_price:.2f}")
            print(f"    Unit: {best_offer['unit']}")

            print(f"🔄 Adding to cart with offerQid: {offer_qid}, Quantity: {quantity_to_order}")
            add_to_cart_response = safe_request(
                "POST",
                f"{QOGITA_API_URL}/carts/{cart_qid}/lines/",
                json={"offerQid": offer_qid, "quantity": quantity_to_order}
            )

            if add_to_cart_response and add_to_cart_response.ok:
                print(f"✅ Added {quantity_to_order} units of {variant_name} to cart.\n")
            else:
                print(f"❌ Failed to add {variant_name} to cart:", add_to_cart_response.json() if add_to_cart_response else "No response")

        existing_gtins.add(gtin)

        sleep_duration = random.uniform(2, 5)
        print(f"⏳ Waiting for {sleep_duration:.2f} seconds...\n")
        time.sleep(sleep_duration)

    except Exception as e:
        print(f"❌ Error processing GTIN {gtin}: {e}")

# Initial login
login()

# Example list of GTINs to process
gtins_to_process = ["3349668614608", "0987654321", "1122334455"]  # Replace with your actual list

# Start processing GTINs
for gtin in gtins_to_process:
    process_gtin(gtin)

# Close the file
csv_file.close()
print("💾 Data saved to variants_sellers.csv")
