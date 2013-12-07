__author__ = 'pike'
from Authentication import *

authUrl="http://114.212.189.132:35357"
novaUrl="http://114.212.189.132:8774"

class OpenstackApi:



    def __init__(self):

        # get the authentication token and tenant id

        au=Authentication()
        au.tokenGet(authUrl,"admin","admin","ADMIN_PASS")
        self.tenantid=au.getTenantId()
        self.tokenid=au.getTokenId()



    def getServer(self):
        url="%s/v2/%s/servers" % (novaUrl,self.tenantid)
        print url
        serverRequest=urllib2.Request(url)
        serverRequest.add_header("Content-type","application/json")
        serverRequest.add_header("X-Auth-Token",self.tokenid)
        request=urllib2.urlopen(serverRequest)
        result=json.loads(request.read())
        print len(result["servers"])

if __name__=="__main__":
    test1=OpenstackApi()
    test1.getServer()