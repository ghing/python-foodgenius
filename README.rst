Example
=======

import foodgenius

api = foodgenius.FoodGenius(authentication={'key': 'your_oauth_key',
    'secret': 'your_oauth_secret'})


response_data = api.places.near('60622').get()
response_data = api.tastes.interactions('justin@getfoodgenius.com').menus.get(max_rating=2.0, limit=3)
response_data = api.places.near.il('chicago').get()
response_data = api.places.near.il.chicago('logan%20square').get()
api.tastes.profile.post({"identity": "geoff@terrorware.com"})
