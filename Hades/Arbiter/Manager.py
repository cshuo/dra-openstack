__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.Arbiter import Api
from Hades.Arbiter import RpcApi

CONF = cfg.CONF


class ArbiterManager(Manager.Manager):

    target = messaging.Target(version = '3.34')

    def __init__(self, *args, **kwargs):
        self.arbiter_rpcapi = RpcApi.ArbiterAPI()
        super(ArbiterManager, self).__init__(service_name = 'hades_arbiter_service',
                                               *args,
                                               **kwargs)

    def testArbiter(self, ctxt, host, arg):
        print "manager: testArbiter\n"
        return "compute1"