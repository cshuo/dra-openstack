__author__ = 'pike'

import oslo_messaging as messaging
from oslo_config import cfg
from Hades import Rpc
from Hades import Config
from Hades import BaseRpcApi


CONF =  cfg.CONF

class EventServiceAPI(BaseRpcApi.BaseAPI):



    def __init__(self, topic, exchange):
        super(EventServiceAPI, self).__init__(topic, exchange)


    def sendEvent(self, ctxt, host, pma, event):
        cctxt = self.client.prepare(server = host)
        cctxt.cast(ctxt, 'sendEvent',
                   host = host, pma = pma, event = event)

    def sendEventForResult(self, ctxt, host, pma, event):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'sendEventForResult',
                   host = host, pma = pma, event = event)

if __name__ == "__main__":
    print 'eventService rpcapi\n'

    api = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
    #print api.sendEvent({}, 'pike', "arbiterPMA", "(newVM cpubound vmInfo)")
    api.sendEvent({}, 'pike', 'arbiterPMA', "host_violation compute2 cpu")
    #query = '''"[{'field': 'timestamp','op': 'ge','value': '2014-12-12T00:00:00'},{'field': 'timestamp','op': 'lt','value': '2014-12-16T00:00:00'},{'field': 'resource_id','op': 'eq','value': 'compute2'}]"'''
    #print api.sendEvent({}, "pike", "monitorPMA", "(host_collect_data_statistics compute2 compute.node.cpu.percent %s None None None avg)" % query)
