import requests
import pandas as pd

# Configuration
HEAD_LIMIT = 100  # Change this to adjust how many GTINs to process
QOGITA_API_URL = "https://api.qogita.com"

# Login details for user.
QOGITA_EMAIL = "jacek.budner@gmail.com"  # Replace with your Qogita email
QOGITA_PASSWORD = "JB100noga!"  # Replace with your Qogita password

# Authentication request.
auth_response = requests.post(url=f"{QOGITA_API_URL}/auth/login/",
                              json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD})

# Check if login was successful
if auth_response.status_code != 200:
    print(f"Error: Unable to authenticate. Status Code: {auth_response.status_code}, Response: {auth_response.text}")
    exit()

auth_data = auth_response.json()
access_token = auth_data.get("accessToken")

if not access_token:
    print("Error: Failed to retrieve access token.")
    exit()

headers = {"Authorization": f"Bearer {access_token}"}

# Read the CSV file and get the first 'HEAD_LIMIT' GTIN values.
df = pd.read_csv("sample.csv")
gtin_list = df["GTIN"].dropna().astype(str).head(HEAD_LIMIT).tolist()

# Create a new DataFrame to store the API results.
df_filtered = df.head(HEAD_LIMIT).copy()  # Keep only the first 'HEAD_LIMIT' rows
df_filtered["Price"] = None
df_filtered["Currency"] = None
df_filtered["Inventory"] = None
df_filtered["Unit"] = None

# Iterate through the GTINs and fetch variant details.
for index, gtin in enumerate(gtin_list):
    try:
        response = requests.get(url=f"{QOGITA_API_URL}/variants/{gtin}/", headers=headers)
        
        # Check if the response is valid JSON
        if response.status_code != 200:
            print(f"Warning: Failed to fetch GTIN {gtin}. Status Code: {response.status_code}, Response: {response.text}")
            continue

        variant = response.json()

        # Update the DataFrame with the retrieved data
        df_filtered.at[index, "Price"] = variant.get("price", "N/A")
        df_filtered.at[index, "Currency"] = variant.get("priceCurrency", "N/A")
        df_filtered.at[index, "Inventory"] = variant.get("inventory", "N/A")
        df_filtered.at[index, "Unit"] = variant.get("unit", "N/A")

        print(f"{variant.get('gtin', 'N/A')} | {variant.get('name', 'N/A')} | {variant.get('price', 'N/A')} | "
              f"{variant.get('priceCurrency', 'N/A')} | {variant.get('inventory', 'N/A')} | {variant.get('unit', 'N/A')}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GTIN {gtin}: {e}")
    except ValueError:
        print(f"Error: Received invalid JSON response for GTIN {gtin}. Response: {response.text}")

# Save the updated DataFrame to a new CSV file
df_filtered.to_csv("updated_sample.csv", index=False)

print(f"Updated data for {HEAD_LIMIT} GTINs saved to updated_sample.csv")
