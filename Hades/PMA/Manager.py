__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from PolicyEngine.PolicyManager import PolicyManager

CONF = cfg.CONF

class PMAManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(PMAManager, self).__init__(*args,**kwargs)

        self.policyManager = PolicyManager()

    def loadPolicy(self, ctxt, host, policy):

        self.addPolicysFromXML(policy)
        return self.policyManager.getPolicyByName('policy3').getAction().getValue()

    def addPolicysFromXML(self, xmlPolicy):
        self.policyManager.addPolicysFromXML(xmlPolicy)

    def enablePolicy(self, policyName):
        self.policyManager.enablePolicy(policyName)



class ArbiterPMAManager(PMAManager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(ArbiterPMAManager, self).__init__(service_name = 'hades_arbiterPMA_service',
                                               *args,
                                               **kwargs)


if __name__ == "__main__":
    manager = ArbiterPMAManager()
    print manager.service_name
