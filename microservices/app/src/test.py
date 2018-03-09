import json,requests
from random import randint
print randint(100000, 999999)
aadhar='7297899599'

url = "https://notify.despairing12.hasura-app.io/v1/send/sms"

# This is the json payload for the query
requestPayload = {
         "to": aadhar,
         "countryCode": "91",
        "message": "OTP For Aadhar verification at Shark@JNU is  "
          }
# Setting headers
headers = {           "Content-Type": "application/json",
                "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
            }

            # Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
print resp.content
if 'id' in resp.json():
    print "ok"
else:
    print "no"