__author__ = 'Suraj'

import json
import os
GOOGLE_CLIENT_ID = json.loads(open('google_client_secrets.json', 'r').read())['web']['client_id']
FB_CLIENT_ID = json.loads(open('fb_client_secrets.json', 'r').read())['web']['client_id']
FB_CLIENT_SECRET = json.loads(open('fb_client_secrets.json', 'r').read())['web']['client_secret']
GOOGLE_CLIENT_SECRETS_LOCATION = os.path.abspath('google_client_secrets.json')
from flask import Flask
app = Flask(__name__)

from trip_planner.views import login
app.register_blueprint(login.mod)