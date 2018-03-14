import requests,json

url = "https://app.despairing12.hasura-app.io/aadhar"

# This is the json payload for the query
requestPayload = {
    "data":{
        "aadhar":"875643234312"
    }
 }

# Setting headers
headers = {
        "Content-Type": "application/json",

}

# Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
print resp.content
