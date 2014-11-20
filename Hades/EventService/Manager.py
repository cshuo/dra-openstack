__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.PMA.RpcApi import ArbiterPMAAPI

CONF = cfg.CONF


class EventServiceManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(EventServiceManager, self).__init__(service_name = 'hades_event_service',
                                               *args,
                                               **kwargs)

        self.arbiterPMA = ArbiterPMAAPI(CONF.hades_arbiterPMA_topic, CONF.hades_exchange)

    def sendEvent(self, ctxt, host, pma):
        print "sendEvent"
        if pma == 'arbiterPMA':
            pass
        else:
            pass
