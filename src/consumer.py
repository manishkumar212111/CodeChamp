
import requests,json
from flask import render_template,Flask,request,url_for,redirect,session,jsonify
from random import randint

def con_login(aadhar):
    if len(aadhar) != 12:
        return "aadhar"

    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "Aadhar",
            "columns": ["mobile"],
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
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    if len(resp.json()) == 0:
        return "not_found"
    try:
        url = "https://notify.despairing12.hasura-app.io/v1/send/sms"
        mobile = str(resp.json()[0]['mobile'])
        random = randint(100000, 999999)
        # This is the json payload for the query
        requestPayload = {
            "to": str(resp.json()[0]['mobile']),
            "countryCode": "91",

            "message": "OTP For Aadhar verification at Shark@JNU is  " + str(random)
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        if 'id' in resp.json():
            session['aadhar'] = aadhar
            mob = mobile[8:10]

            return "sent"
        else:
            return "error"
    except IndexError:
        None
    return render_template('consumer/consumer.html', message="error occurs")
