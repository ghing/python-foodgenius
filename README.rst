This is a simple client library for Food Genius' `REST API <http://getfoodgenius.com/api/>`_.

Dependencies
============

* oauth2
* ecooper_'s fork_ of slumber_ (see `Installation`_)

.. _ecooper: http://github.com/ecooper/
.. _fork: http://github.com/ecooper/slumber/
.. _slumber: http://slumber.in/

Installation
============

# Need to install ecooper's fork of slumber first, otherwise
# pip will use the one found in PyPI
pip install -e git+git://github.com/ecooper/slumber.git
pip install -e git+git://github.com/foodgenius/python-foodgenius.git

Example
=======

::

    import foodgenius

    # Create the API wrapper object using your OAuth credentials
    api = foodgenius.FoodGenius(authentication={'key': 'your_oauth_key',
        'secret': 'your_oauth_secret'})


    # GET /api/0.1/places/near/60622/
    api.places.near('60622').get()

    # GET /api/0.1/tastes/interactions/justin@getfoodgenius.com/?max_rating=2.0&limit=3
    api.tastes.interactions('justin@getfoodgenius.com').menus.get(max_rating=2.0, limit=3)

    # GET /api/0.1/places/near/il/chicago/
    api.places.near.il('chicago').get()
    # Different semantics for accessing the same resource
    api.places.near('il')('chicago').get()

    # POST /api/0.1/tastes/profile/
    api.tastes.profile.post({"identity": "api@getfoodgenius.com"})
