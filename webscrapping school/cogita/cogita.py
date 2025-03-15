import requests
import pandas as pd

# Base API URL
QOGITA_API_URL = "https://api.qogita.com"

# Headers with authentication token (Replace <token> with your actual token)
headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlNjBkMDk3Zi1iZTgxLTQ3YzMtYWZiNS1mMzUzNDA0ZWNlNTEiLCJleHAiOjE3NDE5NzgxNjIsImlhdCI6MTc0MTk3Nzg2MiwiYXVkIjoicW9naXRhOmF1dGg6YWNjZXNzIiwiaXNzIjoicW9naXRhIn0.E8aGxJoc4O9sARiDSSolxKm0RQrmudaU7Djp4BvaR6I",
    "Content-Type": "application/json"
}

# Step 1: Fetch Available Categories
categories_url = f"{QOGITA_API_URL}/categories"
categories_response = requests.get(url=categories_url, headers=headers)

if categories_response.status_code == 200:
    categories = categories_response.json()
    print("\nAvailable Categories:", categories)
else:
    print(f"\nFailed to fetch categories (Status {categories_response.status_code}): {categories_response.text}")

# Step 2: Fetch Brands to Map Brand IDs to Names
brands_url = f"{QOGITA_API_URL}/brands/"
brands_response = requests.get(brands_url, headers=headers)

brand_mapping = {}  # Dictionary to store brand ID -> brand name mapping
if brands_response.status_code == 200:
    brands_data = brands_response.json()
    
    # Check if response is a dictionary and contains a list of brands under a key
    if isinstance(brands_data, dict):
        brands_list = brands_data.get("results", [])  # Adjust key based on API response
    elif isinstance(brands_data, list):
        brands_list = brands_data  # If API directly returns a list

    # Populate brand mapping
    for brand in brands_list:
        if isinstance(brand, dict):  # Ensure each item is a dictionary
            brand_mapping[brand.get("id", "N/A")] = brand.get("name", "N/A")
else:
    print(f"\nFailed to fetch brands (Status {brands_response.status_code}): {brands_response.text}")

# Step 3: Search Query Without Category Name
search_url = (f"{QOGITA_API_URL}/variants/search/?"
              f"&query=perfume+100ml"  # Free text query
              f"&has_deals=true"  # Hot deals only
              f"&brand_name=Paco Rabanne"  # Filter by brand
              f"&brand_name=Calvin Klein"
              f"&stock_availability=in_stock"  # In-stock products
              f"&page=1"
              f"&size=10")  # Limit results

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
            "Supplier": product.get("supplier", "N/A"),
            "GTIN": product.get("gtin", "N/A"),
            "Name": product.get("name", "N/A"),
            "Category": product.get("category_name", "N/A"),
            "Brand": brand_mapping.get(str(product.get("brand_id", "N/A")), "N/A"),  # Ensure brand_id is a string
            "€ Price inc. shipping": product.get("price", "N/A"),
            "Unit": product.get("unit", "N/A"),
            "Inventory": product.get("inventory", "N/A"),
            "Product Link": product.get("imageUrl", "N/A")  # Assuming this is the product link
        })

    # Convert to Pandas DataFrame
    df = pd.DataFrame(product_list)

    # Print DataFrame
    print("\nProduct Data:")
    print(df)

else:
    print(f"\nFailed to fetch products (Status {response.status_code}): {response.text}")

df.to_csv("sample.csv")
