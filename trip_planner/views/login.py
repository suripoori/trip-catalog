__author__ = 'Suraj'

from flask import Blueprint, request, make_response, flash, render_template
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from trip_planner.models import session, User
from trip_planner import GOOGLE_CLIENT_ID, FB_CLIENT_ID, FB_CLIENT_SECRET, GOOGLE_CLIENT_SECRETS_LOCATION

import random, string
import json
import requests

mod = Blueprint('login', __name__, url_prefix='/login')

def createUser(login_session):
    newUser = User(user_name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    login_session['user_id'] = user.id
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@mod.route('/')
def showLogin():
    # Create anti forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is {}".format(login_session['state'])
    return render_template('login.html', client_id=GOOGLE_CLIENT_ID, fb_client_id=FB_CLIENT_ID, STATE=state)


# For more details on oauth2 flow with google, visit https://developers.google.com/identity/protocols/OAuth2WebServer
# The implementation below is slightly different
# The ajax portion in the login will call this function
@mod.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    # First check if the state_token of the server when the user clicked login is same as the state_token
    # when the user POSTs. Otherwise, it may be a malicious attack on the server
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps("Invalid state token"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("Verified state token, so it is the same user")
    # The code here is the data sent in the ajax call to this server. It was received from google when the user
    # approved the request
    code = request.data

    try:
        # convert the authorization code into a credential object by talking to the token_uri from client_secrets
        # this object will contain the access token and the refresh token
        oauth_flow = flow_from_clientsecrets(GOOGLE_CLIENT_SECRETS_LOCATION, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        print("Converted auth code to credentials object by talking to the token uri in client secrets")
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Validate access token in the credentials object
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(access_token))
    resp = requests.get(url)
    result = json.loads(resp.content)
    print("Used access token from credentials object to obtain token info from the google apis")
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the access token is used for the right user
    # The sub here is REQUIRED. Subject Identifier. A locally unique and
    # never reassigned identifier within the Issuer for the End-User, which is intended to be consumed by the Client
    # This should be same as the user_id in the result object obtained by querying tokeninfo on googleapis
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user id does not match given user id"), 401)
        response.headers['Content-Type'] = 'application/json'
        return  response
    print("id token in the credentials object matches the user id in the tokeninfo")

    # Verify the access token is valid for the web server
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match the app"), 401)
        response.headers['Content-Type'] = 'application/json'
        return  response
    print("tokeninfo's client id matches the app's client id")

    # Check to see if a user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and stored_gplus_id == gplus_id:
        response = make_response(json.dumps("Current user already connected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return  response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info by passing in the access token
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['access_token'] = access_token
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['user_id'] = getUserID(login_session['email'])

    if login_session['user_id'] is None:
        createUser(login_session)

    print(login_session['user_id'])
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as {}".format(login_session['username']))
    print("done!")
    return output


@mod.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        print("State token is invalid: ")
        print("Expected: {}".format(login_session['state']))
        print("Got: {}".format(request.args.get('state')))
        response = make_response(json.dumps("Invalid state token"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("Verified state token, so it is the same user")
    # The code here is the data sent in the ajax call to this server. It was received from google when the user
    # approved the request
    access_token = request.data
    # Exchange this short lived token for a long lived server side token
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}' \
          '&client_secret={}&fb_exchange_token={}'.format(FB_CLIENT_ID, FB_CLIENT_SECRET, access_token)

    result = requests.get(url).content
    token = result.split("&")[0]

    # Use token to get user info
    userinfo_url = "https://graph.facebook.com/v2.5/me?{}&fields=name,id,email".format(token)
    result = requests.get(userinfo_url).content
    data = json.loads(result)
    print(data)
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    # Retrieve profile pic URL
    pic_url = "https://graph.facebook.com/v2.5/me/picture?{}&redirect=0&height=200&width=200".format(token)
    pic = requests.get(pic_url).json()
    print(pic)
    login_session['picture'] = pic['data']['url']

    login_session['user_id'] = getUserID(login_session['email'])

    if login_session['user_id'] is None:
        createUser(login_session)

    print(login_session['user_id'])
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as {}".format(login_session['username']))
    print("done!")
    return output