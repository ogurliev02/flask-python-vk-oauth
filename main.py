#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, url_for
from vk_urls import *
import private
import requests
import datetime

app = Flask(__name__)


def get_access_token(code):
    params = {
        'client_id': private.CLIENT_ID,
        'client_secret': private.CLIENT_SECRET,
        'redirect_uri': REDIRECT_URL,
        'code': code
    }
    response = requests.get(VK_ACCESS_TOKEN_URL, params=params)
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        return (response_json['access_token'], response_json['expires_in'])
    else:
        return False


def get_friend_list(access_token, friends_count=5):
    params = {
        'access_token': access_token,
        'order': 'random',
        'count': friends_count,
        'fields': 'photo_100,city',
        'version': VK_API_VERSION
    }
    response = requests.get(VK_API_GET_FRIENDS_URL, params=params)
    if response.status_code == 200:
        friends_dict = dict(response.json())['response']
        # get city name by id
        city_ids = ','.join([str(x.get('city', 0)) for x in friends_dict])
        city_name_id = get_city_name_by_id(city_ids)
        for friend in friends_dict:
            if friend.get('deactivated', False):
                friend['city'] = u'Пользователь удален'
                friend['photo_100'] = url_for('static', filename='deactivated.png')
            else:
                friend['city'] = city_name_id[friend['city']]
        return friends_dict
    else:
        return False


def get_user_info(access_token):
    params = {
        'access_token': access_token,
        'fields': 'photo_200_orig',
        'version': VK_API_VERSION
    }
    response = requests.get(VK_API_GET_USER_INFO_URL, params=params)
    if response.status_code == 200:
        return dict(response.json())['response'][0]
    else:
        return False


def get_city_name_by_id(city_ids, lang='ru'):
    params = {
        'access_token': private.CLIENT_SERVISE_KEY,
        'version': VK_API_VERSION,
        'city_ids': city_ids,
        'lang': lang
    }
    response = requests.get(VK_API_GET_CITY_NAME_BY_ID, params=params)
    city_pairs = dict(response.json())['response']
    city_pairs = {x['cid']: x['name'] for x in city_pairs}
    city_pairs[0] = u'Скрыт или не указан'
    return city_pairs


def create_authorize_url():
    session = requests.Session()
    params = {
        'client_id': private.CLIENT_ID,
        'redirect_uri': REDIRECT_URL,
        'version': VK_API_VERSION,
        'scope': 'friends'
    }
    prepared_request = session.get(VK_AUTHORIZE_URL, params=params)
    return prepared_request.url


def get_access_token_from_db(user_id):
    """ Return access token """
    # TODO actually work with db
    return user_id


def set_access_token_to_db(access_token):
    """ Write access token to db, return user_id to write in cookies """
    # TODO actually create user_id and write it to cookies
    # print(hex(random.getrandbits(256)))
    return access_token


@app.route('/')
def index():
    args = dict(request.args)
    if 'user_id' in request.cookies.keys():
        # if user already have authorized, get token from db and return page
        user_id = request.cookies.get('user_id')
        access_token = get_access_token_from_db(user_id)
        friends_list = get_friend_list(access_token)
        user_info = get_user_info(access_token)
        return render_template('index.html', friends_list=friends_list, user_info=user_info)
    # elif 'code' in args:
    #     # if its vk-oauth redirect - write access token to db, redirect to main page
    #     access_token, expires_in = get_access_token(args['code'])
    #     user_id = set_access_token_to_db(access_token)
    #     resp = make_response(redirect('/'))
    #     expires = datetime.datetime.now() + datetime.timedelta(0, int(expires_in))
    #     resp.set_cookie('user_id', user_id, expires=expires)
    #     return resp
    else:
        # redirect to confirm authorize page
        return render_template('enter.html')


@app.route('/authorization')
def authorization():
    # redirect to https://oauth.vk.com/authorize
    authorize_url = create_authorize_url()
    return redirect(authorize_url, code=307)

app.run(debug=True)