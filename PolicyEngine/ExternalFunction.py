__author__ = 'pike'

from Hades.EventService.RpcApi import *
from Openstack.Service.Nova import Nova
from Openstack.Entity.Instance import Instance

eventService = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
#api.sendEvent({}, 'pike', "arbiterPMA", "(newVM cpubound vmInfo)")

def Migrate(vm, host):
    print "migrate: " + vm + " to " + host
    nova = Nova()
    nova.liveMigration(vm, host)

############################### filter ###############################

def Host_CpuUtil_Filter():
    return 'compute1'


############################### cost function ###############################

def Host_CpuUtil_Cost(hosts):
    return 'compute2'

def VM_CpuUtil_Cost(vms):
    nova = Nova()
    instances = nova.getInstances()
    id = instances[0].getId()
    return id


############################### monitor ###############################

def Get_Host_Resource(host_id, resource):
    return 90

def Get_VMs_On_Host(host_id):
    return "vms"

############################### arbiter ###############################

def Host_Resource_UpperBound(host_id, resource, value):
    if value > 80:
        print "violation"
        event = "(violation host %s %s upperBound %s)" % (host_id, resource, value)
        eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
        print "violation end"