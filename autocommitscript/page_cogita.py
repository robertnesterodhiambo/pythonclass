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

category_mapping = {}
if categories_response.status_code == 200:
    categories_data = categories_response.json()
    if isinstance(categories_data, list):
        category_mapping = {str(category.get("id", "N/A")): category.get("name", "N/A") for category in categories_data}
    else:
        print("Unexpected category response format:", categories_data)
else:
    print(f"Failed to fetch categories (Status {categories_response.status_code}): {categories_response.text}")

# Step 2: Fetch Brands
brands_url = f"{QOGITA_API_URL}/brands/"
brands_response = requests.get(brands_url, headers=headers)

brand_mapping = {}
if brands_response.status_code == 200:
    brands_data = brands_response.json()
    if isinstance(brands_data, dict):
        brands_list = brands_data.get("results", [])
    elif isinstance(brands_data, list):
        brands_list = brands_data
    else:
        brands_list = []
    
    for brand in brands_list:
        if isinstance(brand, dict):
            brand_mapping[str(brand.get("id", "N/A"))] = brand.get("name", "N/A")
else:
    print(f"Failed to fetch brands (Status {brands_response.status_code}): {brands_response.text}")

# Step 3: Fetch Products with Pagination
page = 1
all_products = []
while True:
    search_url = (f"{QOGITA_API_URL}/variants/search/?"
                  f"&has_deals=true"
                  f"&has_deals=false"
                  f"&stock_availability=in_stock"
                  f"&size=100"
                  f"&page={page}")
    response = requests.get(url=search_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get("results", [])
        
        if not products:
            print("No more results. Stopping pagination.")
            break  # Stop when no more products are returned
        
        for product in products:
            all_products.append({
                "Supplier": product.get("supplier_name", "N/A"),
                "GTIN": product.get("gtin", "N/A"),
                "Name": product.get("name", "N/A"),
                "Category": product.get("categoryName"),
                "Brand": product.get("brandName"),
                "€ Price inc. shipping": product.get("price", "N/A"),
                "Unit": product.get("unit", "N/A"),
                "Inventory": product.get("inventory", "N/A"),
                "Product Link": product.get("imageUrl", "N/A"),
                "position": product.get("position")
            })
        
        print(f"Page {page} processed. Total products so far: {len(all_products)}")
        page += 1  # Move to next page
    else:
        print(f"Failed to fetch products (Status {response.status_code}): {response.text}")
        break

# Convert to DataFrame and save to CSV
df = pd.DataFrame(all_products)
df.to_csv("sample.csv", index=False)
print("Data saved to sample.csv")

