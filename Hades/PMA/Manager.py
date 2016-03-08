__author__ = 'pike'

from Hades import Manager
import oslo_messaging as messaging
from oslo_config import cfg
from PolicyEngine.PolicyManager import PolicyManager

CONF = cfg.CONF


class PMAManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(PMAManager, self).__init__(*args,**kwargs)

        # use policyManager to manage policies for each PMA
        self.policyManager = PolicyManager()

    ########################### POLICY ##############################

    def loadPolicy(self, ctxt, host, policy):
        self.policyManager.loadPolicy(policy)
        print 'loadPolicy'
        return True

    ########################### EVENT ##############################

    def handleEvent(self, ctxt, host, event):
        print "handleEvent: " + event
        self.policyManager.assertFact(event)
        self.policyManager.run()


    def handleEventWithResult(self, ctxt, host, event):
        print "handleEventWithResult: " + event
        self.policyManager.assertFact(event)
        self.policyManager.run()
        result = self.policyManager.getStdout()
        print result
        return result


class ArbiterPMAManager(PMAManager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(ArbiterPMAManager, self).__init__(service_name = 'hades_arbiterPMA_service',
                                               *args,
                                               **kwargs)

class MonitorPMAManager(PMAManager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):
        super(MonitorPMAManager, self).__init__(service_name = 'hades_monitorPMA_service',
                                                *args,
                                                **kwargs)

if __name__ == "__main__":
    manager = ArbiterPMAManager()
    print manager.service_name
