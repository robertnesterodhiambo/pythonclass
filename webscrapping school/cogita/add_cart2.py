import requests
import csv
import time
import os

# Credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Session variables
access_token = None
headers = {}
cart_qid = None

# Prepare CSV File (open in append mode so data is added incrementally)
csv_file = open('variants_sellers.csv', mode='a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# Check if CSV has headers, if not write headers
if os.stat('variants_sellers.csv').st_size == 0:
    csv_writer.writerow([
        'GTIN', 'Variant Name', 'Category Name', 'Brand Name', 'Price (€)', 'Inventory', 'Image URL', 
        'Seller', 'MOV (€)', 'Available Qty', 'Ordering Qty', 'Total Price (€)', "Unit"
    ])

# Read existing GTINs from the CSV to avoid duplicates
def get_existing_gtins():
    existing_gtins = set()
    if os.path.exists('variants_sellers.csv') and os.stat('variants_sellers.csv').st_size > 0:
        with open('variants_sellers.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader, None)  # Skip header row, or None if no header exists
            if header:  # If there's a header row, proceed to read the data
                for row in csv_reader:
                    existing_gtins.add(row[0])  # GTIN is in the first column
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
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 401:  # Unauthorized
            print("🔁 Token expired, re-authenticating...")
            login()
            response = requests.request(method, url, headers=headers, **kwargs)
        else:
            print(f"❌ HTTP error occurred: {http_err}")
            return None
    except requests.exceptions.RequestException as err:
        print(f"❌ Request error occurred: {err}")
        return None
    return response

def get_variants(page):
    """Fetch variants from the Qogita API."""
    return safe_request(
        "GET",
        f"{QOGITA_API_URL}/variants/search/?page={page}&size=1000"
    ).json()

def get_offers(fid, slug):
    """Fetch offers for a variant from the Qogita API."""
    offers_url = f"{QOGITA_API_URL}/variants/{fid}/{slug}/offers/"
    offers_raw_response = safe_request("GET", offers_url)
    if offers_raw_response and offers_raw_response.ok:
        return offers_raw_response.json()
    return []

def process_variant(variant):
    """Process each variant and fetch its details."""
    try:
        gtin = variant.get('gtin', '')
        variant_name = variant["name"]
        fid = variant["fid"]
        slug = variant["slug"]
        category_name = variant.get('categoryName', '')
        brand_name = variant.get('brandName', '')
        price = variant.get('price', '')
        inventory = variant.get('inventory', '')
        image_url = variant.get('imageUrl', '')

        # Skip if GTIN already exists
        if gtin in existing_gtins:
            print(f"🔄 Skipping already processed GTIN: {gtin}")
            return

        # Fetch offers for this variant
        offers_response = get_offers(fid, slug)

        if not offers_response:
            print(f"❌ Failed to fetch offers for {variant_name}")
            return

        offers = offers_response.get("offers", [])
        if not offers:
            print(f"❌ No offers found for {variant_name}.")
            return

        # Start with the requested quantity
        requested_quantity = 100

        # Find valid offers that meet the MOV requirement
        valid_offers = [
            offer for offer in offers
            if requested_quantity * float(offer["price"]) >= float(offer["mov"])
        ]

        if not valid_offers:
            print(f"⚠️ No valid offers for {variant_name} meet the MOV requirement.")
            return

        # Choose the best offer (min price)
        best_offer = min(valid_offers, key=lambda x: float(x["price"]))
        offer_qid = best_offer["qid"]

        # Check available quantity and adjust order quantity if needed
        available_quantity = best_offer.get("availableQuantity", 0)
        quantity_to_order = min(requested_quantity, available_quantity)
        total_price = float(best_offer["price"]) * quantity_to_order

        # Save to CSV immediately before printing
        csv_writer.writerow([
            gtin, variant_name, category_name, brand_name, price, inventory, image_url, 
            best_offer['seller'], best_offer['mov'], available_quantity, quantity_to_order, f"{total_price:.2f}", best_offer["unit"]
        ])
        csv_file.flush()  # Ensures data is written to the file immediately

        # Print the output after saving the data
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
        print(f"unit is : {best_offer['unit']}")

        # Add to cart
        add_to_cart_response = safe_request(
            "POST",
            f"{QOGITA_API_URL}/carts/{cart_qid}/lines/",
            json={"offerQid": offer_qid, "quantity": quantity_to_order}
        )

        if add_to_cart_response and add_to_cart_response.ok:
            print(f"✅ Added {quantity_to_order} units of {variant_name} to cart.\n")
        else:
            print(f"❌ Failed to add {variant_name} to cart:", add_to_cart_response.json() if add_to_cart_response else "No response")

        # Add GTIN to the set of existing GTINs after processing
        existing_gtins.add(gtin)

    except Exception as e:
        print(f"❌ Error processing variant {variant.get('name', 'Unknown')}: {e}")

# Initial login
login()

# Step 2: Get all variants (page by page)
page = 1
while True:
    search_response = get_variants(page)

    if not search_response or "results" not in search_response:
        print("❌ No more products found or failed to retrieve products.")
        break

    results = search_response.get("results", [])
    if not results:
        print("❌ No products found on this page.")
        break

    for variant in results:
        process_variant(variant)

    page += 1
    time.sleep(1)  # To avoid hitting API too quickly

# Close the CSV file after processing all pages
csv_file.close()
print("💾 Data saved to variants_sellers.csv")
