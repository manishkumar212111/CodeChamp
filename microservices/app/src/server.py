
from flask import render_template,Flask,request,url_for,redirect
import requests,json
from datetime import datetime
# from flask import jsonify
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/aadhar_entry')
def aadhar_entry():
    return render_template('aadhar.html')

@app.route('/aadhar', methods=['POST','GET'])
def aadhar():
    if request.method == 'POST':
        aadhar=request.form['aadhar']
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']


        if len(aadhar) != 12:
            return render_template('aadhar.html',message="aadhar Number must be of 12 digit",aadhar=aadhar,name=name,mobile=mobile,email=email)
        if len(str(mobile))!=10:
            mobile=0
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
        if 'affected_rows' in resp.json():
            return redirect(url_for('aadhar'))
        elif 'code' in resp.json():
            if resp.json()['error']== 'Uniqueness violation. duplicate key value violates unique constraint \"Aadhar_pkey\"':

                return render_template('aadhar.html', message="Duplicate Aadhar",aadhar=aadhar,mobile=mobile,email=email,name=name)
            else:
                return render_template('aadhar.html', message=resp.json()['error'],aadhar=aadhar,mobile=mobile,email=email,name=name)
        else:
            return render_template('aadhar.html', message="cluster is sleeping wait")

    return render_template('aadhar.html', message="successfull entry Done")
@app.route('/TSP0')
def TSP0():
    return render_template('TSP0.html')

@app.route('/Airtel',methods=['POST','GET'])
def Airtel():
    if request.method=='POST':
        sim_no=request.form['sim_no']
        mob_no=request.form['mobile']
        region=request.form['region']
        aadhar=request.form['aadhar']

        if len(str(sim_no)) !=16:
            return render_template('TSP0.html',message="Sim_no must be of 16 digit")
        if len(str(mob_no)) != 10:
            return render_template('TSP0.html', message="Mob_no must be of 10 digit")
        if len(str(aadhar)) != 12:
            return render_template('TSP0.html', message="aadhar_no must be of 12 digit")
        list=['657894032172',
        '869520329845',
        '476894302178',
        '647389586310',
        '998327908476',
        '895605685890',
        '878779800986',
        '764238947865',
        '789807654324',
        '574375889123']
        if aadhar not in list:
            return render_template('TSP0.html', message="aadhar_no must be from below list")

        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "TSP0",
                "objects": [
                    {
                        "comp_reg_no": 1000,
                        "time_stamp":datetime.now(),
                        "DOI":json.dumps(datetime.now().date(), indent=4, sort_keys=True, default=str),
                        "company_name": "Airtel",
                        "sim_no": sim_no,
                        "mob_no": mob_no,

                        "region": region,
                        "status": "Active"
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
        if 'affected_rows' in resp.json():
            return redirect(url_for('Airtel'))
        elif 'code' in resp.json():
            return render_template('TSP0.html', message=resp.json()['error'])
        else:

            return render_template('TSP0.html', message="cluster is sleeping wait")

    return render_template('TSP0.html', message="successfull entry Done")