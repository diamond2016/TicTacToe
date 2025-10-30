import requests
import json
API_URL= "https://localhost:8080/update_game"
matrix = {"row": 0, "col": 0, "value": 'X'}
headers =  {"Content-Type":"application/json"}
response = requests.post(API_URL, data=json.dumps(matrix), headers=headers)
print(response.json())
print(response.status_code)