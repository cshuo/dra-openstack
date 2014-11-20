__author__ = 'pike'

from oslo.config import cfg
from Hades import Config
from Hades import BaseRpcApi

CONF =  cfg.CONF

#class PMAAPI(BaseRpcApi.BaseAPI):
#    def __init__(self, topic, exchange):
#        super(ArbiterPMAAPI, self).__init__(topic, exchange)
#
#
#    def loadPolicy(self, ctxt, host, arg):
#        cctxt = self.client.prepare(server = host,)
#        return cctxt.call(ctxt, 'loadPolicy',
#                   host = host, arg = arg)

class ArbiterPMAAPI(BaseRpcApi.BaseAPI):


    def __init__(self, topic, exchange):
        super(ArbiterPMAAPI, self).__init__(topic, exchange)


    def loadPolicy(self, ctxt, host, arg):
        cctxt = self.client.prepare(server = host,)
        return cctxt.call(ctxt, 'loadPolicy',
                   host = host, arg = arg)


if __name__ == "__main__":
    print 'arbiterPMA rpcapi\n'
    api = ArbiterPMAAPI(CONF.hades_arbiterPMA_topic, CONF.hades_exchange)
    print api.testArbiterPMA({}, 'pike', None)
