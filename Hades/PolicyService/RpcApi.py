__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc
from Hades import Config

CONF =  cfg.CONF

class PolicyServiceAPI(object):

    """
    client side of the policyService rpc API
    """

    def __init__(self):
        super(PolicyServiceAPI, self).__init__()

        # exchange is set in CONF.control_exchange
        target = messaging.Target(topic = CONF.hades_policyService_topic)
        version_cap = None
        serializer = None
        self.client = self.get_client(target, version_cap, serializer)

    def get_client(self, target, version_cap, serializer):
        return Rpc.get_client(target,
                              version_cap = version_cap,
                              serializer = serializer)

    def testPolicyService(self, ctxt, host, arg):
        cctxt = self.client.prepare(server = host,)
        return cctxt.call(ctxt, 'testPolicyService',
                   host = host, arg = arg)

if __name__ == "__main__":
    print 'policyService rpcapi\n'
    Config.config_init(CONF.hades_exchange)
    api = PolicyServiceAPI()
    print api.testPolicyService({}, 'pike', None)
