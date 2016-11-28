# -*-coding: utf-8-*-

import oslo_messaging as messaging
from oslo_config import cfg

from dra.Hades import Manager
from dra.Hades.PMA.RpcApi import ArbiterPMAAPI
from dra.Hades.PMA.RpcApi import MonitorPMAAPI

CONF = cfg.CONF


class EventServiceManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(EventServiceManager, self).__init__(service_name='hades_event_service', *args, **kwargs)

        self.arbiterPMA = ArbiterPMAAPI(CONF.hades_arbiterPMA_topic, CONF.hades_exchange)
        self.monitorPMA = MonitorPMAAPI(CONF.hades_monitorPMA_topic, CONF.hades_exchange)

    def sendEvent(self, ctxt, host, pma, event):
        print "EventManager -> Event recvd is: "
        print event
        if pma == 'arbiterPMA':
            self.arbiterPMA.handleEvent(ctxt, host, event)
        elif pma == 'monitorPMA':
            self.monitorPMA.handleEvent(ctxt, host, event)

    def sendEventForResult(self, ctxt, host, pma, event):
        print "EventManager -> event recvd is: "
        print event
        if pma == 'arbiterPMA':
            return self.arbiterPMA.handleEventWithResult(ctxt, host, event)
        elif pma == 'monitorPMA':
            return self.monitorPMA.handleEventWithResult(ctxt, host, event)
        else:
            return False
 
    def testRpc(self, ctxt, msg):
        print "Message received: ", msg

if __name__ == "__main__":
    pass
