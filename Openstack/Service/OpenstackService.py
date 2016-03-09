__author__ = 'pike'

from dra.Openstack.Service.Keystone import *

from dra.Openstack.Conf.OpenstackConf import AUTH_URL


class OpenstackService:


    def __init__(self):

        # get the authentication token and tenant id

        au = Authentication()
        au.tokenGet(AUTH_URL, "admin", "admin", "cshuo")

        self.tenantId = au.getTenantId()
        self.tokenId = au.getTokenId()



if __name__=="__main__":pass
