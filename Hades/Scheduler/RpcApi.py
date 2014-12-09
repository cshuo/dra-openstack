__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc
from Hades import Config
from Hades import BaseRpcApi
from oslo.config import cfg


CONF =  cfg.CONF

class SchedulerAPI(BaseRpcApi.BaseAPI):

    """
    client side of the scheduler rpc API
    """

    def __init__(self, topic, exchange):
        super(SchedulerAPI, self).__init__(topic, exchange)


    def testSchedule(self, ctxt, host, arg):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'testSchedule',
                   host = host, arg = arg)

if __name__ == "__main__":
    #scheduler_api = SchedulerAPI(CONF.hades_scheduler_topic, CONF.hades_exchange)
    #print scheduler_api.testSchedule({}, 'pike', None)
    messaging.set_transport_defaults('hades')


    TRANSPORT = messaging.get_transport(CONF,
                                        url = 'rabbit://guest:RABBIT_PASS@114.212.189.134:5672/',
                                        allowed_remote_exmods = [],
                                        aliases = {})
    target = messaging.Target(topic = 'hades_scheduler_topic')
    version_cap = None
    serializer = None
    client = messaging.RPCClient(TRANSPORT,
                               target,
                               version_cap = version_cap,
                               serializer = serializer)

    cctxt = client.prepare(server = 'pike')
    cctxt.call({}, 'testSchedule', host = 'pike', arg = '')