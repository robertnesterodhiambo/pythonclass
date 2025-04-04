import requests

# Credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Step 1: Login
auth_response = requests.post(
    f"{QOGITA_API_URL}/auth/login/",
    json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
).json()

if "accessToken" not in auth_response:
    print("Login failed:", auth_response)
    exit()

access_token = auth_response["accessToken"]
headers = {"Authorization": f"Bearer {access_token}"}
cart_qid = auth_response["user"]["activeCartQid"]

print("✅ Authenticated successfully.")
print(f"🛒 Active Cart QID: {cart_qid}")

# Step 2: Get all variants (page by page)
page = 1
while True:
    search_response = requests.get(
        f"{QOGITA_API_URL}/variants/search/?page={page}&size=100",  # Adjust size as needed
        headers=headers
    ).json()

    results = search_response.get("results", [])
    if not results:
        print("❌ No more products found.")
        break  # Exit the loop when no products are left

    # Process each product (variant)
    for variant in results:
        fid = variant["fid"]
        slug = variant["slug"]

        # Step 3: Get offers for each variant
        offers_url = f"{QOGITA_API_URL}/variants/{fid}/{slug}/offers/"
        offers_response = requests.get(offers_url, headers=headers).json()

        # DEBUG: print response to understand structure
        print("📄 Offers Response Structure for Variant:", variant["name"])
        print(offers_response)

        # Extract offers safely
        offers = offers_response.get("results", []) if isinstance(offers_response, dict) else offers_response

        if not offers:
            print(f"❌ No offers found for {variant['name']}.")
            continue

        # Pick first offer (you can apply your own logic for choosing)
        offer = offers[0]
        offer_qid = offer["qid"]
        quantity = 100  # You can change this based on your needs

        print(f"📦 Found Offer for {variant['name']}: {offer_qid} | Price: {offer['price']} | Available: {offer['inventory']}")

        # Step 4: Add to cart using offerQid
        add_response = requests.post(
            url=f"{QOGITA_API_URL}/carts/{cart_qid}/lines/",
            json={"offerQid": offer_qid, "quantity": quantity},
            headers=headers
        )

        if add_response.ok:
            print(f"✅ Successfully added {quantity} units of {variant['name']} to cart.")
        else:
            print(f"❌ Failed to add {variant['name']} to cart:", add_response.json())

    page += 1  # Move to the next page of variants
