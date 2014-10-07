__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc
from Hades import Config

CONF =  cfg.CONF

class ArbiterAPI(object):

    """
    client side of the arbiter rpc API
    """

    def __init__(self):
        super(ArbiterAPI, self).__init__()
        target = messaging.Target(topic = CONF.hades_arbiter_topic, version = '3.0')
        version_cap = '3.23'
        serializer = None
        self.client = self.get_client(target, version_cap, serializer)

    def get_client(self, target, version_cap, serializer):
        return Rpc.get_client(target,
                              version_cap = version_cap,
                              serializer = serializer)

    def testArbiter(self, ctxt, host, arg):
        version = '3.0'
        cctxt = self.client.prepare(server = host,
                                    version = version)
        return cctxt.call(ctxt, 'testArbiter',
                   host = host, arg = arg)

if __name__ == "__main__":
    print 'arbiter rpcapi\n'
    Config.config_init(CONF.hades_exchange)
    arbiter_api = ArbiterAPI()
    print arbiter_api.testArbiter({}, 'localhost', None)
