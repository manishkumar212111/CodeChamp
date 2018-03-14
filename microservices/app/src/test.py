import requests,json

url = "http://127.0.0.1:5000/aadhar"

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
'''
fail={
  "data": {
    "message": "No result found"
  }
}

result={
  "data": [
    {
      "ID": 28
    },
    {
      "email": "manish.kumar212111@gmail.com"
    }
  ]
}




'''