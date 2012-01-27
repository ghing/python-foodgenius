python-foodgenius
=================

Installing the library and connecting to the API
""""""""""""""""""""""""""""""""""""""""""""""""

The foodgenius API client library can be installed from GitHub using pip

.. code-block:: bash

    $ pip install git+git://github.com/ecooper/nap.git
    $ pip install git+git://github.com/foodgenius/python-foodgenius.git

Once the library is installed, you can instantiate an API resource object
that will let you connect to and interact with the API.

.. code-block:: python

    >>> from foodgenius import Api
    >>> api = Api(authentication={'key': 'YOUR_API_OAUTH_KEY', 'secret': 'YOU_API_OAUTH_SECRET'})

Find places and menus
"""""""""""""""""""""

.. code-block:: python

    >>> (headers, response) = api.places.near('60622').get()
    >>> location = response['locations'][7]
    >>> import pprint
    >>> pprint.pprint(location)
    {u'id': u'a165efa0-94f8-490c-bbf5-60e1aa4842b9',
     u'phone': u'(773) 384-6537',
     u'place': {u'city': u'Chicago',
                u'coords': {u'coordinates': [41.902376, -87.667494],
                            u'type': u'Point'},
                u'country': u'US',
                u'neighborhoods': [u'Wicker Park', u'West Town'],
                u'state': u'IL',
                u'street': u'1132 N Ashland Ave',
                u'street_cont': u'',
                u'zipcode': u'60622'},
     u'restaurant': {u'id': u'757d3ecb-a3bd-4448-90e5-340d5f986635',
                     u'name': u'La Pasadita'}}
    >>> (headers, response) = api.menus(location['id']).get(q='veggie')
    >>> menu_item = response['menu_items'][0]
    >>> pprint.pprint(menu_item)
    {u'description': u'',
     u'id': u'cfc8aa37-0cba-4415-b7db-ea38fd667778',
     u'name': u'Veggie Burrito',
     u'price': 4.95}

Getting suggestions
"""""""""""""""""""

Menu items are suggested on a per-user basis, so you'll first need to create
a profile for your app's users::

.. code-block:: python

    >>> user_id = '12345'
    >>> api.tastes.profile.post({'identity': user_id})

A user's taste profile gets seeded by rating menu items::

.. code-block:: python

    >>> api.tastes.interactions(user_id).menus.post({'id': menu_item['id'], 'rating': 7.5, 'range': 10.0})

And the API can then offer personalized suggestions::

.. code-block:: python

    >>> (headers, response) = api.tastes.explore(user_id).near('il', 'chicago', 'logan square').get()
    >>> suggested_menu_item = response['menu_items'][1]
    >>> pprint.pprint(suggested_menu_item)
    {u'description': u'"the wild thing" puerto rican style steak sandwich served on two slices of fried green plantains with caramelized onions lettuce, tomato and mayonnaise.',
     u'id': u'71d6cf22-0a46-4ac6-8140-3e7d374ab8f5',
     u'location': {u'id': u'22b0ab81-a6af-4379-87e9-88d3b0da7a00',
                   u'phone': u'(773) 772-2822',
                   u'place': {u'city': u'Chicago',
                              u'coords': {u'coordinates': [41.917258,
                                                           -87.719539],
                                          u'type': u'Point'},
                              u'country': u'US',
                              u'neighborhoods': [u'Logan Square'],
                              u'state': u'IL',
                              u'street': u'3706 W Armitage Ave',
                              u'street_cont': u'',
                              u'zipcode': u'60647'},
                   u'restaurant': {u'id': u'4749673c-353b-44ab-9099-05df1fa31f0f',
                                   u'name': u"Laguardia's Cuban Bistro"}},
     u'name': u'Jibarito Steak Sandwich',
     u'price': 7.9}

