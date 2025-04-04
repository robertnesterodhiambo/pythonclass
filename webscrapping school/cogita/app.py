import requests

# Base URL for Qogita's API.
QOGITA_API_URL = "https://api.qogita.com"

# Login credentials (FOR TESTING ONLY — DO NOT hardcode in production).
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Step 1: Authentication
auth_response = requests.post(
    url=f"{QOGITA_API_URL}/auth/login/",
    json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
).json()

if "accessToken" in auth_response:
    access_token = auth_response["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    cart_qid = auth_response["user"]["activeCartQid"]

    print("Login successful.")
    print(f"Access Token: {access_token}")
    print(f"Active Cart QID: {cart_qid}")
    
    # Step 2: Search request with filters
    search_url = (
        f"{QOGITA_API_URL}/variants/search/?" # <-- dynamically inserted
        f"&page=1"
        f"&size=10000000000"
    )

    response = requests.get(url=search_url, headers=headers).json()

    # Step 3: Output results
    print("\nSearch Results:\n---------------------------")
    for variant in response.get("results", []):
        print(f"{variant['gtin']} | {variant['name']} | {variant['categoryName']} | {variant['brandName']} | "
      f"{variant['price']} | {variant['inventory']} | {variant['imageUrl']}")

else:
    print("Login failed:", auth_response)
