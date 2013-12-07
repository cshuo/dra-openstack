__author__ = 'pike'
import urllib2
import urllib
import json

class Authentication:


    def __init__(self):

        self.tokenid=None
        self.tenantid=None

    def tokenGet(self,host,tenant,user,password):
        '''
        get authentication token from keystone

        '''

        url="%s%s" % (host,"/v2.0/tokens")
        tokenrequest=urllib2.Request(url)
        tokenrequest.add_header("Content-type", "application/json")
        data=json.dumps({'auth': {'tenantName': tenant, 'passwordCredentials': {'username': user, 'password': password}}})
        request=urllib2.urlopen(tokenrequest, data)
        result=json.loads(request.read())
        request.close()

        self.tokenid=result["access"]["token"]["id"]
        self.tenantid=result["access"]["token"]["tenant"]["id"]

        #print result
        #print result["access"]["token"]["id"]
        #print result["access"]["token"]["tenant"]["id"]

    def getTokenId(self):
        return self.tokenid

    def getTenantId(self):
        return self.tenantid

if __name__=="__main__":

    test=Authentication()
    test.tokenGet("http://114.212.189.132:35357","admin","admin","ADMIN_PASS")

