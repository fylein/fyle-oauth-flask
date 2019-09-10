import json
import os

import requests
from flask import render_template, redirect, url_for, request
from fylesdk import FyleSDK

from FlaskApp import app
from FlaskApp.connectors.fyle import FyleConnector

# Necessary URLs and Client Id and Client Secret
REDIRECT_URI = os.environ.get("REDIRECT_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BASE_URL = os.environ.get("BASE_URL")
AUTHORIZE_URL = "{0}/app/main/#/oauth/authorize?client_id={1}&redirect_uri={2}&response_type=code&state=ajsfbjak".format(
    BASE_URL, CLIENT_ID, REDIRECT_URI)
TOKEN_URL = '{0}/api/oauth/token'.format(BASE_URL)


# Index/home page
@app.route('/')
@app.route('/login')
def login():
    error = None
    return render_template('welcome.html', error=error)


# Make authorization
@app.route('/authorize', methods=['POST'])
def authorize():
    return redirect(AUTHORIZE_URL, code=302)


'''Displaying Employee profile details 
   If User allow to fetch Employee profile details We will get Code,error will be null
   If User deny to fetch Employee profile details We will get an error(access denied ) , Code will be null
   If User deny to fetch Employee profile details , He/She will be redirected to Home page(welcome.html) '''


@app.route('/profile', methods=['GET'])
def profile():
    global CLIENT_SECRET
    global CLIENT_ID
    error = None
    error = request.args.get('error')
    code = request.args.get('code')
    if code:
        json_response = requests.post(TOKEN_URL, data={"grant_type": "authorization_code",
                                                       "client_id": CLIENT_ID,
                                                       "client_secret": CLIENT_SECRET,
                                                       "code": code})
        data = json.loads(json_response.text)
        refresh_token = data.get("refresh_token")
        fyle_connection = FyleConnector(refresh_token)
        emp_details = fyle_connection.get_employee_details()
        return render_template('profile.html', emp_data=emp_details)
    return redirect(url_for('login'))
