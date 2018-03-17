import json,requests
url = "https://app.despairing12.hasura-app.io/api/TSP/status_count/push_data"
requestPayload = {
    "username":"TSP0",
    "aadhar": "875643234312",
    "mobile": "9987674345",
    "comp_name": "Airtel",
    "LSA":"Rajasthan",
    "secret_code":"5VXK8zhs859tCGcf"

}

# Setting headers
headers = {
        "Content-Type": "application/json",
}

# Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
print resp.content