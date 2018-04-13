# !/usr/bin/env python
# -*- coding:utf8 -*-
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

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()


import base64
import json

from pprint import pprint


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
base_url = "http://mon.prerequis.com:2051/MicroStrategyLibrary/api/";



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#### Recuperation du token MicroStrategy ###
def login(base_url,api_login,api_password):
    #print("Obtention token...")
    console.log(base_url)
    data_get = { "username": "administrator",
                 "password": ""}
    r = requests.post(base_url + 'auth/login', data=data_get)
    authToken = r.headers['X-MSTR-AuthToken']
    if r.ok:
        cookies = dict(r.cookies)
        #print("Token: " + authToken)
        return authToken
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))


                    
                    
def processRequest(req):
    if req.get("result").get("action") != "congessalarie":
        return {}
    #authToken = login(base_url,api_login,api_password)
    res=makeWebhookResult()
    return res   

def makeWebhookResult():
    
    speech = "coucou ca va?" 
    
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
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
