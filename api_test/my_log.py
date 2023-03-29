import requests
import json
s = requests.Session()
ID = None
def log_me():
    endpoint = "http://localhost:5000/api/login/"
    response = s.post(endpoint, json={
        "password": "@@@request23455",
        "email": "mickilyon@outlook.com",
        })

    # print(response.json())
    resp = response.json()
    ID = resp['id']
    print(ID)