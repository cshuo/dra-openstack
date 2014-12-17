__author__ = 'pike'

from Hades.EventService.RpcApi import *
from Openstack.Service.Nova import Nova
from Openstack.Service.Ceilometer import Ceilometer
from Openstack.Entity.Instance import Instance


eventService = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
nova = Nova()
ceilometer = Ceilometer()



############################### filter ###############################

#def Host_CpuUtil_Filter():
#    return 'compute1'

def Host_Filter(hosts, properties):
    hosts = eval(hosts)

    for property in properties:

        if properties == 'cpu_util':

            for hostId in hosts:
                q = '''[{"field": "timestamp",
                    "op": "ge",
                    "value": "2014-12-12T00:00:00"},
                    {"field": "timestamp",
                    "op": "lt",
                    "value": "2014-12-16T00:00:00"},
                    {"field": "resource_id",
                    "op": "eq",
                    "value": "%s"}]''' % hostId
                cpuUtil = Collect_Data_Statistics(meter_name='compute.node.cpu.percent', queryFilter=q)
                if ((properties['cpu_util'].has_key('min') and properties['cpu_util']['min'] > cpuUtil) or
                        (properties['cpu_util'].has_key('max') and properties['cpu_util']['max'] < cpuUtil)) :
                    hosts.remove(hostId)


    return hosts




############################### cost function ###############################

#def Host_CpuUtil_Cost(hosts):
#    return 'compute2'
#
#def VM_CpuUtil_Cost(vms):
#    instances = nova.getInstances()
#    id = instances[0].getId()
#    return id
def Host_CpuUtil_Cost(resourceId):

    q = '''[{"field": "timestamp",
    "op": "ge",
    "value": "2014-12-12T00:00:00"},
    {"field": "timestamp",
    "op": "lt",
    "value": "2014-12-16T00:00:00"},
    {"field": "resource_id",
    "op": "eq",
    "value": "%s"}]''' % resourceId

    score = 1- Collect_Data_Statistics(meter_name='compute.node.cpu.percent', queryFilter=q)
    return score

cost_functions = {
    "Host_CpuUtil_Cost" : Host_CpuUtil_Cost
}

############################### monitor ###############################


def Collect_Data(meter_name, queryFilter, result = "counter_volume"):
    data = ceilometer.getMeter(meter_name, queryFilter)
    return data[result]

def Collect_Data_Statistics(meter_name, queryFilter, groupBy = None, period = None, aggregate = None, result = "avg"):
    data = ceilometer.getMeterStatistics(meter_name, queryFilter, groupBy, period, aggregate)
    return data[result]

def Host_Set_Threshold(resourceId, meter_name, value, properties):
    properties = eval(properties)

    if properties.has_key(meter_name):

        if (properties[meter_name].has_key("min")):
            min = properties[meter_name]["min"]
            if value < min:
                event = "(violation host %s %s)" % (resourceId, meter_name)
                #eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
                print event
        elif (properties[meter_name].has_key("max")):
            max = properties[meter_name]["max"]
            if value < min:
                event = "(violation host %s %s)" % (resourceId, meter_name)
                #eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
                print event


def Vm_Set_Threshold(resourceId, meter_name, value, properties):
    pass

def Get_Vms_On_Host(host):
    instances = nova.getInstancesOnHost(host)
    instanceIds = []
    for instance in instances:
        instanceIds.append(instance.getId())
    return str(instanceIds)

############################### arbiter ###############################

#def Host_Resource_UpperBound(host_id, resource, value):
#    if value > 80:
#        print "violation"
#        event = "(violation host %s %s upperBound %s)" % (host_id, resource, value)
#        eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
#        print "violation end"
#

#input params are all lists
def Host_Generic_Selector(hosts, costFunctions, factors):
    hosts = eval(hosts)
    costFunctions = eval(costFunctions)
    factors = eval(factors)

    dict = {}

    for host in hosts:
        cost = 0
        for i in range(len(costFunctions)):
            cost += cost_functions[costFunctions[i]](host) * factors[i]
        dict[host] = cost

    sortedList = sorted(dict.items(), lambda x,y : cmp(x[1], y[1]))
    return sortedList[-1][0]

def Migrate(vm, host):
    print "migrate: " + vm + " to " + host
    nova = Nova()
    nova.liveMigration(vm, host)



if __name__ == "__main__":
    #properties = '''{"cpu_util" : {"min" : 10, "max" : 90}}'''
    #Host_Set_Threshold("compute1_compute1", "cpu_util" , 5, properties)
    #test = {'a' : 1, 'b' : 2, 'c' : 0}
    #print sorted(test.items(), lambda x,y : cmp(x[1], y[1]))
    #print Host_CpuUtil_Cost('compute1_compute1')
    #print Host_CpuUtil_Cost('compute2_compute2')
    #hosts = '["compute1_compute1", "compute2_compute2"]'
    #costFunctions = '["Host_CpuUtil_Cost"]'
    #factors = '[1]'
    #
    #print Host_Generic_Selector(hosts, costFunctions, factors)
    list =  Get_Vms_On_Host('compute2')