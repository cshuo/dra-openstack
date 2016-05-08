# -*- coding: utf-8 -*-

import oslo_messaging as messaging
from oslo_config import cfg

from dra.Hades import Manager
from dra.PolicyEngine.PolicyManager import PolicyManager


CONF = cfg.CONF


class PMAManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(PMAManager, self).__init__(*args,**kwargs)

        # use policyManager to manage policies for each PMA
        self.policyManager = PolicyManager()

    def loadPolicy(self, ctxt, host, policy):
        self.policyManager.loadPolicy(policy)
        print 'PMAManager -> loadPolicy'
        print policy
        return True

    def handleEvent(self, ctxt, host, event):
        print "PMAManager -> handleEvent: " + event
        self.policyManager.assertFact(event)
        self.policyManager.run()

    def handleEventWithResult(self, ctxt, host, event):
        print "PMAManager -> handleEventWithResult: " + event
        self.policyManager.assertFact(event)
        self.policyManager.run()
        result = self.policyManager.getStdout()
        print result
        return result


class ArbiterPMAManager(PMAManager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):
        super(ArbiterPMAManager, self).__init__(service_name='hades_arbiterPMA_service', *args, **kwargs)
        self.init_event_template()

    def init_event_template(self):
        """
        init system event facts template
        """
        self.policyManager.buildTemplate('evacuate', """(slot instance (type SYMBOL)) (slot type (type SYMBOL))""",
                                         "vm evacuate event facts")
        self.policyManager.buildTemplate('migrate', """(slot instance (type SYMBOL)) (slot src (type SYMBOL)) (slot dest (type SYMBOL))""",
                                         "vm migrate event facts")


class MonitorPMAManager(PMAManager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):
        super(MonitorPMAManager, self).__init__(service_name='hades_monitorPMA_service', *args, **kwargs)

if __name__ == "__main__":
    manager = ArbiterPMAManager()
    print manager.service_name
