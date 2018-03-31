import json,requests
url = "https://notify.despairing12.hasura-app.io/v1/send/sms"

# This is the json payload for the query
requestPayload = {
        "to": "7297899599",
        "countryCode": "91",
        "message":"Demo OTP"
}

    # Setting headers
headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
}

    # Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
print resp.content