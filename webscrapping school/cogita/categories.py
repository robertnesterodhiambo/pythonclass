import requests

url = "https://api.qogita.com/categories/"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)
