import requests

# Base URL for Qogita's API.
QOGITA_API_URL = "https://api.qogita.com"

# Login details
QOGITA_EMAIL = "jacek.budner@gmail.com"  # Replace with your Qogita email
QOGITA_PASSWORD = "JB100noga!"  # Replace with your Qogita password

# Authentication request.
response = requests.post(url=f"{QOGITA_API_URL}/auth/login/",
                         json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}).json()

# Retrieve the access token and create the auth header to use in all requests.
access_token = response["accessToken"]
headers = {"Authorization": f"Bearer {access_token}"}

# Retrieve the active Cart identifier so that you can interact with the cart.
cart_qid = response["user"]["activeCartQid"]
print(cart_qid)