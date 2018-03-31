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
from flask import flash,render_template,Flask,request,url_for,redirect,session,jsonify

from . import tsp
from . import DOT
from . import consumer
from . import TSP_API
from . import support
#import tsp,consumer,DOT,TSP_API


# from flask import jsonify
app=Flask(__name__)
app.secret_key = "287tdw8d7we6554rrtrgdweyt26etedgdge45"
#ALLOWED_EXTENSIONS = set(['csv'])


#********************************FUNCTION***********************************
#allowed file for upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# generete random code
def id_generator(size, chars=string.ascii_uppercase+string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

#email send  function

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

# scheduled function to delete temp_data for OTP store for every 24 hours
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
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

# To count no of views
'''
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
        '''
#****************************************************************************
# Application Home page
@app.route('/')
def home():
    return render_template('index.html')

# frequently asked question
@app.route('/faqs')
def faqs():
    return render_template('faqs.html')
#*************************************CONSUMER****************************************
# render consumer login template
@app.route('/consumer')
def consumer():

    return render_template('consumer/consumer.html')

#Login Logic for consumer

# Mobile otp Send

def mobile_otp():


    # This is the url to which the query is made
    url = "https://notify.despairing12.hasura-app.io/v1/send/sms"

    # This is the json payload for the query
    requestPayload = {
        "to": "9876543210",
        "countryCode": "917297899599",
        "message": "This is the body of SMS"
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 8cafc32cc39fe0e17b06bd326a2cfbfbf968110117f29767"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)


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
            if 'ID' in resp.json()['data'][0]:
                session['id'] = resp.json()['data'][0]['ID']

                em=resp.json()['data'][1]['email']
                mob = em[0:5]
                return render_template('consumer/consumer_otp.html', mobile=mob,aadhar=aadhar)
            else:
                return render_template('consumer/consumer.html', message="unknown error")
        except:
            return render_template('consumer/consumer.html', message="Unknown exception")

    return render_template('consumer/consumer.html', message="error occurs")

# Verify OTP for consumer throug API calling
@app.route('/consumer/otp/verify',methods=['POST','GET'])
def consumer_otp_verify():
    if request.method=='POST':

        otp=request.form['otp']
        aadhar=request.form['aadhar']
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

        if 'data' in resp.json():
            if 'success' in resp.json()['data']:
                session['aadhar']=aadhar

                return render_template('consumer/consumer_success.html', message="No result found")

            else:
                    return render_template('consumer/consumer_success.html',empty="Plzz enter correct otp")
        else:
            session.pop('id',None)
            session['aadhar'] = aadhar
            count = len(resp.json())
            if count > 9:
                response = "The consumer has exhausted total SIM quota allocated"
                return render_template('consumer/consumer_success.html', result=resp.json(),response=response,count=len(resp.json()))
            return render_template('consumer/consumer_success.html', result=resp.json(),count=len(resp.json()))

    return render_template('consumer/consumer_otp.html', message="Error")


#consumer home with detail
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
                    "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
        }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    if len(resp.json()) == 0:
            return render_template('consumer/consumer_success.html',empty="No record found")
    else:
          return render_template('consumer/consumer_success.html', result=resp.json(),count=len(resp.json()))
# Logout consumer
@app.route('/consumer/logout')
def consumer_logout():
    if 'aadhar' in session:
        session.pop('aadhar',None)
        return render_template('index.html',message="successfully logout")
    return render_template('consumer/consumer.html')

#*****************************************XXXXXXXXXXXXX*********************************
#****************************************TELECOM SERVICE PROVIDER **********************
# show login Page of TSP
@app.route('/login_TSP')
def TSP_LOGIN():
    if 'TSP_username' in session:
       return render_template('TSP/home.html')
    return render_template('TSP/login.html')

# Login Logic
@app.route('/login/TSP',methods=['POST','GET'])
def login_TSP():
    if 'TSP_username' in session:
        return render_template('TSP/home.html')

    if request.method=='POST':
        username = request.form['username']
        passowrd = request.form['password']
        username_new= "TSP_"+username
        #LOGIN TSP BY CALLING LOGIN FUNCTION IN TSP.py

        resp= tsp.login(username_new, passowrd)

        if resp==False:
            return render_template('TSP/login.html', message="Username password didn't match",username=username)
        else:
            session['TSP_username']=username
            return render_template('TSP/home.html',username=username)

    return render_template('TSP/login.html',message="error")

#search result
@app.route('/TSP/search',methods=['POST','GET'])
def tsp_search():
    if 'TSP_username' not in session:
        return render_template('TSP/login.html',message="login First")

    if request.method== 'POST':
        aadhar=request.form['aadhar']
        return tsp.search(aadhar)

    return render_template('TSP/home.html',result="Unknown error")



#logout
@app.route('/TSP/logout')
def TSp_logout():
    if 'TSP_username' in session:
        session.pop('TSP_username',None)
        return render_template('index.html',message="successfully logout")
    return render_template('TSP/login.html')

#********************************END*****************************************************

#*********************************DOT****************************************************

# login Page render
@app.route('/login_DOT')
def DOT_login():
    if 'DOT_username' in session:
        return render_template('DOT/home.html')

    return render_template('DOT/login.html')


# login Logic for DOT
@app.route('/login/DOT',methods=['POST','GET'])
def login_DOT():
    if 'DOT_username' in session:
        return render_template('DOT/home.html')

    if request.method=='POST':
        username=request.form['username']
        passowrd=request.form['password']
        username_new="DOT_"+username
        resp=DOT.login(username_new,passowrd)

        if resp is False :
                return render_template('DOT/login.html',message="UserId and password does not match",username=username)
        elif resp is True:
            session['DOT_username']=username
            return render_template('DOT/home.html')
        else:
            return render_template('DOT/login.html',message="unknown error",username=username)

    return render_template('DOT/login.html',message="error")

# DOT HOME WITH SIM more than 9 and search bar
'''@app.route('/DOT/home',methods=['POST','GET'])
#def DOT_home():
    try:
        username=session['DOT_username']
        return DOT.home(username)
    except:
        return render_template('DOT/login.html', result="error")
'''
@app.route('/DOT/SIM/count', methods=['POST', 'GET'])
def DOT_sim_count():
    return DOT.DOT_API_WEB()


# dot can search
@app.route('/DOT/search',methods=['POST','GET'])
def DOT_search():
    if 'DOT_username' not in session:
        return render_template('DOT/login.html',message="login first")

    if request.method== 'POST':
        aadhar=request.form['aadhar']
        return DOT.search(aadhar)
    return render_template('DOT/home.html',result="unknown error")
#logout DOT
@app.route('/DOT/logout')
def dot_logout():
    session.pop('DOT_username',None)
    return render_template('index.html',message="successfully logout")



#*******************************END*******************************************************

#*******************************SUPPORT***************************************************


@app.route('/support/login',methods=['POST','GET'])
def support_login():
    if 'support_user' in session:
        return render_template('support/home.html')
    return render_template('support/login.html')


@app.route('/login/support',methods=['POST','GET'])
def Support_login_submit():
    if 'support_user' in session:
        return render_template('support/home.html')
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        username_new="SUPP_"+username
        resp= support.login_support(username_new,password)
        try:
            if resp==False:
                return render_template('support/login.html',message="UserId and password does not match")
            elif resp==True:
                session['support_user']=username
                return render_template('support/home.html')
            else:
                return render_template('support/login.html',message="unknown error",username=username)
        except:
            return render_template('support/login.html',message=resp,username=username)


    return render_template('support/login.html',message="Get method expected")

@app.route('/support/search',methods=['POST','GET'])
def support_search():
    if 'support_user' not in session:
        return render_template('support/login.html',message="login first")

    if request.method== 'POST':
        aadhar=request.form['aadhar']
        return support.search(aadhar)
    return render_template('support/home.html',result="unknown error")

@app.route('/view_complain')
def view_complain():
    if 'support_user' not in session:
        return render_template('support/login.html', message="login first")

    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "message",
            "columns": [
                "ID",
                "name",
                "email",
                "message"
            ],
            "order_by": [
                {
                    "column": "ID",
                    "order": "desc"
                }
            ]
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
        if len(resp.json()[0])==0:
            return render_template('support/notification.html',message="No new messages found")
        else:
            return render_template('support/notification.html',value=resp.json())
    except:
        return render_template('support/notification.html', message="no notification found")


@app.route('/support/logout')
def support_logout():
    if 'support_user' not in session:
        return render_template('support/login.html', message="login first")

    session.pop('support_user',None)
    return render_template('index.html',message="Logout Successfully")

@app.route('/TSP/create/account',methods=['POST','GET'])
def TSP_register():
    if 'support_user' not in session:
        return render_template('support/login.html', message="login first")
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password = id_generator(11)

        username_new="TSP_"+username;

        resp=support.TSPDOT_Register(username_new,password,email)
        if resp==True:
            body="Login Ceredential for TSP USERNAME:: "+ username+" Password::"+password
            sub="login ceredential"
            if email_send(email,sub,body):
                return redirect(url_for('TSP_register'))
            else:
                return render_template('support/home.html',login_status="Problem in email sending")
        else:
            return render_template('support/home.html',login_status="Login failed, Check if this username has already been assigned")
    return render_template('support/home.html', login_status="Login ceredential has been sent to provided email")


@app.route('/DOT/create/account',methods=['POST','GET'])
def DOT_register():
    if 'support_user' not in session:
        render_template('support/login.html', message="login first")
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password = id_generator(11)

        username_new="DOT_"+username;

        resp=support.TSPDOT_Register(username_new,password,email)
        if resp==True:
            body="Login Ceredential for DOT USERNAME:: "+ username+" Password::"+password
            sub="login ceredential"
            if email_send(email,sub,body):
                return redirect(url_for('DOT_register'))
            else:
                return render_template('support/home.html',login_status="Problem in email sending")
        else:
            return render_template('support/home.html',login_status="Login failed, Check if this username has already been assigned")
    return render_template('support/home.html', login_status="Login ceredential has been sent to provided email")



#********************************END******************************************************
#********************************Extraaa**************************************************

# To store the messages and complain from user

@app.route('/messages', methods=['POST','GET'])
def messages():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
        # This is the url to which the query is made
        url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "message",
                "objects": [
                    {
                        "email": email,
                        "name": name,
                        "message": message
                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        if 'affected_rows' in resp.json():
            return redirect(url_for('messages'))
        else:
            return render_template('index.html', message="problem with server")

    return render_template('index.html', message="Your Message successfully recorded")

# about section

@app.route('/about_us')
def about_us():
    return render_template('about.html')


#************************************************ANDROID API *********************************
# to validate and send otp code
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
            "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
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
                        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
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

# To validate OTP
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
        "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
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
                    "Authorization": "Bearer 5dd53ad731ff1c7dc1c0b74f14052d66699239d69280bf7a"
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

# DOT will login
@app.route('/api/DOT/login',methods=['POST','GET'])
def api_dot_login():
    if request.method=='POST':
        content = request.get_json(force=True)
        js = json.loads(json.dumps(content))
        username="DOT_"+js['data']['username']
        resp=DOT.login(username,js['data']['password'])
        if resp==True:
            return "true"

        else:
            return "false"
    return "Post method required"


# DOT will search

@app.route('/api/DOT/search',methods=['POST','GET'])
def api_dot_search():
    if request.method=='POST':
        content=request.get_json(force=True)
        js=json.loads(json.dumps(content))

        return DOT.api_search(js['data']['aadhar'])


@app.route('/api/DOT/sim/count',methods=['POST','GET'])
def api_dot_sim_count():
    if request.method=='POST':
        return DOT.api_home()
    return "get method expected"

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



#**************************DOT HOMEAGE**************************



@app.route('/DOT/search/filter', methods=['POST','GET'])
def DOT_search_filter():
    if request.method == 'POST':
        aadhar= request.form['aadhar']
        TSP = request.form['TSP']
        LSA = request.form['LSA']

        # Search for single aadhar
        if aadhar != '00' and TSP=='no' and LSA=='no':
            # search for aadhar only
            url = "https://data.despairing12.hasura-app.io/v1/query"

        # This is the json payload for the query
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
                            "$eq": str(aadhar)
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
                if len(resp.json())==0:
                    return render_template('DOT/home.html',message="No result found")
                return render_template('DOT/home.html',res=resp.json(),count=len(resp.json()),aadhar=aadhar,TSP="ALL",LSA="ALL")
            except:
                return render_template('DOT/home.html', message="exception occured")



        # search for Liscence service area
        elif aadhar =='00' and LSA!='no' and TSP=='no' :
            url = "https://data.despairing12.hasura-app.io/v1/query"

            # This is the json payload for the query
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
                        "LSA": {
                            "$eq": LSA
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
                if len(resp.json())==0:
                    return render_template('DOT/home.html',message="No result found")
                return render_template('DOT/home.html',res=resp.json(),aadhar="All",TSP="ALL",LSA=LSA)
            except:
                return render_template('DOT/home.html', message="exception occured")

        # Search  TSP wise
        elif aadhar == '00' and LSA == 'no' and TSP != 'no':
            url = "https://data.despairing12.hasura-app.io/v1/query"

            # This is the json payload for the query
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
                        "comp_name": {
                            "$eq": TSP
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
                if len(resp.json())==0:
                    return render_template('DOT/home.html',message="No result found")
                return render_template('DOT/home.html',res=resp.json(),aadhar="All",TSP=TSP,LSA="ALL")
            except:
                return render_template('DOT/home.html', message="exception occured")


        # Search for aadhar and TSP
        elif aadhar != '00' and TSP != 'no' and LSA == 'no':
            url = "https://data.despairing12.hasura-app.io/v1/query"

            # This is the json payload for the query
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
                        "$and": [
                            {
                                "aadhar_no": {
                                    "$eq": aadhar
                                }
                            },
                            {
                                "comp_name": {
                                    "$eq": TSP
                                }
                            }
                        ]
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
                if len(resp.json())==0:
                    return render_template('DOT/home.html',message="No result found")
                return render_template('DOT/home.html',res=resp.json(),aadhar=aadhar,TSP=TSP,LSA="ALL")
            except:
                return render_template('DOT/home.html', message="exception occured")


        #Search for Aadhar and LSA
        elif aadhar != '00' and LSA != 'no' and TSP == 'no':
            url = "https://data.despairing12.hasura-app.io/v1/query"

            # This is the json payload for the query
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
                    "$and": [
                        {
                            "aadhar_no": {
                                "$eq": aadhar
                            }
                        },
                        {
                            "LSA": {
                                "$eq": LSA
                            }
                        }
                    ]
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
                if len(resp.json())==0:
                    return render_template('DOT/home.html',message="No result found")
                return render_template('DOT/home.html',res=resp.json(),aadhar=aadhar,TSP=TSP,LSA="ALL")
            except:
                return render_template('DOT/home.html', message="exception occured")


        #Search for LSA and TSP
        elif aadhar == '00' and LSA != 'no' and TSP != 'no':
            url = "https://data.despairing12.hasura-app.io/v1/query"

            # This is the json payload for the query
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
                        "$and": [
                            {
                                "comp_name": {
                                    "$eq": TSP
                                }
                            },
                            {
                                "LSA": {
                                    "$eq": LSA
                                }
                            }
                        ]
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
                if len(resp.json())==0:
                    return render_template('DOT/home.html',message="No result found")
                return render_template('DOT/home.html',res=resp.json(),aadhar="All",TSP=TSP,LSA=LSA)
            except:
                return render_template('DOT/home.html', message="exception occured")

        # Search for Aadhar and TSP and LSA
        elif aadhar!='00' and TSP!='no' and LSA!='no':
            url = "https://data.despairing12.hasura-app.io/v1/query"

            # This is the json payload for the query
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
                        "$and": [
                            {
                                "comp_name": {
                                    "$eq": TSP
                                }
                            },
                            {
                                "$and": [
                                    {
                                        "LSA": {
                                            "$eq": LSA
                                        }
                                    },
                                    {
                                        "aadhar_no": {
                                            "$eq": aadhar
                                        }
                                    }
                                ]
                            }
                        ]
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
                if len(resp.json()) == 0:
                    return render_template('DOT/home.html', message="No result found")
                return render_template('DOT/home.html', res=resp.json(),aadhar=aadhar,TSP=TSP,LSA=LSA)
            except:
                return render_template('DOT/home.html', message="exception occured")



        # Show all detail
        elif aadhar == '00' and TSP == 'no' and LSA == 'no':

            url = "https://data.despairing12.hasura-app.io/v1/query"

            # This is the json payload for the query
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
                    "where": {}
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
                if len(resp.json())==0:
                    return render_template('DOT/home.html',message="No result found")
                return render_template('DOT/home.html',res=resp.json(),aadhar="ALL",TSP="ALL",LSA="ALL")
            except:
                return render_template('DOT/home.html', message="exception occured")
            #return render_template('DOT/search.html', aadhar=aadhar, message="Plzz enter valid data in search field")
    return render_template('DOT/home.html', message="Get method expected")

        #*****************************************************COUNT ***************************************************************

    return render_template('DOT/home.html', message="Getmethod expected")


@app.route('/api/aadhar/TSP')
def api_aadhar_tsp():
    url = "https://data.despairing12.hasura-app.io/v1/query"
    # Select aadhar number with their count
    # This is the json payload for the query
    requestPayload = {
        "type": "run_sql",
        "args": {
            "sql": "SELECT aadhar_no ,\"LSA\",COUNT(*) FROM central  GROUP BY aadhar_no,\"LSA\" ORDER BY aadhar_no"
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
            data = {"message": "No result found"}
            return jsonify(data=data)

        for i in range(1, len(resp.json()['result'])):
            if int(resp.json()['result'][i][2]) > 9:
                list.append([resp.json()['result'][i][0], resp.json()['result'][i][1],resp.json()['result'][i][2]])

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




if  __name__ == '__main__':

    app.run(debug=True)