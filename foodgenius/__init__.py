# TODO: Change this import once ecooper's slumber implementation
# has a finalized name
import slumber as ecooper_slumber
import oauth2

# TODO: Change this to production server
API_DOMAIN = '50.57.144.113'
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

def Api(authentication):
    return ecooper_slumber.Api(domain=API_DOMAIN, 
        resource_class=OAuthResource,
        authentication=authentication, 
        uri='/api/' + API_VERSION + '/',
        http=oauth2.Client)
