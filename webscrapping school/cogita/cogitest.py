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

# Step 2: Search for product variant
query = "Yara by Lattafa Perfumes Eau De Parfum 100ml 3.4 fl oz for Women"
search_response = requests.get(
    f"{QOGITA_API_URL}/variants/search/?query={query}&page=1&size=10",
    headers=headers
).json()

results = search_response.get("results", [])
if not results:
    print("❌ No products found.")
    exit()

variant = results[0]
fid = variant["fid"]
slug = variant["slug"]

# Step 3: Get offers from specific variant
offers_url = f"{QOGITA_API_URL}/variants/{fid}/{slug}/offers/"
offers_response = requests.get(offers_url, headers=headers).json()

# DEBUG: print response to understand structure
print("📄 Offers Response Structure:")
print(offers_response)

# Extract offers safely
offers = offers_response.get("results", []) if isinstance(offers_response, dict) else offers_response

if not offers:
    print("❌ No offers found.")
    exit()

# Pick first offer (you can apply your own logic for choosing)
offer = offers[0]
offer_qid = offer["qid"]
quantity = 100

print(f"📦 Found Offer: {offer_qid} | Price: {offer['price']} | Available: {offer['inventory']}")

# Step 4: Add to cart using offerQid
add_response = requests.post(
    url=f"{QOGITA_API_URL}/carts/{cart_qid}/lines/",
    json={"offerQid": offer_qid, "quantity": quantity},
    headers=headers
)

if add_response.ok:
    print(f"✅ Successfully added {quantity} units to cart using Offer QID.")
else:
    print("❌ Failed to add to cart:", add_response.json())

