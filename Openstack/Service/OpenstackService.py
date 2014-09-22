__author__ = 'pike'

from Openstack.Service.Keystone import *

from Openstack.Conf.OpenstackConf import AUTH_URL


class OpenstackService:


    def __init__(self):

        # get the authentication token and tenant id

        au = Authentication()
        au.tokenGet(AUTH_URL, "admin", "admin", "ADMIN_PASS")

        self.tenantId = au.getTenantId()
        self.tokenId = au.getTokenId()



if __name__=="__main__":pass