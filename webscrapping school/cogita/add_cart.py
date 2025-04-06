import requests
import csv

# Credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Session variables
access_token = None
headers = {}
cart_qid = None

# Prepare CSV File (open in append mode so data is added incrementally)
csv_file = open('variants_sellers.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Variant Name', 'Seller', 'Price (€)', 'MOV (€)', 'Available Qty', 'Ordering Qty', 'Total Price (€)'])

def login():
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
    response = requests.request(method, url, headers=headers, **kwargs)
    if response.status_code == 401:
        print("🔁 Token expired, re-authenticating...")
        login()
        response = requests.request(method, url, headers=headers, **kwargs)
    return response

# Initial login
login()

# Step 2: Get all variants (page by page)
page = 1
while True:
    search_response = safe_request(
        "GET",
        f"{QOGITA_API_URL}/variants/search/?page={page}&size=1000"
    ).json()

    results = search_response.get("results", [])
    if not results:
        print("❌ No more products found.")
        break

    for variant in results:
        fid = variant["fid"]
        slug = variant["slug"]
        variant_name = variant["name"]

        offers_url = f"{QOGITA_API_URL}/variants/{fid}/{slug}/offers/"
        offers_raw_response = safe_request("GET", offers_url)

        if not offers_raw_response.ok:
            print(f"❌ Failed to fetch offers for {variant_name} | Status Code: {offers_raw_response.status_code}")
            print("🔎 Response text:", offers_raw_response.text)
            continue

        try:
            offers_response = offers_raw_response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"❌ Could not decode JSON for offers of {variant_name}")
            print("🔎 Raw response content:", offers_raw_response.text)
            continue

        offers = offers_response.get("offers", []) if isinstance(offers_response, dict) else []

        if not offers:
            print(f"❌ No offers found for {variant_name}.")
            continue

        # Start with the requested quantity
        requested_quantity = 100

        # Find valid offers that meet the MOV requirement
        valid_offers = [
            offer for offer in offers
            if requested_quantity * float(offer["price"]) >= float(offer["mov"])
        ]

        if not valid_offers:
            print(f"⚠️ No valid offers for {variant_name} meet the MOV requirement.")
            continue

        # Choose the best offer (min price)
        best_offer = min(valid_offers, key=lambda x: float(x["price"]))
        offer_qid = best_offer["qid"]

        # Check available quantity and adjust order quantity if needed
        available_quantity = best_offer.get("availableQuantity", 0)
        quantity_to_order = min(requested_quantity, available_quantity)
        total_price = float(best_offer["price"]) * quantity_to_order

        # Save to CSV immediately before printing
        csv_writer.writerow([
            variant_name,
            best_offer['seller'],
            best_offer['price'],
            best_offer['mov'],
            available_quantity,
            quantity_to_order,
            f"{total_price:.2f}"
        ])
        csv_file.flush()  # Ensures data is written to the file immediately

        # Print the output after saving the data
        print(f"📦 Selected Offer for {variant_name}:")
        print(f"    Seller: {best_offer['seller']}")
        print(f"    Price: €{best_offer['price']}")
        print(f"    MOV: €{best_offer['mov']}")
        print(f"    Available: {available_quantity}")
        print(f"    Ordering: {quantity_to_order} units | Total: €{total_price:.2f}")

        # Add to cart
        add_to_cart_response = safe_request(
            "POST",
            f"{QOGITA_API_URL}/carts/{cart_qid}/lines/",
            json={"offerQid": offer_qid, "quantity": quantity_to_order}
        )

        if add_to_cart_response.ok:
            print(f"✅ Added {quantity_to_order} units of {variant_name} to cart.\n")
        else:
            try:
                print(f"❌ Failed to add {variant_name} to cart:", add_to_cart_response.json())
            except:
                print(f"❌ Failed to add {variant_name} to cart. Raw response:", add_to_cart_response.text)

    page += 1

# Close the CSV file after processing all pages
csv_file.close()
print("💾 Data saved to variants_sellers.csv")
