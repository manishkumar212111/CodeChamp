from . import hashing
from . import server

import json,requests


def generete_code(email,username):
    url = "https://data.despairing12.hasura-app.io/v1/query"

    pa = server.id_generator(16)
    hashing.hash_password(pa)
    # This is the json payload for the query
    requestPayload = {
        "type": "insert",
        "args": {
            "table": "API_code",
            "objects": [
                {
                "secret_code": hashing.hash_password(pa),
                "username": username
                }
            ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
        }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    if 'affected_rows' in resp.json():
        sub="TSP Status check API Password"
        to=email
        body="YOUR username NAME AND SECRET CODE ::"+ username+ " TSP0  SECRET_CODE::"+ str(pa)
        server.email_send(to,sub,body)
        return "success"
    else:
        return "error"


def API_STATUS_COUNT(username,secret_code,aadhar):
    if len(aadhar)!=12:
        return "Aadhar number is incorrect"
    url = "https://data.despairing12.hasura-app.io/v1/query"
    requestPayload = {
        "type": "select",
        "args": {
            "table": "API_code",
            "columns": [
                "username",
                "secret_code"
            ],
            "where": {
                "username": {
                    "$eq": username
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
    try:
        if resp.json()[0]['secret_code']:
            secret = resp.json()[0]['secret_code']
        else:
            return "invalid Username"
    except:
        return "Incorrect OTP"

    result = hashing.check_password( secret,secret_code)
    if result==True:

        # This is the json payload for the query
        requestPayload = {
            "type": "count",
            "args": {
                "table": "central",
                "where": {
                    "aadhar_no": {
                        "$eq": aadhar
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
        try:
            if int(resp.json()['count']) >=9:
                return "False"
            else:
                return "True"
        except:
            return "aadhar Not Found"



    else:
        return "incorrect secret code"