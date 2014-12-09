__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.PMA.RpcApi import ArbiterPMAAPI
from Hades.PMA.RpcApi import MonitorPMAAPI

CONF = cfg.CONF


class EventServiceManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(EventServiceManager, self).__init__(service_name = 'hades_event_service',
                                               *args,
                                               **kwargs)

        self.arbiterPMA = ArbiterPMAAPI(CONF.hades_arbiterPMA_topic, CONF.hades_exchange)
        self.monitorPMA = MonitorPMAAPI(CONF.hades_monitorPMA_topic, CONF.hades_exchange)

    def sendEvent(self, ctxt, host, pma, event):
        print "sendEvent"
        if pma == 'arbiterPMA':
            self.arbiterPMA.handleEvent({}, 'pike', event)
        elif pma == 'monitorPMA':
            self.monitorPMA.handleEvent({}, 'pike', event)


    def sendEventForResult(self, ctxt, host, pma, event):
        print "sendEventForResult"
        if pma == 'arbiterPMA':
            return self.arbiterPMA.handleEventWithResult({}, 'pike', event)
        elif pma == 'monitorPMA':
            return self.monitorPMA.handleEventWithResult({}, 'pike', event)
        else:
            return False
