
from flask import render_template,Flask,request,url_for,redirect,session
import requests,json
import base64
import smtplib
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
import random
from datetime import datetime

# from flask import jsonify
app=Flask(__name__)
app.secret_key = "287tdw8d7we6554rrtrgdweyt26etedgdge45"
#********************************FUNCTION***********************************
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return (base64.urlsafe_b64encode("".join(enc)))
def id_generator(size=11, chars=string.ascii_uppercase+string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))
def email(toaddr, sub, body):
        fromaddr = "t68pf1@gmail.com"
        # toaddr = "manish.kumar212111@gmail.com"
        msg = MIMEMultipart()
        msg[ 'From' ] = fromaddr
        msg[ 'To' ] = toaddr
        msg[ 'Subject' ] = sub

        # body = "Manish here"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "man12345")
        text = msg.as_string()
        resp = server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return True

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
#****************************************************************************
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
        '574375889123'
              '349374082347',
              '456241535623',
              '098675437568',
              '789546235689',
              '456325896144'
              ]
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
                        "time_stamp":json.dumps(datetime.now(), indent=4, sort_keys=True, default=str),
                        "DOI":json.dumps(datetime.now().date(), indent=4, sort_keys=True, default=str),
                        "company_name": "Airtel",
                        "sim_no": sim_no,
                        "mob_no": mob_no,
                        "aadhar":aadhar,
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

@app.route('/TSP1')
def TSP1():
    return render_template('TSP1.html')

