import requests

# Base URL for Qogita's API
QOGITA_API_URL = "https://api.qogita.com"

# Login details for user
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

# Send authentication request
response = requests.post(
    url=f"{QOGITA_API_URL}/auth/login/",
    json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD}
)

# Attempt to parse the response
try:
    response_json = response.json()
    print("Response JSON:", response_json)  # Debugging

    # Check if access token is in the response
    if "accessToken" in response_json:
        access_token = response_json["accessToken"]
        bearer_token = f"Bearer {access_token}"

        print("\nAccess Token:")
        print(access_token)

        print("\nBearer Token:")
        print(bearer_token)

        # Retrieve active cart ID if available
        cart_qid = response_json.get("user", {}).get("activeCartQid", "No cart found")
        print("\nCart ID:", cart_qid)
    else:
        print("Failed to retrieve access token:", response_json)

except requests.exceptions.JSONDecodeError:
    print("Error: Unable to parse JSON response. Raw response:", response.text)
