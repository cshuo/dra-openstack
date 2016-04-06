import urllib2
import urllib
import json

class Authentication:


    def __init__(self):

        self.tokenId=None
        self.tenantId=None

    def tokenGet(self, host, tenant, user, password):
        '''
        get authentication token from keystone

        '''

        url = "%s/v2.0/tokens" % host
        tokenRequest = urllib2.Request(url)
        tokenRequest.add_header("Content-type", "application/json")

        data = json.dumps({'auth': {'tenantName': tenant, 'passwordCredentials': {'username': user, 'password': password}}})
        request = urllib2.urlopen(tokenRequest, data)

        result=json.loads(request.read())
        request.close()

        self.tokenId = result["access"]["token"]["id"]
        self.tenantId = result["access"]["token"]["tenant"]["id"]

    def getTokenId(self):
        return self.tokenId

    def getTenantId(self):
        return self.tenantId

if __name__=="__main__":

    auth = Authentication()
    auth.tokenGet("http://20.0.1.11:35357", "admin", "admin", "cshuo")

