__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.PolicyService import RpcApi

CONF = cfg.CONF


class PolicyServiceManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(PolicyServiceManager, self).__init__(service_name = 'hades_policy_service',
                                               *args,
                                               **kwargs)

    def testPolicyService(self, ctxt, host, arg):
        print "manager: testPolicyService\n"
        return "hello policy service manager"