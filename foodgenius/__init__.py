# TODO: Change this import once ecooper's slumber implementation
# has a finalized name
import slumber as ecooper_slumber
import oauth2

API_DOMAIN = 'getfoodgenius.com'
API_VERSION = '0.1'

class OAuthResource(ecooper_slumber.Resource):
    def _get_client(self):
        consumer = oauth2.Consumer(self._meta.authentication.get('key'),
            self._meta.authentication.get('secret'))

        return self._meta.http(consumer)

    def request(self, method, **kwargs):
        if "body" not in kwargs:
            # httplib2's request method sets the default body to None, but
            # oauth2's method sets the default to an empty string. We need
            # to play nice with oauth2
            kwargs["body"] = ""

        return super(OAuthResource, self).request(method, **kwargs)

def Api(authentication, domain=API_DOMAIN, version=API_VERSION):
    return ecooper_slumber.Api(domain=domain, 
        resource_class=OAuthResource,
        authentication=authentication, 
        uri='/api/' + version + '/',
        http=oauth2.Client)
