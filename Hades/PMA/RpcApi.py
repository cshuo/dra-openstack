__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc
from Hades import Config

CONF =  cfg.CONF

class ArbiterPMAAPI(object):


    def __init__(self):
        super(ArbiterPMAAPI, self).__init__()

        # exchange is set in CONF.control_exchange
        target = messaging.Target(topic = CONF.hades_arbiterPMA_topic)
        version_cap = None
        serializer = None
        self.client = self.get_client(target, version_cap, serializer)

    def get_client(self, target, version_cap, serializer):
        return Rpc.get_client(target,
                              version_cap = version_cap,
                              serializer = serializer)

    def testArbiterPMA(self, ctxt, host, arg):
        cctxt = self.client.prepare(server = host,)
        return cctxt.call(ctxt, 'testArbiterPMA',
                   host = host, arg = arg)

    def loadPolicy(self, ctxt, policy):
        pass

if __name__ == "__main__":
    print 'arbiterPMA rpcapi\n'
    Config.config_init(CONF.hades_exchange)
    api = ArbiterPMAAPI()
    print api.testArbiterPMA({}, 'pike', None)
