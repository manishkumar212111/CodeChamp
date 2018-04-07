from flask import Flask,render_template,request,jsonify,session
import requests,json
import base64
import datetime
#from geopy.geocoders import GoogleV3
app=Flask(__name__)

app.secret_key = "287tdw8d7we6554rrtrgdweyt26etedgdge45"

def getLocation(lati,longi):
    geocoder = "a"
    location_list = geocoder.reverse((21.1673500, 72.7850900))
    location = location_list[0]
    address = location.address
    return address


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')


@app.route('/Data/Entry')
def data_entry():
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


@app.route('/submit/Data',methods=['POST','GET'])
def submit_data():
    if request.method=='POST':
        p_id=request.form['p_id']
        date=request.form['date']
        address=request.form['address']
        im_id=request.form['im_id']



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
                return render_template('home.html',head=resp.json()[0]['department'])
            else:
                return render_template('login.html',message="Please enter correct email and password")
        except:
            return render_template('login.html', message=resp.content)

    return render_template('login.html', message="POST method expected")


#**********************************android API**********************************

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

