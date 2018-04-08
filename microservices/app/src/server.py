from flask import flash,Flask,render_template,request,jsonify,session,redirect,url_for
import requests,json
import base64
import datetime
from geopy.geocoders import GoogleV3
app=Flask(__name__)

app.secret_key = "287tdw8d7we6554rrtrgdweyt26etedgdge45"

# To get Current location of the problem using latitude and longitude
def getLocation(lati,longi):
    geocoder = GoogleV3()
    location_list = geocoder.reverse((21.1673500, 72.7850900))
    location = location_list[0]
    address = location.address
    return address

# App home
@app.route('/')
def index():
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "problem_db",
            "columns": [
                "p_id",
                "p_st",
                "p_category",
                "sub_date",
                "sol_date",
                "address",
                "status"
            ],
            "order_by": [
                {
                    "column": "status",
                    "order": "desc"
                }
            ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)


    return render_template('index.html',res=resp.json())

# Login page for different department
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')


# Data show to admin after login from dummy database of problem statement
@app.route('/Data/Entry',methods=['POST','GET'])
def data_entry():
    if request.method=='POST':
        password=request.form['password']
        if password!='7297':
            return render_template('index.html',value="Incorrect password")

        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "select",
            "args": {
                "table": "problem_dummy",
                "columns": [
                    "p_id",
                    "latitude",
                    "longitude",
                    "im_id",
                    "date"
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        return render_template('DbEntry.html',res=resp.json())

def getlocation(lati,lon):
    return "Sardar Vallabhbhai Engineering College Rd, SVNIT Campus, Athwa, Surat, Gujarat 395007, India"

# Admin can view data from database
@app.route('/view/Data/Entry',methods=['POST','GET'])
def view_data_entry():
    p_id=request.args.get('p_id')
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "problem_dummy",
            "columns": [
                "longitude",
                "latitude",
                "date",
                "im_id",
                "p_id"
            ],
            "where": {
                "p_id": {
                    "$eq": p_id
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    try:
        if resp.json()[0]:
            address=getlocation(resp.json()[0]['latitude'],resp.json()[0]['longitude'])
            return render_template('DataEntryDetail.html', address=address,date=resp.json()[0]['date'],im_id=resp.json()[0]['im_id'],p_id=p_id)
    except:

        address = getlocation(resp.json()[0]['latitude'], resp.json()[0]['longitude'])
        return render_template('DataEntryDetail.html', address=address, date=resp.json()[0]['date'],
                               im_id=resp.json()[0]['im_id'], p_id=p_id)


# move data from dummy to original database
@app.route('/submit/Data',methods=['POST','GET'])
def submit_data():
    if request.method=='POST':
        p_id=request.form['p_id']
        date=request.form['date']
        category=request.form['department']
        p_st=request.form['p_st']
        address=request.form['address']
        im_id=request.form['im_id']
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "problem_db",
                "objects": [
                    {
                        "p_st": p_st,
                        "p_category": category,
                        "sub_date": date,
                        "sol_date": "Not Done yet",
                        "address": getlocation("lati","long"),
                        "status": "pending",
                        "im_id":im_id
                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"

        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        try:
            if resp.json()['affected_rows']:
                url = "https://data.despairing12.hasura-app.io/v1/query"

                # This is the json payload for the query
                requestPayload = {
                "type": "delete",
                "args": {
                    "table": "problem_dummy",
                    "where": {
                        "p_id": {
                        "$eq": p_id
                        }
                    }
                    }
                }

                # Setting headers
                headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
                }

                # Make the query and store response in resp
                resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
                try:
                    if resp.json()['affected_rows']:
                        url = "https://data.despairing12.hasura-app.io/v1/query"

                        # This is the json payload for the query
                        requestPayload = {
                            "type": "select",
                            "args": {
                                "table": "problem_dummy",
                                "columns": [
                                    "p_id",
                                    "latitude",
                                    "longitude",
                                    "im_id",
                                    "date"
                                ]
                            }
                        }

                        # Setting headers
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
                        }

                        # Make the query and store response in resp
                        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

                        return render_template('DbEntry.html', res=resp.json(),value="Value Successfully entered")
                except:
                    return render_template('DbEntry.html', value="Exception occurred1")

        except:
            return render_template('DbEntry.html', value="Exception occurred")

# department login logic

@app.route('/login/department',methods=['POST','GET'])
def login_department():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "select",
            "args": {
                "table": "user_table",
                "columns": [
                    "department"
                ],
                "where": {
                    "$and": [
                        {
                            "email": {
                                "$eq": email
                            }
                        },
                        {
                            "password": {
                                "$eq": password
                            }
                        }
                    ]
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        try:
            if resp.json()[0]:

                response=resp.json()[0]['department']
                if response=='support':
                    return redirect(url_for(''))
                url = "https://data.despairing12.hasura-app.io/v1/query"

                # This is the json payload for the query
                requestPayload = {
                    "type": "select",
                    "args": {
                        "table": "problem_db",
                        "columns": [
                            "p_id",
                            "p_st",
                            "sub_date",
                            "address",
                            "status",
                            "im_id"
                        ],
                        "where": {
                            "p_category": {
                                "$eq": response
                            }
                        }
                    }
                }

                # Setting headers
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
                }

                # Make the query and store response in resp
                resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
                session['user']=response
                return render_template('home.html',res=resp.json(),head=response)


            else:
                return render_template('login.html',message="Please enter correct email and password")
        except:
            return render_template('login.html', message=resp.content)

    return render_template('login.html', message="POST method expected")

# Logout user
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))


# to change status of problem
@app.route('/change/status',methods=['POST','GET'])
def change_status():
    if request.method=='POST':
        p_id=request.form['p_id']
        status=request.form['status']
        department=request.form['department']
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "update",
            "args": {
                "table": "problem_db",
                "where": {
                    "p_id": {
                        "$eq": p_id
                    }
                },
                "$set": {
                    "status": status,
                    "sol_date":json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str)
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        try:
            if resp.json()['affected_rows']:
                url = "https://data.despairing12.hasura-app.io/v1/query"

                # This is the json payload for the query
                requestPayload = {
                    "type": "select",
                    "args": {
                        "table": "problem_db",
                        "columns": [
                            "p_id",
                            "p_st",
                            "sub_date",
                            "sol_date",
                            "address",
                            "status"
                        ],
                        "where": {
                            "p_category": {
                                "$eq": department
                            }
                        }
                    }
                }

                # Setting headers
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
                }

                # Make the query and store response in resp
                resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
                return render_template('home.html',res=resp.json(),value="Status successfully changed",head=department)
        except:
            return render_template('home.html',value="Status successfully changed")

#**********************************android API**********************************

# android API to upload Image
@app.route('/image/upload',methods=['POST','GET'])
def image_upload():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        decoded = base64.b64decode(js['data']['image'])

        image_binary = base64.decodestring(decoded)
        imgdata = base64.b64decode(js['data']['image'])
        filename = 'test.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as file:
            file.write(imgdata)

            # Make the query and store response in resp
            #resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

            url = "https://filestore.despairing12.hasura-app.io/v1/file"

            # Setting headers
            headers = {
                "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
            }

            # Open the file and make the query
            with open('test.jpg', 'rb') as file_image:
                resp = requests.post(url, data=file_image.read(), headers=headers)
                try:
                    data = {
                    "ID":resp.json()['file_id']
                    }
                    return jsonify(data=data)
                except:
                    return "Unable to upload right now, server busy"

            return "Oops , something wrong"

    return "POST method expected"


# Submit problem
@app.route('/problem/submit',methods=['POST','GET'])
def problem_submit():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "problem_dummy",
                "objects": [
                    {
                        "longitude": js['data']['long'],
                        "date": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str),
                        "latitude": js['data']['lat'],
                        "im_id": js['data']['ID'],

                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        return resp.content

        try:
            if resp.json()['affected_rows']:
                data={
                    "message":"success"
                }
                return jsonify(data=data)
            else:
                return resp.content
        except:
            data={
                "error":"Unable to push now"
            }
            return jsonify(data=data)
    return "POST method expected"

@app.route('/raw/problem/submit',methods=['POST','GET'])
def raw_problem_submit():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        # This is the url to which the query is made
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "raw_problem",
                "objects": [
                    {
                        "sub_date": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str),
                        "p_st": js['data']['p_st'],
                        "department": js['data']['department'],
                        "addresss":js['data']['address']
                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        try:
            if resp.json()['affected_rows']:
                data={
                    "message":"success"
                }
                return jsonify(data=data)
        except:
            data = {
                "error": "success"
            }
            return jsonify(data=data)

