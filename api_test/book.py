import requests
import json
import datetime
endpoint = "http://localhost:5000/api/book/"
from my_log import log_me
s = requests.Session()

endpoint1 = "http://localhost:5000/api/login/"

response = s.post(endpoint1, json={
    "password": "@@@request23455",
    "email": "mickilyon@outlook.com",
    })



response2 = s.post(endpoint, json={
    'id': "PEOGE",
    'type':'standard',
    'date': f"{datetime.datetime.now().isoformat()}",
    'number_people':1
})
    
print(response2.json())
