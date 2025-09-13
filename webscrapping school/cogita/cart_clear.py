import requests

QOGITA_API_URL = "https://api.qogita.com"
QOGITA_EMAIL = "jacek.budner@gmail.com"
QOGITA_PASSWORD = "JB100noga!"

def login():
    url = f"{QOGITA_API_URL}/auth/login/"
    resp = requests.post(url, json={"email": QOGITA_EMAIL, "password": QOGITA_PASSWORD})
    resp.raise_for_status()
    tokens = resp.json()
    print("🔎 Login response:", tokens)  # Debugging line
    return tokens


def get_first_cart_id(access_token):
    url = f"{QOGITA_API_URL}/carts/"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    carts = resp.json()

    results = carts.get("results", [])
    if not results:
        print("⚠️ No carts found.")
        return None
    
    cart_id = results[0]["qid"]
    print(f"🛒 Found cart ID: {cart_id}")
    return cart_id

def clear_cart(access_token, cart_id):
    url = f"{QOGITA_API_URL}/carts/{cart_id}/empty/"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.post(url, headers=headers)
    if resp.status_code == 204:
        print(f"✅ Cart {cart_id} cleared successfully.")
    else:
        print(f"❌ Failed to clear cart: {resp.status_code} {resp.text}")

def main():
    token = login()
    cart_id = get_first_cart_id(token)
    if cart_id:
        clear_cart(token, cart_id)

if __name__ == "__main__":
    main()
