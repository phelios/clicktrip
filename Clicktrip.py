from bottle import route, run, template, redirect, request, response
from config import InstagramConfig
import requests
import json

from flickr import Flickr
from instagram import Instagram


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/getimage/<location>/<service>')
@route('/getimage/<location>')
def getImage(location, service='flickr'):

    returnJson = {}

    print(" 1. my token is " + request.get_cookie("insta_auth_token"))

    if service == 'flickr':
        ps = Flickr()
    elif service == 'insta':
        ps = Instagram()
    print("2. my token is " + request.get_cookie("insta_auth_token"))

    print("GETTING SHIT")
    ps.photo_lookup(location)
    print(" 3. my token is " + request.get_cookie("insta_auth_token"))
    photo = ps.get_next_photo()
    print(" 4. my token is " + request.get_cookie("insta_auth_token"))
    print(photo)


    return json.dumps(photo)

@route('/instagram/authenticate')
def authenticate_instagram_callback():
    Instagram().auth()

#@route('/instagram/authenticate/callback')
def authenticate_instagram_callback():
    auth_code = request.query['code']

    payload = {
            'client_id':  InstagramConfig.CLIENT_ID,
            'client_secret': InstagramConfig.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': InstagramConfig.REDIRECT_URL,
            'code': auth_code
    }

    r = requests.post(InstagramConfig.ACCESS_TOKEN_API, payload)

    access_token = r.json()['access_token']

        # return InstagramConfig.SEARCH_BY_TAG_API.format(tag='sydney', access_token=access_token)

    r = requests.get(InstagramConfig.SEARCH_BY_TAG_API.format(tag='sydney', access_token=access_token))

    media = r.json()['data']

    images = []
    for item in media:
        images.append(item['images']['standard_resolution']['url'])

    response.content_type = 'application/json'

    return json.dumps(images)


run(host='localhost', port=8080)