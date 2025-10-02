import requests

url = "https://www.immobiliare.it/api-next/search-list/real-estates?fkRegione=liguria&fkProvincia=GE&criterio=rilevanza&pag=1"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

resp = requests.get(url, headers=headers)
data = resp.json()

for item in data.get("results", []):  # key may differ
    lat = item.get("latitude")
    lng = item.get("longitude")
    title = item.get("title")
    price = item.get("price", {}).get("value")
    print(title, price, lat, lng)
