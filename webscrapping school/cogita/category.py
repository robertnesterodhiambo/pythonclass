import requests

# Define API credentials and base URL
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"
QOGITA_API_URL = "https://api.qogita.com"

def get_auth_token():
    """Authenticate and retrieve an access token"""
    auth_url = f"{QOGITA_API_URL}/auth/token"
    response = requests.post(auth_url, json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD})
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Authentication failed: {response.text}")

def search_variants():
    """Search for variants with filters applied"""
    token = get_auth_token()  # Authenticate and get token

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Properly formatted query parameters
    params = {
        "query": "perfume 100ml",
        "has_deals": "true",
        "category_name": "Cosmetics",
        "brand_name": ["Paco Rabanne", "Calvin Klein"],  # Multiple brands as a list
        "stock_availability": "in_stock",
        # "cart_allocation_qid": "<your_real_uuid>",  # Uncomment if needed
        "page": 1,
        "size": 10
    }

    response = requests.get(f"{QOGITA_API_URL}/variants/search/", params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for variant in data["results"]:
            print(f"{variant['gtin']} | {variant['name']} | {variant['price']} | {variant['inventory']} | {variant['imageUrl']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Run search function
search_variants()
