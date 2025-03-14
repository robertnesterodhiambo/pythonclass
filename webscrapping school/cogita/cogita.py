import requests

# Base URL for Qogita's API
QOGITA_API_URL = "https://api.qogita.com"

# Login details for user
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Send authentication request
response = requests.post(
    url=f"{QOGITA_API_URL}/auth/login/",
    json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
)

# Attempt to parse the response
try:
    response_json = response.json()
    print("Response JSON:", response_json)  # Debugging

    if "accessToken" in response_json:
        access_token = response_json["accessToken"]
        bearer_token = f"Bearer {access_token}"

        print("\nAccess Token:", access_token)
        
        # Define headers with Bearer token
        headers = {
            "Authorization": bearer_token,
            "Content-Type": "application/json"
        }

        # Fetch product data
        product_response = requests.get(f"{QOGITA_API_URL}/products", headers=headers)

        if product_response.status_code == 200:
            products = product_response.json()

            # Extract and print required details
            for product in products.get("items", []):
                supplier = product.get("supplier", "N/A")
                gtin = product.get("gtin", "N/A")
                name = product.get("name", "N/A")
                category = product.get("category", "N/A")
                brand = product.get("brand", "N/A")
                price = product.get("price", {}).get("eur", "N/A")  # Assuming price is under 'eur'
                unit = product.get("unit", "N/A")
                inventory = product.get("inventory", "N/A")
                product_link = product.get("url", "N/A")

                print(f"\nSupplier: {supplier}")
                print(f"GTIN: {gtin}")
                print(f"Name: {name}")
                print(f"Category: {category}")
                print(f"Brand: {brand}")
                print(f"€ Price inc. shipping: {price}")
                print(f"Unit: {unit}")
                print(f"Inventory: {inventory}")
                print(f"Product Link: {product_link}")
                print("-" * 50)

        else:
            print("Failed to fetch products:", product_response.text)

    else:
        print("Failed to retrieve access token:", response_json)

except requests.exceptions.JSONDecodeError:
    print("Error: Unable to parse JSON response. Raw response:", response.text)
