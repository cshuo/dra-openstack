__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.Scheduler import RpcApi
from Hades import Config
from Hades.EventService.RpcApi import EventServiceAPI

CONF = cfg.CONF


class SchedulerManager(Manager.Manager):

    target = messaging.Target(version = '3.34')

    def __init__(self, *args, **kwargs):
        self.scheduler_rpcapi = RpcApi.SchedulerAPI()
        super(SchedulerManager, self).__init__(service_name = 'hades_scheduler_service',
                                               *args,
                                               **kwargs)
        self.eventServiceApi = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)

    def testSchedule(self, ctxt, host, arg):

        host =  self.eventServiceApi.sendEventForResult({}, 'pike', 'arbiterPMA', '(newVM cpubound vmInfo)')

        return host