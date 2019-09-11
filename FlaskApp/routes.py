import json
import os

import requests
from flask import render_template, redirect, url_for, request
from fylesdk import FyleSDK

from FlaskApp import app
from FlaskApp.connectors.fyle import FyleConnector

# Necessary URLs and Client Id and Client Secret
REDIRECT_URI ="http://localhost:8080/refresh_token"
REFRESH_TOKEN=""
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BASE_URL = os.environ.get("BASE_URL")
AUTHORIZE_URL = "{0}/app/main/#/oauth/authorize?client_id={1}&redirect_uri={2}&response_type=code&state=ajsfbjak".format(
    BASE_URL, CLIENT_ID, REDIRECT_URI)
TOKEN_URL = '{0}/api/oauth/token'.format(BASE_URL)


# Index/home page
#Login page 
@app.route('/')
@app.route('/login',methods=['GET'])
def login():
    error = None
    return render_template('welcome.html', error=error)


#Make authorization
@app.route('/login',methods=['POST'])
def authorize():
    return redirect(AUTHORIZE_URL, code=302)


#Logout endpoint 
@app.route('/logout',methods=['POST'])
def logout():
     global REFRESH_TOKEN
     if request.method == 'POST':
        REFRESH_TOKEN=""
     return redirect(url_for('login'))



'''Displaying Employee profile details 
   If User allow to fetch Employee profile details We will get Code,error will be null
   If User deny to fetch Employee profile details We will get an error(access denied ) , Code will be null
   If User deny to fetch Employee profile details , He/She will be redirected to Home page(welcome.html) '''


@app.route('/profile', methods=['GET'])
def profile():
    global REFRESH_TOKEN
    if REFRESH_TOKEN:
        fyle_connection = FyleConnector(REFRESH_TOKEN)
        emp_details = fyle_connection.get_employee_details()
        return render_template('profile.html', emp_data=emp_details)
    return redirect(url_for('login'))

# To get Refresh Token 
@app.route('/refresh_token',methods=['GET'])
def get_refresh_token():
    global CLIENT_SECRET
    global REFRESH_TOKEN
    global CLIENT_ID
    error = None
    code = None 
    error = request.args.get('error')
    code = request.args.get('code')
    if code:
        json_response = requests.post(TOKEN_URL, data={"grant_type": "authorization_code",
                                                       "client_id": CLIENT_ID,
                                                       "client_secret": CLIENT_SECRET,
                                                       "code": code})
        data = json.loads(json_response.text)
        REFRESH_TOKEN = data.get("refresh_token")
    return redirect(url_for('profile'))


    
