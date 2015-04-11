__author__ = 'pike'

from Hades.EventService.RpcApi import *
from Openstack.Service.Nova import Nova
from Openstack.Service.Ceilometer import Ceilometer
from Openstack.Entity.Instance import Instance
import random


eventService = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
nova = Nova()
ceilometer = Ceilometer()



############################### filter ###############################

# properties = '{"cpu_util" : {"min" : 0.5, "max" : 70}}'
def Host_Filter(hostIds, properties):

    print "Host_Filter : " + hostIds

    hostIds = eval(hostIds)
    properties = eval(properties)

    filteredHosts = []

    for property in properties:

        if property == 'compute.node.cpu.percent':

            for hostId in hostIds:
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

                print hostId + " : " + str(cpuUtil)

                if ((properties[property].has_key('min') and properties[property]['min'] > cpuUtil) or
                        (properties[property].has_key('max') and properties[property]['max'] < cpuUtil)) :
                    pass
                else:
                    filteredHosts.append(hostId)

    print "filteredHosts: " + str(filteredHosts)

    return str(filteredHosts)




############################### cost function ###############################

def Host_CpuUtil_Cost(resourceId):
    print "Host_CpuUtil_Cost"

    q = '''[{"field": "timestamp",
    "op": "ge",
    "value": "2014-12-12T00:00:00"},
    {"field": "timestamp",
    "op": "lt",
    "value": "2014-12-16T00:00:00"},
    {"field": "resource_id",
    "op": "eq",
    "value": "%s"}]''' % resourceId

    score = (100 - Collect_Data_Statistics(meter_name='compute.node.cpu.percent', queryFilter=q)) / 100.0

    print resourceId + " : " + str(score)

    return score

cost_functions = {
    "Host_CpuUtil_Cost" : Host_CpuUtil_Cost
}

############################### monitor ###############################


def Collect_Data(meter_name, queryFilter, result = "counter_volume"):

    print "Collect_Data"

    data = ceilometer.getMeter(meter_name, queryFilter)
    return data[result]

def Collect_Data_Statistics(meter_name, queryFilter, groupBy = None, period = None, aggregate = None, result = "avg"):

    print "Collect_Data_Statistics"
    #print meter_name
    #print queryFilter

    #data = ceilometer.getMeterStatistics(meter_name, queryFilter, groupBy, period, aggregate)
    #print data[result]
    #return data[result]
    return 1

def Get_Vms_On_Host(hostId):

    print "Get_Vms_On_Host: " + hostId

    hostName = Host_Id_To_Name(hostId)
    instances = nova.getInstancesOnHost(hostName)
    instanceIds = []
    for instance in instances:
        instanceIds.append(instance.getId())

    print str(instanceIds)

    return str(instanceIds)

def Host_Set_Threshold(resourceId, meter_name, value, properties):

    print "Host_Set_Threshold"

    properties = eval(properties)

    if properties.has_key(meter_name):

        if (properties[meter_name].has_key("min")):
            min = properties[meter_name]["min"]
            if value < min:
                event = "(host_violation %s %s)" % (resourceId, meter_name)
                eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
                print event
        elif (properties[meter_name].has_key("max")):
            max = properties[meter_name]["max"]
            if value > max:
                event = "(host_violation %s %s)" % (resourceId, meter_name)
                eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
                print event


#def Vm_Set_Threshold(resourceId, meter_name, value, properties):
#    pass



############################### arbiter ###############################

#input params are all lists
def Host_Generic_Selector(hostIds, costFunctions, factors):

    print "Host_Generic_Selector: " + hostIds

    hostIds = eval(hostIds)
    costFunctions = eval(costFunctions)
    factors = eval(factors)

    dict = {}

    for host in hostIds:
        cost = 0
        for i in range(len(costFunctions)):
            cost += cost_functions[costFunctions[i]](host) * factors[i]
        dict[host] = cost

    sortedList = sorted(dict.items(), lambda x,y : cmp(x[1], y[1]))
    destHost = sortedList[-1][0]

    print destHost

    return destHost


def Vm_Random_Selector(instanceIds):

    print "Vm_Random_Selector"

    instanceIds = eval(instanceIds)
    index = random.randint(0, len(instanceIds)-1)
    vm = instanceIds[index]

    print vm

    return vm


def Migrate(instanceId, hostId):
    hostName = Host_Id_To_Name(hostId)
    print "migrate: " + instanceId + " to " + hostName
    nova = Nova()
    nova.liveMigration(instanceId, hostName)


def Host_Id_To_Name(hostId):
    return hostId.split('_')[0]

def Host_Name_To_Id(hostName):
    return "%s_%s" % (hostName, hostName)




if __name__ == "__main__":
    properties = '{"cpu_util" : {"min" : 0.5, "max" : 70}}'
    #Host_Set_Threshold("compute1_compute1", "cpu_util" , 5, properties)
    #test = {'a' : 1, 'b' : 2, 'c' : 0}
    #print sorted(test.items(), lambda x,y : cmp(x[1], y[1]))
    #print Host_CpuUtil_Cost('compute1_compute1')
    #print Host_CpuUtil_Cost('compute2_compute2')
    #hosts = '["compute1_compute1", "compute2_compute2"]'
    #costFunctions = '["Host_CpuUtil_Cost"]'
    #factors = '[1]'

    #print Host_Generic_Selector(hosts, costFunctions, factors)
    #list =  Get_Vms_On_Host('compute2')
    #Migrate("5bdbf476-f046-4986-9e1d-5b078414a298", "compute1")
    #print Host_Filter("['compute1_compute1','compute2_compute2']", properties)
