import slumber
from slumber import exceptions
import oauth2
import urllib

API_HOST = 'http://50.57.144.113'
API_VERSION = '0.1'

class OAuthResourceAttributesMixin(slumber.ResourceAttributesMixin): 
    """
    A reimplementation of slumber.ResourceAttributesMixin that returns
    an OAuthResource object instead of a ResourceObject
    """

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)

        return OAuthResource(
            base_url=slumber.url_join(self._meta.base_url, item),
            format=self._meta.format,
            authentication=self._meta.authentication,
            append_slash=self._meta.append_slash,
        )

class OAuthResource(slumber.Resource, OAuthResourceAttributesMixin):
    """
    A reimplementation of slumber.Resource that uses OAuth.
    """
    def __init__(self, *args, **kwargs):
        super(slumber.Resource, self).__init__(*args, **kwargs)

        consumer = oauth2.Consumer(self._meta.authentication.get('key'),
            self._meta.authentication.get('secret'))

        self._http = oauth2.Client(consumer)

    def _request(self, method, **kwargs):
        s = self.get_serializer()
        url = self._meta.base_url

        if self._meta.append_slash and not url.endswith("/"):
            url = url + "/"

        if "body" in kwargs:
            body = kwargs.pop("body")
        else:
            # httplib2's request method sets the default body to None, but
            # oauth2's method sets the default to an empty string.  We need
            # to play nice with oauth2
            body = ""

        if kwargs:
            url = "?".join([url, urllib.urlencode(kwargs)])

        # Important: headers need to strictly follow HTTP spec to 
        # work well with oauth2, e.g. "Content-Type", not "content-type"
        resp, content = self._http.request(url, method, body=body, headers={"Content-Type": s.get_content_type()})

        if 400 <= resp.status <= 499:
            raise exceptions.HttpClientError("Client Error %s: %s" % (resp.status, url), response=resp, content=content)
        elif 500 <= resp.status <= 599:
            raise exceptions.HttpServerError("Server Error %s: %s" % (resp.status, url), response=resp, content=content)

        return resp, content

class FoodGenius(slumber.API, OAuthResourceAttributesMixin):
    class Meta:
        base_url = "%s/api/%s/" % (API_HOST, API_VERSION)
        format = "json"

