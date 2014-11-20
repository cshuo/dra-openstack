__author__ = 'pike'

from oslo.config import cfg
from Hades import Config
from Hades import BaseRpcApi

CONF =  cfg.CONF


#base class for PMAAPI
class PMAAPI(BaseRpcApi.BaseAPI):
    def __init__(self, topic, exchange):
        super(PMAAPI, self).__init__(topic, exchange)


    def loadPolicy(self, ctxt, host, policy):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'loadPolicy',
                   host = host, policy = policy)


class ArbiterPMAAPI(PMAAPI):

    def __init__(self, topic, exchange):
        super(ArbiterPMAAPI, self).__init__(topic, exchange)



if __name__ == "__main__":
    print 'arbiterPMA rpcapi\n'
    api = ArbiterPMAAPI(CONF.hades_arbiterPMA_topic, CONF.hades_exchange)
