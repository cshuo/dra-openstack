# -*- coding: utf-8 -*-

from oslo_config import cfg
from ..BaseRpcApi import BaseAPI

CONF = cfg.CONF

DEFAULT_SERVER = 'pike'


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

    def test(self, ctxt):
        cctxt = self.client.prepare(server=DEFAULT_SERVER)
        print "send arg now..."
        cctxt.cast(ctxt, 'test_sche', arg='cshuo')


if __name__ == '__main__':
    cclient = DynamicSchedulerApi(CONF.hades_scheduler_topic, CONF.hades_exchange)
    # cclient.test({})
    # cclient.handle_underload({}, 'compute2')
    cclient.handle_overload({}, 'compute1', ['83ff087d-c739-45d9-a695-d2c4dea35aff'])

