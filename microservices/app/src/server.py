from flask import Flask,render_template,request,jsonify
import requests,json
import base64

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

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
            if resp.json()[0]['department']:
                return "Success"
            else:
                return "INcorrect credential"
        except:
            return resp.content
    return "Get method expected"








#**********************************android API**********************************

@app.route('/image/upload',methods=['POST','GET'])
def image_upload():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        decoded = base64.b64decode(js['data']['image'])
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "test",
                "objects": [
                    {
                        "Name": js['data']['image'],
                        "ID": "222"
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

        url = "https://filestore.despairing12.hasura-app.io/v1/file"

        # Setting headers
        headers = {
            "Content-Type": "image / png",
            "Authorization": "Bearer bbaa14a4678aa95b48f009258441ea4dd383b90231cbb544"
        }

        # Open the file and make the query
        # with open(file.filename, 'rb') as file_image:
        resp = requests.put(url, data=decoded, headers=headers)

        return resp.content
    return "POST method expected"





