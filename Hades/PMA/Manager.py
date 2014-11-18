__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from PolicyEngine.PolicyManager import PolicyManager

CONF = cfg.CONF


class ArbiterPMAManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(ArbiterPMAManager, self).__init__(service_name = 'hades_arbiterPMA_service',
                                               *args,
                                               **kwargs)

        self.policyManager = PolicyManager()

    def testArbiterPMA(self, ctxt, host, arg):
        print "manager: testArbiterPMA\n"
        return "arbiterPMA"

    def addPolicy(self, xmlPolicy):
        self.policyManager.addPolicyFromXML(xmlPolicy)
