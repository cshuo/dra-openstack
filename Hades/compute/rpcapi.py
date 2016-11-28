# -*- coding: utf-8 -*-

from oslo_config import cfg
from ..BaseRpcApi import BaseAPI

CONF = cfg.CONF

DEFAULT_SERVER = "pike"
RPC_TIMEOUT = 1000


class ComputeManagerApi(BaseAPI):
    """
    client side of controller manager
    """
    def __init__(self, topic, exchange, server):
        super(ComputeManagerApi, self).__init__(topic, exchange)
        self.server = server

    
    def res_health_check(self, ctxt):
        cctxt = self.client.prepare(server=self.server, timeout=RPC_TIMEOUT)
        cctxt.cast(ctxt, "res_health_check")
