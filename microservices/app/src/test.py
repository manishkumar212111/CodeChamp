import requests
import json

# This is the url to which the query is made
url = "https://data.despairing12.hasura-app.io/v1/query"

# This is the json payload for the query
requestPayload={
    "type": "run_sql",
    "args": {
        "sql": "SELECT aadhar_no, COUNT(*) FROM central GROUP BY aadhar_no ORDER BY aadhar_no"
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
for i in range(1,len(resp.json()['result'])):
   if int(resp.json()['result'][i][1]) > 1 :
      list.append([resp.json()['result'][i][0],resp.json()['result'][i][1]])
print list
