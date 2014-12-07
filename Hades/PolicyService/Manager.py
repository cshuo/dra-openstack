__author__ = 'pike'

from Hades import Manager
from oslo import messaging
from oslo.config import cfg
from Hades.PMA.RpcApi import ArbiterPMAAPI
from Hades.PMA.RpcApi import MonitorPMAAPI

CONF = cfg.CONF


class PolicyServiceManager(Manager.Manager):

    target = messaging.Target()

    def __init__(self, *args, **kwargs):

        super(PolicyServiceManager, self).__init__(service_name = 'hades_policy_service',
                                               *args,
                                               **kwargs)
        self.arbiterPMAApi = ArbiterPMAAPI(CONF.hades_arbiterPMA_topic, CONF.hades_exchange)
        self.monitorPMAApi = MonitorPMAAPI(CONF.hades_monitorPMA_topic, CONF.hades_exchange)

    def loadPolicy(self, ctxt, host, policys):
        for policy in policys:
            if policy['target'] == 'arbiterPMA':
                self.arbiterPMAApi.loadPolicy({}, 'pike', policy)
            elif policy['target'] == 'monitorPMA':
                self.monitorPMAApi.loadPolicy({}, 'pike', policy)
            else:
                return False

        return True
