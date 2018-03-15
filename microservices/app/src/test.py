import requests,json

url = "http://127.0.0.1:5000/api/consumer_otp"
#url="https://app.despairing12.hasura-app.io/api/consumer_otp"
# This is the json payload for the query
requestPayload = {
    "data":{
        "OTP":698287,
        "ID":29
    }
 }

# Setting headers
headers = {
        "Content-Type": "application/json",

}

# Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
print resp.content

'''fail={
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

print type(result['data'][0])
'''

