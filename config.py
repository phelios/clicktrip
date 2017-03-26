class InstagramConfig():
    CLIENT_ID = '0d235450749e459d8585c8b7f3fd7a8b'
    CLIENT_SECRET = '9e1aa217a91e480e9088e74bf250a1cd'
    REDIRECT_URL = 'http://localhost:8080/instagram/authenticate/callback'
    AUTHORIZE_API = "https://api.instagram.com/oauth/authorize/?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&scope=public_content"
    ACCESS_TOKEN_API = 'https://api.instagram.com/oauth/access_token'
    SEARCH_BY_TAG_API = 'https://api.instagram.com/v1/tags/{tag}/media/recent?access_token={access_token}'
