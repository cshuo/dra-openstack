__author__ = 'pike'

from oslo_config import cfg
from dra.Hades import Config
from dra.Hades import BaseRpcApi

CONF =  cfg.CONF


#base class for PMAAPI
class PMAAPI(BaseRpcApi.BaseAPI):
    def __init__(self, topic, exchange):
        super(PMAAPI, self).__init__(topic, exchange)

    ##################### POLICY #######################
    def loadPolicy(self, ctxt, host, policy):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'loadPolicy',
                   host = host, policy = policy)

    ##################### EVENT #######################
    def handleEvent(self, ctxt, host, event):
        cctxt = self.client.prepare(server = host)
        cctxt.cast(ctxt, 'handleEvent', host = host, event = event)

    def handleEventWithResult(self, ctxt, host, event):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'handleEventWithResult', host = host, event = event)


class ArbiterPMAAPI(PMAAPI):

    def __init__(self, topic, exchange):
        super(ArbiterPMAAPI, self).__init__(topic, exchange)

class MonitorPMAAPI(PMAAPI):
    def __init__(self, topic, exchange):
        super(MonitorPMAAPI, self).__init__(topic, exchange)



if __name__ == "__main__":
    print 'arbiterPMA rpcapi\n'
    api = ArbiterPMAAPI(CONF.hades_arbiterPMA_topic, CONF.hades_exchange)
    print api.handleEvent({}, 'pike', {'fact' : '(animal-is duck)'})
