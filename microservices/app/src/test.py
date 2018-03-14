import requests,json

#url = "http://127.0.0.1:5000/aadhar"
url="https://app.despairing12.hasura-app.io/api/aadhar_otp"
# This is the json payload for the query
requestPayload = {
    "data":{
        "aadhar":"875643238312"
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