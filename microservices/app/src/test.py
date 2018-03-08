import requests
import json
from datetime import datetime
# This is the url to which the query is made
url = "https://data.despairing12.hasura-app.io/v1/query"

# This is the json payload for the query
requestPayload = {
    "type": "select",
    "args": {
        "table": "Aadhar",
        "columns": [
            "aadhar_no"
        ]
    }
}

# Setting headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
}

# Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
list=[]
# resp.content contains the json response.
for i in range(60,70):
    print resp.json()[i]['aadhar_no']
    list.append(resp.json()[i]['aadhar_no'])

print list

print datetime.now()