import os
from flask import Flask,render_template,redirect,url_for,request
from fylesdk import FyleSDK
from FlaskApp import app
import json
import requests



# Necessary URLs and Client Id and Client Secret

REDIRECT_URL="http://localhost:8080/profile"
CLIENT_ID= os.environ.get("client_id")
CLIENT_SECRET=os.environ.get("client_secret")
BASE_URL="https://staging.fyle.in/app/main/#/oauth/authorize?"
APP_URL=BASE_URL+"client_id="+CLIENT_ID+"&redirect_uri="+REDIRECT_URL+"&response_type=code&state=ajsfbjak"
ENDPOINT = 'https://staging.fyle.in/api/oauth/token' 

#Home/index route, Only Accepts GET and POST method
#For GET method it redirects home Page (welcome.html)
#For POST method , it redirects APP_URL, with code 302

@app.route('/',methods=['GET','POST'])
@app.route('/home' ,methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return redirect(APP_URL,code =302)
    return render_template('welcome.html', error=error)

'''Displaying Employee profile details 
   If User allow to fetch Employee profile details We will get Code,error will be null
   If User deny to fetch Employee profile details We will get an error(access denied ) , Code will be null
   If User deny to fetch Employee profile details , He/She will be redirected to Home page(welcome.html)
   with reason(s) displying on page '''

@app.route('/profile',methods=['GET'])
def profile():
    global CLIENT_SECRET
    global CLIENT_ID
    error=None
    error=request.args.get('error')
    Code=request.args.get('code')
    if request.method == 'GET' and Code :
        Json_Response=requests.post(ENDPOINT,data={"grant_type": "authorization_code",
                                        "client_id": CLIENT_ID,
                                        "client_secret": CLIENT_SECRET,
                                        "code":Code})
        data=json.loads(Json_Response.text)
        RefreshToken=data.get("refresh_token")
        emp_details=get_profile_details(RefreshToken)
        return render_template('profile.html',emp_data=emp_details)
    return redirect(url_for('login'))



'''Making connection with  FyleSDK
   Fetching the profile details of Employee and returning necessary details  
   base_url for FyleSDK connection is 'https://staging.fyle.in/' '''

def get_profile_details(theRefrshToken):
    global CLIENT_ID
    global CLIENT_SECRET
    connection = FyleSDK(
            base_url=os.environ.get("base_url"),
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=theRefrshToken
        )
    employee_data=connection.Employees.get_my_profile() 
    return employee_data.get('data')



