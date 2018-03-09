import json,requests

aadhar='476894302171'
if len(aadhar) != 12:
    print "2"
url = "https://data.despairing12.hasura-app.io/v1/query"

# This is the json payload for the query
requestPayload = {
    "type": "select",
    "args": {
        "table": "Aadhar",
        "columns": ["mobile"],
        "where": {
            "aadhar_no": {
                "$eq": aadhar
            }
        }
    }
}

# Setting headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
}

# Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

if len(resp.json())==0:
    print "no"
else:
    print resp.json()
