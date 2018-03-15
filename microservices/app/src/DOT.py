import json,requests
import binascii,base64
from flask import Flask,jsonify,render_template,session
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
        elif 'username' in resp.json()[0]:
            return True
        else:
            return False
    except:
        return False




def home(username):
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "run_sql",
        "args": {
            "sql": "SELECT aadhar_no, COUNT(*) FROM central GROUP BY aadhar_no ORDER BY aadhar_no"
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    list=[]
    try:
        if len(resp.json()['result'])==1:
            return render_template('DOT/home.html', message="Data not found")

        for i in range(1, len(resp.json()['result'])):
            if int(resp.json()['result'][i][1]) > 1:
                list.append([resp.json()['result'][i][0], resp.json()['result'][i][1]])
        data={

        "list":list

        }
        if len(list) ==0:
            return render_template('DOT/home.html', message="Currently no user is using more than 1 sim")

        return render_template('DOT/home.html',result=data)
    except:
        return render_template('DOT/home.html', Message="Error retrieving data")
    return render_template('DOT/home.html', result="error")

def search(aadhar):
    if len(aadhar) != 12:
        return render_template('DOT/home.html', error="Aadhar must be 12 digit" + str(aadhar))

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
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    if len(resp.json()) == 0:
        return render_template('DOT/home.html', search="not found",empty="No record found",aadhar=aadhar,count="Not found")
    else:
        return render_template('DOT/home.html',aadhar=aadhar, search="found", count=len(resp.json()),result1=resp.json())
