__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg

CONF = cfg.CONF


class EventServiceManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(EventServiceManager, self).__init__(service_name = 'hades_event_service',
                                               *args,
                                               **kwargs)


    def sendEvent(self, ctxt, host, pma):
        print "sendEvent"
