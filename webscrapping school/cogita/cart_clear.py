import requests

QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

def login():
    url = f"{QOGITA_API_URL}/auth/login/"
    resp = requests.post(url, json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD})
    resp.raise_for_status()
    tokens = resp.json()
    print("✅ Logged in successfully")
    return tokens["accessToken"]

def get_active_cart_id(access_token):
    # According to docs, you can use "active" instead of qid when emptying, but
    # if you need the actual qid, you can fetch carts and find the one with qid == activeCartQid
    url = f"{QOGITA_API_URL}/carts/"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    carts = resp.json().get("results", [])

    if not carts:
        print("⚠️ No carts found.")
        return None

    # Option 1: Use the "active" cart via the `active` identifier
    # (Docs allow using "active" directly)
    return "active"

    # Option 2: If you want the actual qid, you can find it in user info or via `activeCartQid`
    # For example, if login returns user info with `activeCartQid`, you could use that.
    # Or look through the carts list if they have an `is_active` flag or similar.

def clear_cart(access_token, cart_identifier):
    # Using the documented POST /carts/{qid}/empty/
    url = f"{QOGITA_API_URL}/carts/{cart_identifier}/empty/"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    resp = requests.post(url, headers=headers, timeout=30)  # add timeout
    if resp.status_code in (200, 204):
        print(f"✅ Cart '{cart_identifier}' cleared successfully.")
    else:
        print(f"❌ Failed to clear cart '{cart_identifier}': {resp.status_code} {resp.text}")

def main():
    token = login()
    cart_id = get_active_cart_id(token)
    if cart_id:
        clear_cart(token, cart_id)

if __name__ == "__main__":
    main()
