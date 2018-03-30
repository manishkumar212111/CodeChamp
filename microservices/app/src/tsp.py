import json,requests
import binascii,base64
from flask import jsonify,render_template
from . import hashing

def login(username, password):

        # Call Data api to compare username and password
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
            "args": {
                "table": "login_ceredential",
                "columns": [
                    "username",
                    "password"
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
            "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
        }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    try:
        # if username or password not match
        if len(resp.json()) == 0:
            return False
        # match
        elif 'username' in resp.json()[0]:
            if hashing.check_password(resp.json()[0]['password'], password):
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def search(aadhar):
    # if aadhar is not 12 digit
    if len(aadhar) != 12:
        return render_template('TSP/home.html', message="Aadhar must be 12 digit" + str(aadhar))
    #call data API
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "count",
        "args": {
            "table": "central",
            "where": {
            "$and": [
                {
                    "aadhar_no": {
                        "$eq": str(aadhar)
                    }
                },
                {
                    "status": {
                        "$eq": "Active"
                    }
                }
            ]
        }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    try:
        #if no detail found
        if resp.json()['count'] == 0:
            return render_template('TSP/home.html', aadhar=aadhar, result="Not found any detail")
        # detail found
        else:
            count = len(resp.json()['count'])
            if count > 8:
                response = "The consumer has exhausted total SIM quata allocated"

            return render_template('TSP/home.html', response=response,aadhar=aadhar, result=resp.json()['count'])
    except:
        return render_template('TSP/home.html', aadhar=aadhar, result=resp.json()['count'])
    return render_template('TSP/home.html', aadhar=aadhar, result="Server busy")
