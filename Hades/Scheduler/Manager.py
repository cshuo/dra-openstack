__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.EventService.RpcApi import EventServiceAPI

CONF = cfg.CONF


class SchedulerManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(SchedulerManager, self).__init__(service_name = 'hades_scheduler_service',
                                               *args,
                                               **kwargs)
        self.eventServiceApi = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)

    def testSchedule(self, ctxt, host, arg):
        print "customized scheduler"

        host =  self.eventServiceApi.sendEventForResult({}, 'pike', 'arbiterPMA', '(newVM cpubound vmInfo)')
        host = host.strip('\n')
        print host
        return host