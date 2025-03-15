import requests

url = "https://api.qogita.com/brands/"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)
