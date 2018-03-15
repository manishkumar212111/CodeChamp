
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
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
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
            "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
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
