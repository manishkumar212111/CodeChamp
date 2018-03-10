import json,requests

url = "https://data.despairing12.hasura-app.io/v1/query"

# This is the json payload for the query
requestPayload = {
    "type": "select",
    "args": {
        "table": "central",
        "columns": [
            "mobile",
            "comp_name",
            "LSA"
        ],
        "where": {
            "aadhar_no": {
                "$eq": 875643234312
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

for i in resp.json():
    print i['mobile']



print resp.content