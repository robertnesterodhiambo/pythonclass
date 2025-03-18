import requests
import pandas as pd

# Base API URL
QOGITA_API_URL = "https://api.qogita.com"

# Headers with authentication token
headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlNjBkMDk3Zi1iZTgxLTQ3YzMtYWZiNS1mMzUzNDA0ZWNlNTEiLCJleHAiOjE3NDE5NzgxNjIsImlhdCI6MTc0MTk3Nzg2MiwiYXVkIjoicW9naXRhOmF1dGg6YWNjZXNzIiwiaXNzIjoicW9naXRhIn0.E8aGxJoc4O9sARiDSSolxKm0RQrmudaU7Djp4BvaR6I",
    "accept": "application/json"
}

# Step 1: Fetch Available Categories
categories_url = f"{QOGITA_API_URL}/categories/"
categories_response = requests.get(url=categories_url, headers=headers)

category_mapping = {}  # Dictionary to store category ID -> category name mapping
if categories_response.status_code == 200:
    categories_data = categories_response.json()
    
    if isinstance(categories_data, list):
        category_mapping = {str(category.get("id", "N/A")): category.get("name", "N/A") for category in categories_data}
    else:
        print("\nUnexpected category response format:", categories_data)
else:
    print(f"\nFailed to fetch categories (Status {categories_response.status_code}): {categories_response.text}")

# Step 2: Fetch Brands to Map Brand IDs to Names
brands_url = f"{QOGITA_API_URL}/brands/"
brands_response = requests.get(brands_url, headers=headers)

brand_mapping = {}  # Dictionary to store brand ID -> brand name mapping
if brands_response.status_code == 200:
    brands_data = brands_response.json()
    
    # Handle response format
    if isinstance(brands_data, dict):
        brands_list = brands_data.get("results", [])  # Adjust key based on API response
    elif isinstance(brands_data, list):
        brands_list = brands_data  # If API directly returns a list
    else:
        brands_list = []
    
    # Populate brand mapping
    for brand in brands_list:
        if isinstance(brand, dict):
            brand_mapping[str(brand.get("id", "N/A"))] = brand.get("name", "N/A")
else:
    print(f"\nFailed to fetch brands (Status {brands_response.status_code}): {brands_response.text}")

# Step 3: Search Query Without Category Name
search_url = (f"{QOGITA_API_URL}/variants/search/?"
              f"&has_deals=true"
              f"&has_deals=false"
              f"&stock_availability=in_stock"
              f"&size=100000")

# Step 4: Request to fetch products
response = requests.get(url=search_url, headers=headers)

# Step 5: Check if request was successful
if response.status_code == 200:
    data = response.json()  # Convert to JSON
    products = data.get("results", [])

    # Extract required details
    product_list = []
    for product in products:
        product_list.append({
            "Supplier": product.get("supplier_name", "N/A"),
            "GTIN": product.get("gtin", "N/A"),
            "Name": product.get("name", "N/A"),
            "Category": product.get("categoryName"),  # Ensure category_id is a string
            "Brand": product.get("brandName"),  # Ensure brand_id is a string
            "€ Price inc. shipping": product.get("price", "N/A"),
            "Unit": product.get("unit", "N/A"),
            "Inventory": product.get("inventory", "N/A"),
            "Product Link": product.get("imageUrl", "N/A"),
            "position": product.get("position")
        })

    # Convert to Pandas DataFrame
    df = pd.DataFrame(product_list)

    # Pr                        int DataFrame
    print("\nProduct Data:")
    print(df)

else:
    print(f"\nFailed to fetch products (Status {response.status_code}): {response.text}")

# Save results to CSV
df.to_csv("sample.csv", index=False)
print("response")

response = requests.get(url=search_url, headers=headers).json()

for variant in response.get("results", []):
    print(f"{variant['gtin']} | {variant['name']} | {variant['price']} | {variant['imageUrl']}")



