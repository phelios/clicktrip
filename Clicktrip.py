from bottle import route, run, template
import flickrapi
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