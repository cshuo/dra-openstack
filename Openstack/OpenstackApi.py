__author__ = 'pike'

from Authentication import *

from Openstack import AUTHURL,NOVAURL

class OpenstackApi:



    def __init__(self):

        # get the authentication token and tenant id

        au=Authentication()
        au.tokenGet(AUTHURL,"admin","admin","ADMIN_PASS")
        self.tenantid=au.getTenantId()
        self.tokenid=au.getTokenId()



    # get instances that belong to a tenant
    def getInstances(self):
        url="%s/v2/%s/servers" % (NOVAURL,self.tenantid)
        print url
        serverRequest=urllib2.Request(url)
        serverRequest.add_header("Content-type","application/json")
        serverRequest.add_header("X-Auth-Token",self.tokenid)
        request=urllib2.urlopen(serverRequest)
        result=json.loads(request.read())
        print len(result["servers"])

if __name__=="__main__":
    apitest=OpenstackApi()
    apitest.getInstances()