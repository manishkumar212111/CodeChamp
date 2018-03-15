import json,requests
import binascii,base64
from flask import jsonify,render_template
def b64encode(s, altchars=None):
   encoded = binascii.b2a_base64(s)[:-1]
   if altchars is not None:
      return (encoded, {'+': altchars[0], '/': altchars[1]})
   return encoded
def b64decode(s, altchars=None):
   if altchars is not None:
      s = (s, {altchars[0]: '+', altchars[1]: '/'})
   try:
      return binascii.a2b_base64(s)
   except:
       return False


def login(username,password):
    p1 = str.encode(password)
    pas = b64encode(p1)

    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "login_ceredential",
            "columns": [
                "username"
            ],
            "where": {
                "$and": [
                    {
                        "username": {
                            "$eq": username
                        }
                    },
                    {
                        "password": {
                            "$eq": json.dumps(pas.decode('utf-8'))
                        }
                    }
                ]
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
        if len(resp.json()) == 0:
            return False
        elif 'cluster' in resp.json():
            return "cluster"
        elif 'username' in resp.json()[0]:

            return True
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
                "aadhar_no": {
                    "$eq": str(aadhar)
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
        #if no detail found
        if resp.json()['count'] == 0:
            return render_template('TSP/home.html', aadhar=aadhar, result="Not found any detail")
        # detail found
        else:
            return render_template('TSP/home.html', aadhar=aadhar, result=resp.json()['count'])
    except:
        return render_template('TSP/home.html', aadhar=aadhar, result="Server busy")
    return render_template('TSP/home.html', aadhar=aadhar, result="Server busy")
