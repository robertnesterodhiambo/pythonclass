import requests

# Base URL
QOGITA_API_URL = "https://api.qogita.com"

# Login credentials — use environment variables instead of hardcoding in real use
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"  # 🔒 Consider storing securely

# Login to retrieve the token and active cart ID
try:
    response = requests.post(
        url=f"{QOGITA_API_URL}/auth/login/",
        json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
    )

    response.raise_for_status()
    data = response.json()

    access_token = data["accessToken"]
    cart_qid = data["user"]["activeCartQid"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    print("Login successful!")
    print("Access Token:", access_token)  # just to show it's retrieved
    print("Active Cart QID:", cart_qid)

    # Download variant data
    url = "https://api.qogita.com/variants/search/download/"
    response = requests.get(url, headers=headers)

    response.raise_for_status()  # Raise error if not 200

    # Save to CSV file
    with open("/home/dragon/DATA/variants.csv", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("Variants data saved to variants.csv")

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
except KeyError:
    print("Unexpected response structure:", response.text)
