import requests
import json
endpoint = "http://localhost:5000/api/hotel-listings/"

ID = None

response = requests.get(endpoint)
    
print(response.json())
resp = response.json()

hotel_id = resp[1]['id']