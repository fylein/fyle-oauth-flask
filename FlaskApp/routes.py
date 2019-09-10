import json
import os

import requests
from flask import render_template, redirect, url_for, request
from fylesdk import FyleSDK

from FlaskApp import app

# Necessary URLs and Client Id and Client Secret


REDIRECT_URL = os.environ.get("REDIRECT_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BASE_URL = os.environ.get("BASE_URL")
AUTHORIZE_URL = "{0}/app/main/#/oauth/authorize?".format(BASE_URL)
APP_URL = "{0}client_id={1}&redirect_uri={2}&response_type=code&state=ajsfbjak".format(
    AUTHORIZE_URL, CLIENT_ID, REDIRECT_URL)
ENDPOINT = '{0}/api/oauth/token'.format(BASE_URL)


# Home/index route, Only Accepts GET and POST method
# For GET method it redirects home Page (welcome.html)
# For POST method , it redirects APP_URL, with code 302

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return redirect(APP_URL, code=302)
    return render_template('welcome.html', error=error)


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
    if request.method == 'GET' and code:
        json_response = requests.post(ENDPOINT, data={"grant_type": "authorization_code",
                                                      "client_id": CLIENT_ID,
                                                      "client_secret": CLIENT_SECRET,
                                                      "code": code})
        data = json.loads(json_response.text)
        my_refresh_token = data.get("refresh_token")
        emp_details = get_profile_details(my_refresh_token)
        return render_template('profile.html', emp_data=emp_details)
    return redirect(url_for('login'))


'''Making connection with  FyleSDK
   Fetching the profile details of Employee and returning necessary details  
   base_url for FyleSDK connection is 'https://staging.fyle.in/' '''


def get_profile_details(the_refrsh_token):
    global CLIENT_ID
    global CLIENT_SECRET
    global BASE_URL
    connection = FyleSDK(
        base_url=BASE_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=the_refrsh_token
    )
    employee_data = connection.Employees.get_my_profile()
    return employee_data.get('data')
