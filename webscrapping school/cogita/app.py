import requests

# Base URL for Qogita's API.
QOGITA_API_URL = "https://api.qogita.com"

# Login credentials (FOR TESTING ONLY — DO NOT use this in production).
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Authentication request
response = requests.post(
    url=f"{QOGITA_API_URL}/auth/login/",
    json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
).json()

# Check for success
if "accessToken" in response:
    # Retrieve the access token and cart QID
    access_token = response["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    cart_qid = response["user"]["activeCartQid"]

    print("Login successful.")
    print("Access Token:", access_token)
    print("Active Cart QID:", cart_qid)
else:
    print("Login failed:", response)
