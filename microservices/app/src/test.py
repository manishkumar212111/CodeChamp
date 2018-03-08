import requests
import json
'''# This is the url to which the query is made
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

# resp.content contains the json response.
for i in range(0,10):
    print resp.json()[i]['aadhar_no']
    '''
aadhar='476894302178'
list=[657894032172,869520329845,476894302178]
if int(aadhar) in list:
    print "yes"