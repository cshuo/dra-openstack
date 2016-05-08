# -*- coding: utf-8 -*-

import oslo_messaging as messaging
from oslo_config import cfg

from dra.Hades import Manager
from dra.Hades.Arbiter import RpcApi
from dra.Hades.Arbiter import SchedulePolicy

CONF = cfg.CONF


class ArbiterManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):
        self.arbiter_rpcapi = RpcApi.ArbiterAPI()
        self.schedulePolicy = SchedulePolicy.SchedulePolicy()
        super(ArbiterManager, self).__init__(service_name = 'hades_arbiter_service',
                                               *args,
                                               **kwargs)

    def testArbiter(self, ctxt, arg):
        host = self.schedulePolicy.randomSchedule()
        print "selected host is:", host
        return host
