from flask import Flask,render_template,request
import requests,json

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
            if resp.json()['department']:
                return "Success"
            else:
                return "INcorrect credential"
        except:
            return resp.json()
    return "Get method expected"




