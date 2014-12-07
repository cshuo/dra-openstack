__author__ = 'pike'

from Hades.EventService.RpcApi import *

eventService = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
#api.sendEvent({}, 'pike', "arbiterPMA", "(newVM cpubound vmInfo)")

def migrate():
    print "migrate"

############################### filter ###############################

def Host_CpuUtil_Filter():
    return 'hosts'


############################### cost function ###############################

def Host_CpuUtil_Cost(hosts):
    return 'compute2'


############################### monitor ###############################

def Get_Host_Resource(host_id, resource):
    return 90

############################### arbiter ###############################

def Host_resource_upperBound(host_id, resource, value):
    if value > 80:
        print "violation"
        eventService.sendEvent({}, 'pike', 'arbiterPMA', "(violation host host_id resource upperBound value)")
        print "violation end"