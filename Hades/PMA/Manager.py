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

    def loadPolicy(self, ctxt, host, arg):

        return "loadPolicy"

    def addPolicyFromXML(self, xmlPolicy):
        self.policyManager.addPolicyFromXML(xmlPolicy)

    def enablePolicy(self, policyName):
        self.policyManager.enablePolicy(policyName)
