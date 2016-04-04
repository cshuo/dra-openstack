# -*- coding: utf-8 -*-

from oslo_config import cfg
from ..BaseRpcApi import BaseAPI

CONF = cfg.CONF


class DynamicSchedulerApi(BaseAPI):
    """
    client side of dynamic scheduler rpc api
    """
    def __init__(self, topic, exchange):
        super(DynamicSchedulerApi, self).__init__(topic, exchange)

    def handle_underload(self):
        pass

    def handle_overload(self):
        pass
