# -*- coding: utf-8 -*-

from oslo_config import cfg
from ..BaseRpcApi import BaseAPI

CONF = cfg.CONF

DEFAULT_SERVER = 'cshuo'


class DynamicSchedulerApi(BaseAPI):
    """
    client side of dynamic scheduler rpc api
    """
    def __init__(self, topic, exchange):
        super(DynamicSchedulerApi, self).__init__(topic, exchange)

    def handle_underload(self, ctxt, host):
        cctxt = self.client.prepare(server=DEFAULT_SERVER)
        # TODO may substitute cast with call to get return info
        cctxt.cast(ctxt, 'handle_underload', host=host)

    def handle_overload(self, ctxt, host, vms):
        cctxt = self.client.prepare(server=DEFAULT_SERVER)
        cctxt.cast(ctxt, 'handle_overload', host=host, vms=vms)


if __name__ == '__main__':
    pass

