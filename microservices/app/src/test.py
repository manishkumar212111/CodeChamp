import json,requests
url = "https://app.despairing12.hasura-app.io/count"
# Select aadhar number with their count
# This is the json payload for the query
requestPayload = {
}

    # Setting headers
headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
}

# Make the query and store response in resp
resp = requests.request("GET", url, data=json.dumps(requestPayload), headers=headers)
print resp.content