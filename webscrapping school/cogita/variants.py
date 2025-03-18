import requests

QOGITA_API_URL = "https://api.qogita.com"  # Make sure this is the correct base URL

# Headers with authentication token
headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlNjBkMDk3Zi1iZTgxLTQ3YzMtYWZiNS1mMzUzNDA0ZWNlNTEiLCJleHAiOjE3NDE5NzgxNjIsImlhdCI6MTc0MTk3Nzg2MiwiYXVkIjoicW9naXRhOmF1dGg6YWNjZXNzIiwiaXNzIjoicW9naXRhIn0.E8aGxJoc4O9sARiDSSolxKm0RQrmudaU7Djp4BvaR6I",
    "accept": "application/json"
}

params = {
    "query": "perfume 100ml",
    "has_deals": "true",
    # "category_name": "Cosmetics",
    "brand_name": "Paco Rabanne,Calvin Klein",  # Assuming API supports comma-separated values
    "stock_availability": "in_stock",
    # "cart_allocation_qid": "<uuid>",  # Replace with actual UUID
    "page": 1,
    "size": 10
}

response = requests.get(f"{QOGITA_API_URL}/variants/search/", params=params, headers=headers).json()

for variant in response.get("results", []):
    print(f"{variant['gtin']} | {variant['name']} | {variant['price']} | {variant['inventory']} | {variant['imageUrl']}")

print(response)