@app.route('/Jio',methods=['POST','GET'])
def Jio():
    if request.method=='POST':
        sim_no=request.form['sim_no']
        mob_no=request.form['mobile']
        region=request.form['region']
        aadhar=request.form['aadhar']

        if len(str(sim_no)) !=16:
            return render_template('TSP1.html',message="Sim_no must be of 16 digit")
        if len(str(mob_no)) != 10:
            return render_template('TSP1.html', message="Mob_no must be of 10 digit")
        if len(str(aadhar)) != 12:
            return render_template('TSP1.html', message="aadhar_no must be of 12 digit")
        list=[
              '349374082347',
              '456241535623',
              '098675437568',
              '789546235689',
              '456325896144','234516171215', '789456123451', '234567856789', '254678954624', '123546869545', '345686957612', '543128730487', '856452132512', '789213542167']
        if aadhar not in list:
            return render_template('TSP1.html', message="aadhar_no must be from below list")

        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "TSP1",
                "objects": [
                    {
                        "comp_reg_no": 1001,
                        "time_stamp":json.dumps(datetime.now(), indent=4, sort_keys=True, default=str),
                        "DOI":json.dumps(datetime.now().date(), indent=4, sort_keys=True, default=str),
                        "company_name": "Jio",
                        "sim_no": sim_no,
                        "mob_no": mob_no,
                        "aadhar": aadhar,
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
            return redirect(url_for('Jio'))
        elif 'code' in resp.json():
            return render_template('TSP1.html', message=resp.json()['error'])
        else:

            return render_template('TSP1.html', message="cluster is sleeping wait")

    return render_template('TSP1.html', message="successfull entry Done")

@app.route('/TSP2')
def TSP2():
    return render_template('TSP2.html')

@app.route('/Vodafone',methods=['POST','GET'])
def Vodafone():
    if request.method=='POST':
        sim_no=request.form['sim_no']
        mob_no=request.form['mobile']
        region=request.form['region']
        aadhar=request.form['aadhar']

        if len(str(sim_no)) !=16:
            return render_template('TSP2.html',message="Sim_no must be of 16 digit")
        if len(str(mob_no)) != 10:
            return render_template('TSP2.html', message="Mob_no must be of 10 digit")
        if len(str(aadhar)) != 12:
            return render_template('TSP2.html', message="aadhar_no must be of 12 digit")
        list=[
              '349374082347',
              '456241535623',
              '098675437568',
              '789546235689',
              '456325896144','601809204314', '154645236966', '475689003887', '745216359562', '789546215689', '349374082347', '456241535623', '098675437568', '789546235689', '456325896144']
        if aadhar not in list:
            return render_template('TSP2.html', message="aadhar_no must be from below list")

        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "TSP2",
                "objects": [
                    {
                        "comp_reg_no": 1002,
                        "time_stamp":json.dumps(datetime.now(), indent=4, sort_keys=True, default=str),
                        "DOI":json.dumps(datetime.now().date(), indent=4, sort_keys=True, default=str),
                        "company_name": "Vodafone",
                        "sim_no": sim_no,
                        "mob_no": mob_no,
                        "aadhar": aadhar,
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
            return redirect(url_for('Vodafone'))
        elif 'code' in resp.json():
            return render_template('TSP2.html', message=resp.json()['error'])
        else:

            return render_template('TSP2.html', message="cluster is sleeping wait")

    return render_template('TSP2.html', message="successfull entry Done")

@app.route('/TSP3')
def TSP3():
    return render_template('TSP3.html')

@app.route('/Idea',methods=['POST','GET'])
def Idea():
    if request.method=='POST':
        sim_no=request.form['sim_no']
        mob_no=request.form['mobile']
        region=request.form['region']
        aadhar=request.form['aadhar']

        if len(str(sim_no)) !=16:
            return render_template('TSP3.html',message="Sim_no must be of 16 digit")
        if len(str(mob_no)) != 10:
            return render_template('TSP3.html', message="Mob_no must be of 10 digit")
        if len(str(aadhar)) != 12:
            return render_template('TSP3.html', message="aadhar_no must be of 12 digit")
        list=[
              '349374082347',
              '456241535623',
              '098675437568',
              '789546235689',
              '456325896144','102030405007', '102030405008', '102030405009', '102030405010', '102030405011', '102030405012', '102030405013', '102030405014', '102030405015', '102030405016']
        if aadhar not in list:
            return render_template('TSP3.html', message="aadhar_no must be from below list")

        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "TSP3",
                "objects": [
                    {
                        "comp_reg_no": 1003,
                        "time_stamp":json.dumps(datetime.now(), indent=4, sort_keys=True, default=str),
                        "DOI":json.dumps(datetime.now().date(), indent=4, sort_keys=True, default=str),
                        "company_name": "Idea",
                        "sim_no": sim_no,
                        "mob_no": mob_no,
                        "aadhar": aadhar,
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
            return redirect(url_for('Idea'))
        elif 'code' in resp.json():
            return render_template('TSP3.html', message=resp.json()['error'])
        else:

            return render_template('TSP3.html', message="cluster is sleeping wait")

    return render_template('TSP3.html', message="successfull entry Done")

@app.route('/consumer')
def consumer():
    return render_template('consumer/consumer.html')

@app.route('/consumer/login_otp',methods= ['POST','GET'])
def consumer_login():
    if request.method=='POST':
        random = randint(100000, 999999)
        aadhar=request.form['aadhar']
        if len(aadhar) !=12:
            return render_template('consumer/consumer.html',message="Aadhar number must be of 12 digit")

        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "select",
            "args": {
                "table": "Aadhar",
                "columns": ["mobile"],
                "where": {
                    "aadhar_no": {
                        "$eq": aadhar
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
        if len(resp.json()) == 0:
            return render_template('consumer/consumer.html',message="Not Found")
        try:
            url = "https://notify.despairing12.hasura-app.io/v1/send/sms"

            # This is the json payload for the query
            requestPayload = {
                "to": str(resp.json()[0]['mobile']),
                "countryCode": "91",
                "message": "OTP For Aadhar verification at Shark@JNU is  " +str(random)
            }

            # Setting headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
            }

            # Make the query and store response in resp
            resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

            if 'id' in resp.json():
                session['aadhar']=aadhar
                return render_template('consumer/consumer_otp.html', random=random)
            else:
                return render_template('consumer/consumer.html',message="cluster is sleeping or OTP send limit exceeded"+str(resp.content))

        except IndexError:
            None
        return render_template('consumer/consumer.html', message="error occurs")

@app.route('/consumer/otp/verify',methods=['POST','GET'])
def consumer_otp_verify():
    if request.method=='POST':
        random=request.form['random']
        otp=request.form['otp']

        if len(otp) !=6:
            return render_template('consumer/consumer_otp.html',message="OTP MUST BE OF 6 digit")
        if otp == random:
            if 'aadhar' in session:
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
                                "$eq": session['aadhar']
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

                if len(resp.json()) == 0:
                    return render_template('consumer/consumer_success.html',empty="No record found")
                else:
                    return render_template('consumer/consumer_success.html', result=resp.json(),count=len(resp.json()))
        else:
            return render_template('consumer/consumer_otp.html', message="Plzz enter correct otp"+str(random)+str(otp),random=random)

    return render_template('consumer/consumer_otp.html', message="Error")


@app.route('/register/DOTTSP',methods=['POST','GET'])
def DOTTSP():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        p=id_generator()
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "login_ceredential",
                "objects": [
                    {
                        "username": username,
                        "password": encode(app.secret_key , p)
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
            to=email
            sub="SHARK@JNU LOGIN CEREDENTIAL "
            body="your login ceredential ::  USERNAME:: "+username+ "    Password:: "+p
            email(to,sub,body)
            return "success"
        else:
            resp.content

