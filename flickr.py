import flickrapi
import json

from photoService import PhotoService

class Flickr(PhotoService):

    def __init__(self):
        self.CLIENT_ID = '2581fe0b520e995090db8d4f5066a218'
        self.CLIENT_SECRET = '6e6a44356e9bd34d'

        self.flickr = flickrapi.FlickrAPI(self.CLIENT_ID, secret=self.CLIENT_SECRET)
        self.photo_set = []

    def photo_lookup(self, tag_set, tags_intersect=False):

        if tags_intersect:
            tag_mode = "all"
        else:
            tag_mode = "any"
        self.photo_set = self.flickr.walk(tag_mode=tag_mode, tags=tag_set)

        return 1

    #todo make this a generator
    def get_next_photo(self):

        data={}
        for photo in self.photo_set:
            data['title'] = photo.get('title')
            data['url'] = self.getFlickrURL( self.flickr.photos.getInfo(photo_id=photo.get('id'),  format='json').decode("utf-8"))

            return data

    def getFlickrURL(self, imageJSON):
        photo = json.loads(imageJSON)['photo']

        farm_id = photo['farm']
        server_id = photo['server']
        photo_id = photo['id']
        photo_secret = photo['secret']

        url = 'https://farm{farmid}.staticflickr.com/{serverid}/{id}_{secret}_h.jpg'.format(farmid=farm_id,
                                                                                                 serverid=server_id,
                                                                                                 id=photo_id,
                                                                                                 secret=photo_secret)
        return (url)

