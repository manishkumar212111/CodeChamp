from . import hashing
from flask import Flask,render_template,session
import json,requests
app=Flask(__name__)
app.secret_key="287tdw8d7we6554rrtrgdweyt26etedgdge45"
def login_support(username,password,user):
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
        if len(resp.json()):
            return render_template('support/login.html',message="Username and password mismatched",username=user)
        elif password in resp.json()[0]:
            result=hashing.check_password(resp.json()[0]['password'],password)
            if result==True:
                session['support_user']=user
                render_template('support/home.html')

            else:
                return render_template('support/login.html', message="Username and password mismatched",username=user)

        else:
            return render_template('support/login.html', message="Can't Login this time", username=user)

    except:
        return render_template('support/login.html', message="Exception occured", username=user)


