from . import hashing
from flask import render_template
import json,requests


def login_support(username,password):
    # This is the url to which the query is made
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
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
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

def TSP_Register(username,password,email):
    pa=hashing.hash_password(password)
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "insert",
        "args": {
            "table": "login_ceredential",
            "objects": [
                {
                    "password": pa,
                    "username": username,
                    "email": email
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
        return True
    else:
        return False


