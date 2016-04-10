# -*- coding: utf-8 -*-

from .Keystone import *
from ..Conf.OpenstackConf import AUTH_URL
from ...Utils.HttpUtil import OpenstackRestful


class OpenstackService:
    au = Authentication()

    def __init__(self):

        # get the authentication token and tenant id

        self.au.tokenGet(AUTH_URL, "admin", "admin", "cshuo")
        self.tenantId = self.au.getTenantId()
        self.tokenId = self.au.getTokenId()
        self.restful = OpenstackRestful(self.tokenId)
        # self.restful = OpenstackRestful('234j234j234h23g4234bb')

    def update_token(self):
        self.au.tokenGet(AUTH_URL, 'admin', 'admin', 'cshuo')
        self.tokenId = self.au.getTokenId()
        self.tenantId = self.au.getTenantId()
        self.restful.update_token(self.tokenId)


if __name__ == "__main__":
    pass
