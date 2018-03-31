import json,requests
import binascii,base64
from . import hashing
from flask import Flask,jsonify,render_template,session

# login DOT
def login(username,password):
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
            if hashing.check_password(resp.json()[0]['password'],password):
                return True
            else:
                return False
        else:
            return False
    except:
        return False



# when DOT logged in go to home page
def home(username):
    url = "https://data.despairing12.hasura-app.io/v1/query"
    # Select aadhar number with their count
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
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    list=[]
    try:
        if len(resp.json()['result'])==1:
            return render_template('DOT/home.html', message="Data not found")

        for i in range(1, len(resp.json()['result'])):
            if int(resp.json()['result'][i][1]) > 9:
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
            "$and": [
                {
                    "aadhar_no": {
                        "$eq": aadhar
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

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    if len(resp.json()) == 0:
            return render_template('DOT/home.html', search="not found",empty="No record found",aadhar=aadhar,count="Not found")
    else:
        count = len(resp.json())
        if count > 9:
            response = "The consumer has exhausted total SIM quota allocated"
            return render_template('DOT/home.html',aadhar=aadhar, response=response,search="found", count=len(resp.json()),res=resp.json())
        return render_template('DOT/home.html', aadhar=aadhar,result=resp.json(), search="found", count=len(resp.json()),res=resp.json())

def mobile_search(mobile):
    # This is the url to which the query is made
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "central",
            "columns": [
                "aadhar_no"
            ],
            "where": {
                "mobile": {
                    "$eq": mobile
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
    return resp.content

#**************************************************ANDROID********************************************************
def api_home():

        url = "https://data.despairing12.hasura-app.io/v1/query"
        # Select aadhar number with their count
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
            "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        list = []
        try:
            if len(resp.json()['result']) == 1:
                return "0"

            for i in range(1, len(resp.json()['result'])):
                if int(resp.json()['result'][i][1]) > 1:
                    list.append([resp.json()['result'][i][0], resp.json()['result'][i][1]])
            data = {

                "list": list

            }
            if len(list) == 0:
                return "0"

            return jsonify(data=data)
        except:
            return "Exception Occured"


def DOT_API_WEB():


    url = "https://data.despairing12.hasura-app.io/v1/query"
        # Select aadhar number with their count
        # This is the json payload for the query
    requestPayload = {
            "type": "run_sql",
            "args": {
                "sql": "SELECT aadhar_no, COUNT(*) FROM central  where status='Active' GROUP BY aadhar_no ORDER BY aadhar_no"
            }
    }

    # Setting headers
    headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    list = []
    try:
        if len(resp.json()['result']) == 1:
            data={"message":"No result found"}
            return jsonify(data=data)

        for i in range(1, len(resp.json()['result'])):
            if int(resp.json()['result'][i][1]) > 8:
                list.append([resp.json()['result'][i][0], resp.json()['result'][i][1]])

        data = {

                "list": list

        }
        if len(list) == 0:
            data = {"message": "No result found"}
            return jsonify(data=data)

        else:
            return jsonify(data=data)
    except:
        data = {"message": "Exception occurred"}
        return jsonify(data=data)


def api_search(aadhar):
    if len(aadhar) != 12:
        return "length of aadhar must be 12 digit"

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
            "$and": [
                {
                    "aadhar_no": {
                        "$eq": aadhar
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

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    try:
        if len(resp.json()) == 0:
            return "not_found"
        elif 'mobile' in resp.json()[0]:
            return resp.content
        else:
            return 'aadhar_error'
    except:
        return "Not found"