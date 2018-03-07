
from flask import render_template,Flask,request,url_for,redirect
import requests,json
# from flask import jsonify
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/aadhar', methods=['POST','GET'])
def aadhar():
    if request.method == 'POST':
        aadhar=request.Form['aadhar']
        name = request.Form['name']
        mobile = request.Form['mobile']
        email = request.Form['email']
        if len(aadhar) != 12:
            return render_template('aadhar.html',message="aadhar Number must be of 12 digit",aadhar=aadhar,name=name,mobile=mobile,email=email)

        if len(mobile) != 10 and mobile!="NULL":
            return render_template('aadhar.html',message="Mobile Number must be of 12 digit",aadhar=aadhar,name=name,mobile=mobile,email=email)
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "Aadhar",
                "objects": [
                    {
                        "mobile": mobile,
                        "email": email,
                        "aadhar_no": aadhar,
                        "name": name
                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        if 'affected_rows' in resp.json()==1:
            return redirect(url_for('aadhar'))
        elif resp.json()['code'] == 'postgres-error':
            return render_template('aadhar.html', message="Error plzz contact MANISH(7297899599)",aadhar=aadhar,mobile=mobile,email=email,name=name)
        else:
            return render_template('aadhar.html', message="Duplicate aadhar",aadhar=aadhar,mobile=mobile,email=email,name=name)

    return render_template('aadhar.html', message="successfull entry Done")
@app.route('/template2')
def template2():
    return render_template('template2.html')

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
