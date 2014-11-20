__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc
from Hades import Config
from Hades import BaseRpcApi


CONF =  cfg.CONF

class EventServiceAPI(BaseRpcApi.BaseAPI):



    def __init__(self, topic, exchange):
        super(EventServiceAPI, self).__init__(topic, exchange)


    def sendEvent(self, ctxt, host, pma):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'sendEvent',
                   host = host, pma = pma)

if __name__ == "__main__":
    print 'eventService rpcapi\n'

    api = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
    print api.sendEvent({}, 'pike', "arbiterPMA")
