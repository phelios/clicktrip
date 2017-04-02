from bottle import route, run, template, redirect, request, response
from config import InstagramConfig
import requests
import json

from flickr import Flickr

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/getimage/<location>/<service>')
@route('/getimage/<location>')
def getImage(location, service='flickr'):

    returnJson = {}


    if service == 'flickr':
        ps = Flickr()

    ps.photo_lookup(location)
    photo = ps.get_next_photo()
    print(photo)
    return json.dumps(photo)


@route('/instagram/authenticate')
def authenticate_instagram():

    return redirect(InstagramConfig.AUTHORIZE_API
        .format(
                client_id=InstagramConfig.CLIENT_ID,
                redirect_url=InstagramConfig.REDIRECT_URL))

@route('/instagram/authenticate/callback')
def authenticate_instagram_callback():
    auth_code = request.query['code']

    payload = {
        'client_id': InstagramConfig.CLIENT_ID,
        'client_secret': InstagramConfig.CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': InstagramConfig.REDIRECT_URL,
        'code': auth_code
    }

    r = requests.post(InstagramConfig.ACCESS_TOKEN_API, payload)

    access_token = r.json()['access_token']

    #return InstagramConfig.SEARCH_BY_TAG_API.format(tag='sydney', access_token=access_token)

    r = requests.get(InstagramConfig.SEARCH_BY_TAG_API.format(tag='sydney', access_token=access_token))

    media = r.json()['data']

    images = []
    for item in media:
        images.append(item['images']['standard_resolution']['url'])

    response.content_type = 'application/json'

    return json.dumps(images)




run(host='localhost', port=8080)