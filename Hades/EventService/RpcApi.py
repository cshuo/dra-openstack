# -*- coding:utf-8 -*-

from oslo_config import cfg

from .. import BaseRpcApi

CONF = cfg.CONF


class EventServiceAPI(BaseRpcApi.BaseAPI):
    def __init__(self, topic, exchange):
        super(EventServiceAPI, self).__init__(topic, exchange)

    def sendEvent(self, ctxt, host, pma, event):
        cctxt = self.client.prepare(server=host)
        cctxt.cast(ctxt, 'sendEvent',
                   host=host, pma=pma, event=event)

    def sendEventForResult(self, ctxt, host, pma, event):
        cctxt = self.client.prepare(server=host)
        return cctxt.call(ctxt, 'sendEventForResult',
                          host=host, pma=pma, event=event)


if __name__ == "__main__":
    print 'eventService rpcapi\n'

    api = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
    # print api.sendEvent({}, 'pike', "arbiterPMA", "(newVM cpubound vmInfo)")
    # api.sendEvent({}, 'pike', 'arbiterPMA', "(host_violation compute1 cpu)")
    # query = '''"[{'field': 'timestamp','op': 'ge','value': '2016-03-08T10:00:00'},{'field': 'timestamp','op': 'lt','value': '2016-03-08T12:00:00'},{'field': 'resource_id','op': 'eq','value': 'compute2_compute2'}]"'''
    # print api.sendEvent({}, "pike", "monitorPMA", "(host_collect_data_statistics compute2_compute2 compute.node.cpu.percent %s None None None avg)" % query)
    # api.sendEventForResult({}, 'pike', 'arbiterPMA', "(evacuation (instance c4d73b6b-4d28-4cde-a8a8-b31613162da8) (type MATLAB_SLAVE))")
    api.sendEventForResult({}, 'pike', 'arbiterPMA', "(dismiss (host compute1))")
