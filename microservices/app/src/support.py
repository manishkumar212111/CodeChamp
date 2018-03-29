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

def TSPDOT_Register(username,password,email):
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
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    if 'affected_rows' in resp.json():
        return True
    else:
        return False

def search(aadhar):
    if len(aadhar) != 12:
        return render_template('support/home.html', error="Aadhar must be 12 digit" + str(aadhar))

    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "central",
            "columns": [
                "mobile",
                "comp_name",
                "LSA"
            ],
            "where": {
                "aadhar_no": {
                    "$eq": aadhar
                }
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    if len(resp.json()) == 0:
            return render_template('support/home.html', search="not found",empty="No record found",aadhar=aadhar,count="Not found")
    else:
            count=len(resp.json())
            if count >8:
                response="The consumer has exhausted total SIM quata allocated"
            return render_template('support/home.html',aadhar=aadhar, response=response,search="found", count=len(resp.json()),res=resp.json())



