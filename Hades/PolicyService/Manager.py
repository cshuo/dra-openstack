__author__ = 'pike'

import oslo_messaging as messaging
from oslo_config import cfg

from dra.Hades import Manager
from dra.Hades.PMA.RpcApi import ArbiterPMAAPI
from dra.Hades.PMA.RpcApi import MonitorPMAAPI

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
        print "policy loaded is:"
        print policys
        for policy in policys:
            if policy['target'] == 'arbiterPMA':
                self.arbiterPMAApi.loadPolicy({}, 'pike', policy)
            elif policy['target'] == 'monitorPMA':
                self.monitorPMAApi.loadPolicy({}, 'pike', policy)
            else:
                return False
        return True


if __name__ == "__main__":
    CONF.control_exchange = CONF.hades_exchange
    transport = messaging.get_transport(CONF)
    target = messaging.Target(topic=CONF.hades_policyService_topic, server='pike')
    endpoints = [
        PolicyServiceManager(),
    ]
    server = messaging.get_rpc_server(transport, target, endpoints,
                                      executor='blocking')
    server.start()
    server.wait()
