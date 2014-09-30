__author__ = 'pike'

from oslo import messaging
from oslo.config import cfg
from Hades import Rpc
from Hades import Config

CONF =  cfg.CONF

class SchedulerAPI(object):

    """
    client side of the scheduler rpc API
    """

    def __init__(self):
        super(SchedulerAPI, self).__init__()
        target = messaging.Target(topic = CONF.scheduler_topic, exchange = CONF.exchange, version = '3.0')
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
        return cctxt.call(ctxt, 'testSchedule',
                   host = host, arg = arg)

if __name__ == "__main__":
    Config.config_init()
    scheduler_api = SchedulerAPI()
    print scheduler_api.testSchedule({}, 'localhost', None)