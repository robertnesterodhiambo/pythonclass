import requests

url = "https://api.qogita.com/variants/search/"
headers = {
    "accept": "application/json",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlNjBkMDk3Zi1iZTgxLTQ3YzMtYWZiNS1mMzUzNDA0ZWNlNTEiLCJleHAiOjE3NDE5NzgxNjIsImlhdCI6MTc0MTk3Nzg2MiwiYXVkIjoicW9naXRhOmF1dGg6YWNjZXNzIiwiaXNzIjoicW9naXRhIn0.E8aGxJoc4O9sARiDSSolxKm0RQrmudaU7Djp4BvaR6I"
}

response = requests.get(url, headers=headers)

# Print status code for debugging
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print(response.json())  # If JSON response is expected
else:
    print(f"Error: {response.text}")
