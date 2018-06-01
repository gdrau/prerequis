# !/usr/bin/env python
#-*- coding:utf8 -*-
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib2
import requests
import base64
import json

from pprint import pprint
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError


import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

### Parametre MicroStrategy ###
api_login = 'administrator'
api_password = ''
api_iserver = '192.168.1.96'
project_id = 'B85DD89411E83A9413360080EF15F2B2'
base_url = "http://192.168.1.96:8080/MicroStrategyLibrary/api/";



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'
    if action == 'congessalarie' :
        authToken, cookies = login(base_url,api_login,api_password)
        datastore=get_report(base_url, authToken, cookies, project_id)
        res = makeWebhookResult(datastore)
        return make_response(jsonify({'fulfillmentText': res}))
    
    
    

#### Recuperation du token MicroStrategy ###
def login(base_url,api_login,api_password):
    base_url = "http://192.168.1.96:8080/MicroStrategyLibrary/api/";
    data_get = { "username": "administrator",
                 "password": "",
                 "loginMode": "1",
                 "maxSearch": "3",
                 "workingSet": 0,
                 "changePassword": "false",
                 "newPassword": "string",
                 "metadataLocale": "en_us",
                 "warehouseDataLocale": "en_us",
                 "displayLocale": "en_us",
                 "messagesLocale": "en_us",
                 "numberLocale": "en_us",
                 "timeZone": "UTC",
                 "applicationType": "35" }
    r = requests.post(base_url + 'auth/login', data=data_get)
    if r.ok:
        authToken = r.headers['X-MSTR-AuthToken']
        cookies = dict(r.cookies)
        #print("Token: " + authToken)
        return authToken, cookies
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

def get_report(base_url, authToken, cookies, project_id):
	base_url2=base_url + "reports/074C4FD647680AD5526DDBB9DBFFFE90/instances?offset=0&limit=1000"
	data_rp={}
        header_rp = {'X-MSTR-AuthToken': authToken,
                     'Accept': 'application/json',
		     'Content-Type': 'application/json',
	             'X-MSTR-ProjectID': project_id}
	r = requests.post(base_url2 , headers=header_rp, data=data_rp, cookies=cookies)
	datast = json.loads(r.content)
	return datast
	
					
		
def processRequest(req):
    if req.get("result").get("action") != "congessalarie":
        return {}
    base_url = "http://192.168.1.96:8080/MicroStrategyLibrary/api/";
    authToken, cookies = login(base_url,api_login,api_password)
    datastore=get_report(base_url, authToken, cookies, project_id)
    res = makeWebhookResult(datastore)
    return res




def makeWebhookResult(datastore):
    lo=len(datastore['result']['data']['root']['children'])		
    for i in range(0,lo,1):
	consultant=datastore['result']['data']['root']['children'][i]['element']['name']
	lo2=len(datastore['result']['data']['root']['children'][i]['children'])
	for j in range(0,lo2,1):
		pole=datastore['result']['data']['root']['children'][i]['children'][j]['element']['name']
		lo3=len(datastore['result']['data']['root']['children'][i]['children'][j]['children'])
		for k in range(0,lo3,1):
			date_debut=datastore['result']['data']['root']['children'][i]['children'][j]['children'][k]['element']['name']		
			lo4=len(datastore['result']['data']['root']['children'][i]['children'][j]['children'][k]['children'])
			for l in range(0,lo4,1):
				date_fin=datastore['result']['data']['root']['children'][i]['children'][j]['children'][k]['children'][l]['element']['name']
				print(consultant +" du pole " + pole + " est absent du " + date_debut + " a "+ date_fin)
	if speech == '': 
		speech = speech + consultant +" du pole " + pole + " est absent du " + date_debut + " a "+ date_fin
	else:
		speech = consultant +" du pole " + pole + " est absent du " + date_debut + " a "+ date_fin
    
	print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apigdr-webhook"
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')