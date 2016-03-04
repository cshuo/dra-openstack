__author__ = 'pike'

from Hades import Manager
import oslo_messaging as messaging
from oslo_config import cfg
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
        print "Event recvd is: "
        print event
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

if __name__ == "__main__":
    print CONF.hades_exchange
    CONF.control_exchange = CONF.hades_exchange
    transport = messaging.get_transport(CONF)
    target = messaging.Target(topic=CONF.hades_eventService_topic, server='pike')
    endpoints = [
        EventServiceManager(),
    ]
    server = messaging.get_rpc_server(transport, target, endpoints,
                                      executor='blocking')
    server.start()
    server.wait()
