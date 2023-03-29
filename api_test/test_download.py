import requests
import json
s = requests.Session()
ID = None
endpoint = "http://localhost:5000/api/download/ticket/"
response = s.get(endpoint)
resp = response.json()
print(resp)
