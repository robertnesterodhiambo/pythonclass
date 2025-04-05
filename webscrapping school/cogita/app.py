import requests
import time
import csv

# Base URL and credentials
QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Step 1: Authentication
auth_response = requests.post(
    f"{QOGITA_API_URL}/auth/login/",
    json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
).json()

if "accessToken" in auth_response:
    access_token = auth_response["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    cart_qid = auth_response["user"]["activeCartQid"]

    print("Login successful.")
    print(f"Active Cart QID: {cart_qid}\n")

    # Open CSV file for writing (append mode to add new entries)
    with open("products.csv", mode="w", newline='', encoding="utf-8") as file:
        # Define CSV writer
        fieldnames = ["gtin", "name", "categoryName", "brandName", "price", "inventory", "imageUrl"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header to the CSV file
        writer.writeheader()

        # Step 2: Paginate through all results
        page = 1
        size = 500000  # Reasonable size per page
        total_count = 0

        while True:
            print(f"Fetching page {page}...")

            search_url = (
                f"{QOGITA_API_URL}/variants/search/?"
                f"page={page}&size={size}"
            )

            response = requests.get(url=search_url, headers=headers).json()

            results = response.get("results", [])
            if not results:
                print("No more results. Done.")
                break

            for variant in results:
                # Write each result to the CSV file
                writer.writerow({
                    "gtin": variant.get('gtin', ''),
                    "name": variant.get('name', ''),
                    "categoryName": variant.get('categoryName', ''),
                    "brandName": variant.get('brandName', ''),
                    "price": variant.get('price', ''),
                    "inventory": variant.get('inventory', ''),
                    "imageUrl": variant.get('imageUrl', '')
                })

                print(f"Saved: {variant['gtin']} | {variant['name']} | {variant['categoryName']} | "
                      f"{variant['brandName']} | {variant['price']} | {variant['inventory']} | {variant['imageUrl']}")

                total_count += 1

            page += 1
            time.sleep(0.5)  # Sleep to avoid rate limits

        print(f"\n✅ Total products retrieved: {total_count}")

else:
    print("Login failed:", auth_response)
