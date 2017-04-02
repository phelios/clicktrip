from bottle import route, run, template, redirect, request, response
from config import InstagramConfig
import requests
import json


from photoService import PhotoService

class Instagram(PhotoService):

    CLIENT_ID = '0d235450749e459d8585c8b7f3fd7a8b'
    CLIENT_SECRET = '9e1aa217a91e480e9088e74bf250a1cd'
    REDIRECT_URL = 'http://localhost:8080/instagram/authenticate/callback'
    AUTHORIZE_API = "https://api.instagram.com/oauth/authorize/?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&scope=public_content"
    ACCESS_TOKEN_API = 'https://api.instagram.com/oauth/access_token'
    SEARCH_BY_TAG_API = 'https://api.instagram.com/v1/tags/{tag}/media/recent?access_token={access_token}'

    REDIRECT_URL = 'http://localhost:8080/instagram/authenticate/callback'
    #REDIRECT_URL = "http://localhost:8080//getimage/bali/insta/true"

    def __init__(self):
        self.photo_set = []
        print("checking")


        #self.auth()
        print("leaving const")



    def auth(self):
        print("authing")
        print(request.get_cookie("insta_auth_token"))
        if request.get_cookie("insta_auth_token") is None:
            return redirect(self.AUTHORIZE_API
            .format(
            client_id=self.CLIENT_ID,
            redirect_url=self.REDIRECT_URL))
        else:
            print("i have a thing, its "+ request.get_cookie("insta_auth_token"))

    def photo_lookup(self, tag_set, tags_intersect=False):
        print("my token is " + request.get_cookie("insta_auth_token"))
        r = requests.get(InstagramConfig.SEARCH_BY_TAG_API.format(tag=tag_set, access_token=request.get_cookie("insta_auth_token")))
        print (r.json())
        self.photo_set = r.json()['data']



    def get_next_photo(self):


        data={}
        data['title'] = "photo"
        data['url'] = self.photo_set[0]['images']['standard_resolution']['url']

        return data

@route('/instagram/authenticate/callback')
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

    print("setting")
    response.set_cookie("insta_auth_token", r.json()['access_token'])
    print("moving on")

    for cookie in request.cookies:
        print(cookie)
