import requests
import json
endpoint_reg = "http://localhost:5000/api/register/"



reg_response = requests.post(endpoint_reg, json={
    "username": "oopont666dd455",
    "password1": "@@@request23455",
    "email": "mickilyon@outlook.com",
     })

print(reg_response.json())
