__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.Scheduler import Api
from Hades.Scheduler import RpcApi

CONF = cfg.CONF


class SchedulerManager(Manager.Manager):

    target = messaging.Target(version = '3.34')

    def __init__(self, *args, **kwargs):
        self.scheduler_rpcapi = RpcApi.SchedulerAPI()
        super(SchedulerManager, self).__init__(service_name = 'hades_scheduler_service',
                                               *args,
                                               **kwargs)

    def testSchedule(self, ctxt, host, arg):
        print "manager: testScheduler\n"
        return "manager: testScheduler\n"