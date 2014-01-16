__author__ = 'pike'

from Authentication import *

from Openstack import AUTHURL,NOVAURL

class OpenstackService:



    def __init__(self):

        # get the authentication token and tenant id

        au=Authentication()
        au.tokenGet(AUTHURL,"admin","admin","ADMIN_PASS")
        self.tenantid=au.getTenantId()
        self.tokenid=au.getTokenId()





if __name__=="__main__":pass