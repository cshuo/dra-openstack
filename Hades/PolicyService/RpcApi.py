__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc
from Hades import Config
from Hades import BaseRpcApi


CONF =  cfg.CONF

class PolicyServiceAPI(BaseRpcApi.BaseAPI):

    """
    client side of the policyService rpc API
    """

    def __init__(self, topic, exchange):
        super(PolicyServiceAPI, self).__init__(topic, exchange)


    def loadPolicy(self, ctxt, host, arg):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'loadPolicy',
                   host = host, arg = arg)

if __name__ == "__main__":
    print 'policyService rpcapi\n'

    api = PolicyServiceAPI(CONF.hades_policyService_topic, CONF.hades_exchange)
    print api.loadPolicy({}, 'pike', None)
