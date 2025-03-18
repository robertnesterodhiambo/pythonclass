import requests
import pandas as pd

# Base URL for Qogita's API.
QOGITA_API_URL = "https://api.qogita.com"

# Login details for user.
QOGITA_EMAIL = "jacek.budner@gmail.com"  # Replace with your Qogita email
QOGITA_PASSWORD = "JB100noga!"  # Replace with your Qogita password

# Authentication request.
response = requests.post(url=f"{QOGITA_API_URL}/auth/login/",
                         json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}).json()

# Retrieve the access token and create the auth header to use in all requests.
access_token = response["accessToken"]
headers = {"Authorization": f"Bearer {access_token}"}

# Read the CSV file and get the first 10 GTIN values.
df = pd.read_csv("sample.csv")
gtin_list = df["GTIN"].dropna().astype(str).head(10).tolist()

# Create new columns to store API response data.
df_filtered = df.head(10).copy()  # Filter first 10 rows
df_filtered["Price"] = None
df_filtered["Currency"] = None
df_filtered["Inventory"] = None
df_filtered["Unit"] = None

# Iterate through the first 10 GTINs and fetch variant details.
for index, gtin in enumerate(gtin_list):
    variant = requests.get(url=f"{QOGITA_API_URL}/variants/{gtin}/", headers=headers).json()

    # Update the DataFrame with the retrieved data
    df_filtered.at[index, "Price"] = variant.get("price", "N/A")
    df_filtered.at[index, "Currency"] = variant.get("priceCurrency", "N/A")
    df_filtered.at[index, "Inventory"] = variant.get("inventory", "N/A")
    df_filtered.at[index, "Unit"] = variant.get("unit", "N/A")

    print(f"{variant['gtin']} | {variant['name']} | {variant.get('price', 'N/A')} | {variant.get('priceCurrency', 'N/A')} | "
          f"{variant.get('inventory', 'N/A')} | {variant.get('unit', 'N/A')}")

# Save the updated DataFrame to a new CSV file
df_filtered.to_csv("updated_sample.csv", index=False)

print("Updated data saved to updated_sample.csv")

