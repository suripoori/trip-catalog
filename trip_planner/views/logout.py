__author__ = 'Suraj'


from flask import Blueprint, make_response, flash, redirect, url_for
from flask import session as login_session

import random, string
import json
import requests

mod = Blueprint('login', __name__, url_prefix='/login')

@mod.route('/fbdisconnect')
def fbdisconnect():
    access_token = login_session.get('access_token')
    facebook_id = login_session.get('facebook_id')
    print('In fbdisconnect access token is {}'.format(access_token))
    print('User name is: ')
    print(login_session.get('username'))
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://graph.facebook.com/{}/permissions?access_token={}'.format(facebook_id,access_token)
    print(url)
    result = requests.delete(url).content
    print('result is ')
    print(result)
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@mod.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    print('In gdisconnect access token is {}'.format(access_token))
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(login_session['access_token'])
    result = requests.get(url).content
    print('result is ')
    print(result)
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@mod.route('/disconnect')
def disconnect():
    if 'gplus_id' in login_session:
        gdisconnect()
        del(login_session['gplus_id'])
        del(login_session['credentials'])
    elif 'facebook_id' in login_session:
        fbdisconnect()
        del(login_session['facebook_id'])
    del(login_session['access_token'])
    del(login_session['username'])
    del(login_session['email'])
    del(login_session['picture'])
    del(login_session['user_id'])
    flash("You have successfully been logged out.")
    return redirect(url_for('login.showLogin'), 301)