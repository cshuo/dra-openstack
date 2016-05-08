__author__ = 'pike'

import random

from dra.Hades.EventService.RpcApi import *
from dra.Openstack.Service.Nova import Nova
from dra.Openstack.Service.Ceilometer import Ceilometer
from dra.Openstack.Entity.Instance import Instance


eventService = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
nova = Nova()
ceilometer = Ceilometer()


############################### added by cshuo ###############################
def simple_host_filter():
    return str(nova.getComputeHosts())

def test_eva(instance, vm_type):
    print "--------------------------test_eva-----------------------"
    print "Hi, I am " + instance
    print "type of {0} is {1}".format(instance, vm_type)
############################### added by cshuo ###############################


############################### filter ###############################

# properties = '{"cpu_util" : {"min" : 0.5, "max" : 70}}'
def Host_Filter(hostIds, threshold):
    """
    filter hosts by specific meters. NOTE support cpu utils only now NOTE 
    """
    print "Host to filter: " + hostIds
    hostIds = eval(hostIds)
    properties = eval(threshold)

    filteredHosts = []

    for property in properties:
        if property == 'compute.node.cpu.percent':
            for hostId in hostIds:
                resource_id = hostId + '_' + hostId
                q = '''[{"field": "timestamp",
                    "op": "ge",
                    "value": "2016-03-08T10:00:00"},
                    {"field": "timestamp",
                    "op": "lt",
                    "value": "2016-03-08T12:00:00"},
                    {"field": "resource_id",
                    "op": "eq",
                    "value": "%s"}]''' % resource_id

                cpuUtil = Collect_Data_Statistics(meter_name='compute.node.cpu.percent', queryFilter=q)
                print hostId + " : " + str(cpuUtil)
                if ((properties[property].has_key('min') and properties[property]['min'] > cpuUtil) or
                        (properties[property].has_key('max') and properties[property]['max'] < cpuUtil)) :
                    pass
                else:
                    filteredHosts.append(hostId)
    print "filtered hosts is: ", filteredHosts
    return str(filteredHosts)

############################### cost function ###############################

def Host_CpuUtil_Cost(host_id):
    resource_id = host_id + '_' + host_id
    q = '''[{"field": "timestamp",
    "op": "ge",
    "value": "2016-03-08T10:00:00"},
    {"field": "timestamp",
    "op": "lt",
    "value": "2016-03-08T12:00:00"},
    {"field": "resource_id",
    "op": "eq",
    "value": "%s"}]''' % resource_id
    score = (100 - Collect_Data_Statistics(meter_name='compute.node.cpu.percent', queryFilter=q)) / 100.0
    #score = random.randint(1,99)
    return score

cost_functions = {
    "Host_CpuUtil_Cost" : Host_CpuUtil_Cost
}

############################### monitor ###############################


def Collect_Data(meter_name, queryFilter, result = "counter_volume"):

    print "Collect_Data"

    data = ceilometer.getMeter(meter_name, queryFilter)
    return data[result]


def Collect_Data_Statistics(meter_name, queryFilter, groupBy = None, period = None, aggregate = None, metric= "avg"):
    #print meter_name
    #print queryFilter
    data = ceilometer.getMeterStatistics(meter_name, queryFilter, groupBy, period, aggregate)
    return data[metric]


def Get_Vms_On_Host(resourceId):
    hostName = Resource_Id_To_Name(resourceId)
    instances = nova.getInstancesOnHost(hostName)
    instanceIds = []
    for instance in instances:
        instanceIds.append(str(instance.getId()))
    return str(instanceIds)


def Host_Set_Threshold(resourceId, meter_name, value, threshold):
    print "Host_Set_Threshold: {res}, {meter}, {value}".format(res=resourceId, meter=meter_name, value=value)
    properties = eval(threshold)

    if properties.has_key(meter_name):
        print "deal ", meter_name
        if (properties[meter_name].has_key("min")):
            min = properties[meter_name]["min"]
            if value < min:
                event = "(host_violation %s %s)" % (resourceId, meter_name)
                eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
                print event
        if (properties[meter_name].has_key("max")):
            max = properties[meter_name]["max"]
            if value > max:
                print "value too large..."
                event = "(host_violation %s %s)" % (resourceId, meter_name)
                eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
                print event


############################### arbiter ###############################

#input params are all lists
def Host_Generic_Selector(hostIds, costFunctions, factors):
    """
    get optimal dest hosts selection with respect to cost functions and according factors
    """
    hostIds = eval(hostIds)
    costFunctions = eval(costFunctions)
    factors = eval(factors)

    host_cost = {}

    for host in hostIds:
        cost = 0
        for i in range(len(costFunctions)):
            cost += cost_functions[costFunctions[i]](host) * factors[i]
        host_cost[host] = cost
    dest_h = max(host_cost, key=host_cost.get)
    print "dest host is: ", dest_h
    return dest_h


def Vm_Random_Selector(instanceIds):
    instanceIds = eval(instanceIds)
    index = random.randint(0, len(instanceIds)-1)
    vm = instanceIds[index]
    print "selected vm is: ", vm
    return vm


def Migrate(instanceId, hostId):
    vm_lists = Get_Vms_On_Host(Host_Name_To_Id(hostId))
    if instanceId in vm_lists:
        print "vm already in dest host..."
        return 
    hostName = hostId
    print "migrate: " + instanceId + " to " + hostName
    nova = Nova()
    nova.liveMigration(instanceId, hostName)


def Resource_Id_To_Name(hostId):
    return hostId.split('_')[0]


def Host_Name_To_Id(hostName):
    return "%s_%s" % (hostName, hostName)



if __name__ == "__main__":
    #properties = '{"cpu_util" : {"min" : 0.5, "max" : 70}}'
    #Host_Set_Threshold("compute1_compute1", "cpu_util" , 5, properties)
    #test = {'a' : 1, 'b' : 2, 'c' : 0}
    #print sorted(test.items(), lambda x,y : cmp(x[1], y[1]))
    #print Host_CpuUtil_Cost('compute1')
    #print Host_CpuUtil_Cost('compute2')
    #print simple_host_filter()
    hosts = '["compute1", "compute2"]'
    costFunctions = '["Host_CpuUtil_Cost"]'
    factors = '[1]'
    print Host_Generic_Selector(hosts, costFunctions, factors)
    #list =  Get_Vms_On_Host('compute2')
    #Migrate("5bdbf476-f046-4986-9e1d-5b078414a298", "compute1")
    #properties = '{"compute.node.cpu.percent" : {"min" : 0.5, "max" : 70}}'
    #print Host_Filter("['compute1','compute2']", properties)
    #vms = Get_Vms_On_Host("compute2")
    #print Vm_Random_Selector(vms)
