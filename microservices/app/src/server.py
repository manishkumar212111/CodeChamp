import binascii
import json
import random
import smtplib
import string
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
import requests
from flask import render_template,Flask,request,url_for,redirect,session,jsonify

from . import tsp
from . import DOT
from . import consumer
from . import TSP_API
#import tsp,consumer,DOT,TSP_API


# from flask import jsonify
app=Flask(__name__)
app.secret_key = "287tdw8d7we6554rrtrgdweyt26etedgdge45"
#********************************FUNCTION***********************************
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

def id_generator(size, chars=string.ascii_uppercase+string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))
def email_send(toaddr, sub, body):
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
def schedule():
    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "delete",
        "args": {
            "table": "temp_otp",
            "where": {}
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule, 'interval', hours=24)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
#****************************************************************************
@app.route('/')
def home():

    return render_template('index.html')
@app.route('/aadhar_entry')
def aadhar_entry():
    return render_template('aadhar.html')

#@app.route('/aadhar', methods=['POST','GET'])
def aadhar1():
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
#*************************************CONSUMER****************************************
# render consumer login template
@app.route('/consumer')
def consumer():
    return render_template('consumer/consumer.html')

@app.route('/consumer/login_otp',methods= ['POST','GET'])
def consumer_login():
    try:
        if session['aadhar']:
            return redirect(url_for('consumer_home'))
    except:
        a=0
    if request.method=='POST':

        aadhar=request.form['aadhar']
        if len(aadhar) !=12:
            return render_template('consumer/consumer.html',message="Aadhar number must be of 12 digit")

        url = "https://app.despairing12.hasura-app.io/api/aadhar"

        # This is the json payload for the query
        requestPayload = {
           "data":
               {
                   "aadhar":aadhar
               }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
         }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        try:
            if 'message' in resp.json()['data']:
                return render_template('consumer/consumer.html',message=resp.json()['data']['message'])
            elif 'ID' in resp.json()['data']:
                session['id'] = resp.json()['data'][0]['ID']
                session['aadhar'] = aadhar
                em=resp.json()['data'][0]['email']
                mob = em[0:5]
                return render_template('consumer/consumer_otp.html', mobile=mob)
            else:
                return render_template('consumer/consumer.html', message=resp.json())
        except:
            return render_template('consumer/consumer.html', message="Unknown error")

    return render_template('consumer/consumer.html', message="error occurs")


