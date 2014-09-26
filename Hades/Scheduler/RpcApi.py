__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc

rpcapi_opts = [
    cfg.StrOpt('scheduler_topic',
               default = 'scheduler',
               help = 'the topic hades nodes listen on'),
]

CONF =  cfg.CONF
CONF.register_opts(rpcapi_opts)

class SchedulerAPI(object):

    """
    client side of the scheduler rpc API
    """

    def __init__(self):
        super(SchedulerAPI, self).__init__()
        target = messaging.Target(topic = CONF.compute_topic, version = '3.0')
        version_cap = '3.23'
        serializer = None
        self.client = self.get_client(target, version_cap, serializer)

    def get_client(self, target, version_cap, serializer):
        return Rpc.get_client(target,
                              version_cap = version_cap,
                              serializer = serializer)

    def testSchedule(self, ctxt, host, arg):
        version = '3.0'
        cctxt = self.client.prepare(server = host,
                                    version = version)
        cctxt.cast(ctxt, 'testSchedule',
                   host = host, arg = arg)