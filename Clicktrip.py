from bottle import route, run, template, redirect, request, response
import flickrapi
from config import InstagramConfig
import requests
import json

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/getimage/<location>/<service>')
@route('/getimage/<location>')
def getImage(location, service='flickr'):

    returnJson = {}

    if service == 'flickr':
        flickr = flickrapi.FlickrAPI('2581fe0b520e995090db8d4f5066a218',secret='6e6a44356e9bd34d')
        for photo in flickr.walk(tag_mode='all', tags=location):
            returnJson['title'] = photo.get('title')
            returnJson['url'] = getFlickrURL( flickr.photos.getInfo(photo_id=photo.get('id'),  format='json').decode("utf-8"))
            break

    return returnJson


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


def getFlickrURL(imageJSON):
    q = json.loads( imageJSON)
    j = q['photo']
    for x in j:
        print(x)

    print (json.dumps(j))

    farm_id = j['farm']
    server_id = j['server']
    photo_id = j['id']
    photo_secret = j['secret']

    base_url = 'https://farm{farmid}.staticflickr.com/{serverid}/{id}_{secret}_h.jpg'.format(farmid=farm_id, serverid=server_id, id=photo_id, secret=photo_secret)
    return (base_url)



run(host='localhost', port=8080)