@app.route('/consumer/otp/verify',methods=['POST','GET'])
def consumer_otp_verify():
    if request.method=='POST':

        otp=request.form['otp']

        if len(otp) !=6:
            return render_template('consumer/consumer_otp.html',message="OTP MUST BE OF 6 digit")
        url = "https://app.despairing12.hasura-app.io/api/consumer_otp"

        # This is the json payload for the query
        requestPayload = {
            "data":{
                "ID":session['id'],
                "OTP":otp
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        if len(resp.json())==0:
            return render_template('consumer/consumer_otp.html', message="Internal error")
        try:
            if 'message' in resp.json()['data']:
                return render_template('consumer/consumer_otp.html', message="Plzz enter Correct OTP")

            elif 'success' in resp.json()['data']:
                return render_template('consumer/consumer_success.html',empty="No record found")
            else:
                return render_template('consumer/consumer_success.html', result=resp.json(),count=len(resp.json()))
        except:
            return render_template('consumer/consumer_otp.html', message="Plzz enter correct otp")

    return render_template('consumer/consumer_otp.html', message="Error")



def consumer_home():
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

@app.route('/consumer/logout')
def consumer_logout():
    if 'aadhar' in session:
        session.pop('aadhar',None)
        return render_template('index.html',logout="successfully logout")
    return render_template('consumer/consumer.html')

#*****************************************XXXXXXXXXXXXX*********************************
#****************************************TELECOM SERVICE PROVIDER **********************
# show login Page of TSP
@app.route('/login_TSP')
def TSP_LOGIN():
    return render_template('TSP/login.html')

# Login Logic
@app.route('/login/TSP',methods=['POST','GET'])
def login_TSP():
    if request.method=='POST':
        username = request.form['username']
        passowrd = request.form['password']
        #LOGIN TSP BY CALLING LOGIN FUNCTION IN TSP.py

        resp= tsp.login(username, passowrd)

        if resp==False:
            return render_template('TSP/login.html', message="Username password didn't match")
        else:
            session['TSP_username']=username
            return render_template('TSP/home.html',username=username)

    return render_template('TSP/login.html',message="error")

#search result
@app.route('/TSP/search',methods=['POST','GET'])
def tsp_search():
    if request.method== 'POST':
        aadhar=request.form['aadhar']
        return tsp.search(aadhar)

    return render_template('TSP/home.html',result="Unknown error")

#logout
@app.route('/TSP/logout')
def TSp_logout():
    if 'TSP_username' in session:
        session.pop('TSP_username',None)
        return render_template('index.html',logout="successfully logout")
    return render_template('TSP/login.html')

#********************************END*****************************************************

#*********************************DOT****************************************************

# login Page render
@app.route('/login_DOT')
def DOT_login():
    return render_template('DOT/login.html')


# login Logic for DOT
@app.route('/login/DOT',methods=['POST','GET'])
def login_DOT():
    if request.method=='POST':
        username=request.form['username']
        passowrd=request.form['password']
        resp=DOT.login(username,passowrd)
        try:
            if resp==False:
                return render_template('DOT/login/html',message="UserId and password does not match")
            elif resp==True:
                session['DOT_username']=username
                return redirect(url_for('DOT_home'))
            else:
                return render_template('DOT/login.html',"unknown error")
        except:
            return render_template('DOT/login.html',message="Incorrect Username and password")

    return render_template('DOT/login.html',message="error")

# DOT HOME WITH SIM more than 9 and search bar
@app.route('/DOT/home')
def DOT_home():
    try:
        username=session['DOT_username']
        return DOT.home(username)
    except:
        return render_template('DOT/login.html', result="error")


# dot can search
@app.route('/DOT/search',methods=['POST','GET'])
def DOT_search():
    if request.method== 'POST':
        aadhar=request.form['aadhar']
        return DOT.search(aadhar)
    return render_template('DOT/home.html',result="unknown error")
#logout DOT
@app.route('/DOT/logout')
def dot_logout():
    if 'DOT_username' in session:
        session.pop('DOT_username',None)
        return render_template('index.html',logout="successfully logout")
    return render_template('DOT/login.html')



#*******************************END*******************************************************
@app.route('/register/DOTTSP',methods=['POST','GET'])
def DOTTSP():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']

        p=id_generator(11)
        pa=p
        p1=str.encode(p)
        pas=b64encode(p1)
        if pas is False:
            return "error occurs"
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "login_ceredential",
                "objects": [
                    {
                        "username": username,
                        "password": json.dumps(pas.decode('utf-8'))
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
            body="your login ceredential ::  USERNAME:: "+str(username)+ "    Password:: "+str(pa)
            b=email_send(to,sub,body)
            return resp.content
        else:
            return resp.content
    return "okay"

@app.route('/TSP/aadhar_search',methods=['POST','GET'])
def tsp_aadhar_search():
    if request.method=='POST':
        aadhar=request.form['aadhar']
        if len(aadhar) !=12:
            return render_template('TSP/home.html',message="Aadhar number must be of 12 digits")
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "count",
            "args": {
                "table": "central",
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
        if 'count' in resp.json():
            return render_template('/TSP/search.html',aadhar=aadhar,count=resp.json())
        else:
            return render_template('/TSP/home.html',message="Something wrong")


#************************************************ANDROID API *********************************

@app.route('/api/aadhar',methods=['POST','GET'])
def api_aadhar():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))

        # This is the url to which the query is made
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "select",
            "args": {
                "table": "Aadhar",
                "columns": [
                    "aadhar_no",
                    "email"

                ],
                "where": {
                    "aadhar_no": {
                        "$eq": (js['data']['aadhar'])
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
        if 'cluster' in resp.json():
            data = {
                "message": "cluster is sleeping wait for a minute"
            }
            return jsonify(data=data)
        if len(resp.json())==0:
            data={
                "message":"No result found"
            }
            return jsonify(data=data)
        try:
            if len(resp.json()[0]['email']):
                otp=randint(100000,999999)
                em=resp.json()[0]['email']
                mes="SHARK@JNU CONSUMER LOGIN OTP::"+str(otp)
                sub="SHARK@JNU"
                a=email_send(em,sub,mes)
                if a==True:
                    url = "https://data.despairing12.hasura-app.io/v1/query"

                    # This is the json payload for the query
                    requestPayload = {
                        "type": "insert",
                        "args": {
                            "table": "temp_otp",
                            "objects": [
                                {
                                    "OTP": otp,
                                    "aadhar":(js['data']['aadhar'])
                                }
                            ],
                            "returning": [
                                "ID"
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
                    try:
                        if resp.json()['returning'][0]['ID']:
                            id=resp.json()['returning'][0]['ID']
                            data=[
                                {"ID":id },
                               {"email": em}
                            ]


                            return jsonify(data=data)
                        else:
                            data={
                                "message":resp.content
                            }
                            return resp.content
                    except IndexError :
                        data = {
                            "message": "No email found"
                        }
                        return jsonify(data=data)



        except IndexError:
            data = {
                "message": "Uknown error"
            }
            return jsonify(data=data)
    data= {
        "message":"GET METHOD"
    }

    return jsonify(data=data)

@app.route('/api/consumer_otp',methods=['POST','GET'])
def api_consumer_otp():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
        requestPayload = {
        "type": "select",
        "args": {
            "table": "temp_otp",
            "columns": [
                "aadhar"
            ],
            "where": {
                "$and": [
                    {
                        "ID": {
                            "$eq": (js['data']['ID'])
                        }
                    },
                    {
                        "OTP": {
                            "$eq": (js['data']['OTP'])
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
            if len(resp.json())==0:
                data={
                    "message":"invalid OTP"
                }
                return jsonify(data=data)
            if resp.json()[0]['aadhar']:
                url = "https://data.despairing12.hasura-app.io/v1/query"
                requestPayload = {
                    "type": "select",
                    "args": {
                        "table": "central",
                        "columns": [
                            "mobile",
                            "comp_name",
                            "LSA",
                            "aadhar_no"
                        ],
                        "where": {
                            "aadhar_no": {
                                "$eq":resp.json()[0]['aadhar']
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
                resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
                if len(resp1.json())==0:
                    data={
                        "success":"Not Found detail"
                    }
                    return jsonify(data=data)
                else:
                    return resp1.content




        except IndexError:
            data = {
                "message": "Invalid OTP"
            }
            return jsonify(data=data)
    data ={
    "message": "Get method expected"
        }
    return jsonify(data=data)

@app.route('/api/DOT/login',methods=['POST','GET'])
def api_dot_login():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        resp=DOT.login(js['data']['username'],js['data']['password'])
        if resp==True:
            return DOT.api_home()

        else:
            return "false"
    return "Post method required"



@app.route('/api/DOT/search')
def api_dot_search():
    if request.method=='POST':
        content=request.get_json(force=True)
        js=json.loads(json.dumps(content))

        return api_dot_search(js['data']['aadhar'])
#*********************************************************************************************************************


#***************************************************TSP API EXTENDED FEATURE******************************************

@app.route('/api/TSP/status_count',methods=['POST','GET'])
def api_TSP_status_count():
    if request.method=='POST':

        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        aadhar=js['aadhar']
        if len(aadhar) != 12:
            return "Aadhar number is incorrect"
        username=js['username']
        secret_code=js['secret_code']
        return TSP_API.API_STATUS_COUNT(username, secret_code, aadhar)
    return "Get method"

@app.route('/api/TSP/status_count/push_data',methods=['POST','GET'])
def api_TSP_status_count_push_data():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        username=js['username']
        secret_code=js['secret_code']
        aadhar=js['aadhar']
        if len(aadhar) != 12:
            return "Aadhar number is incorrect"
        comp_name=js['comp_name']
        LSA=js['LSA']
        mobile=js['mobile']

        return TSP_API.API_status_count_push(username,secret_code,aadhar,comp_name,LSA,mobile)
    return "get method accepted"


if  __name__ == '__main__':
    app.run(debug=True)