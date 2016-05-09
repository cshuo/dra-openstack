# -*- coding:utf-8 -*-

import random
import sys
from ..Hades.EventService.RpcApi import *
from ..Openstack.Service.Nova import Nova
from ..Openstack.Service.Ceilometer import Ceilometer
from ..db.utils import DbUtil

_eventService = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
_nova = Nova()
_ceilometer = Ceilometer()


# added by cshuo #
def simple_host_filter():
    return str(_nova.getComputeHosts())


def test_eva(instance, vm_type):
    print "--------------------------test_eva-----------------------"
    print "Hi, I am " + instance
    print "type of {0} is {1}".format(instance, vm_type)


def print_log(log):
    print log


def generateEvent(event_name, *args):
    """
    assert a event into Clips
    @param event_name:
    @param args:
    @return:
    """
    if event_name == 'evacuation':
        event = "(evacuation (instance {id}) (type {type}))".format(id=args[0], type=args[1])
    elif event_name == 'migration':
        event = "(migration (instance {id}) (src {src}) (dest {dest}))".format(id=args[0], src=args[1],
                                                                               dest=args[2])
    print "generateEvent -> :\n", event
    _eventService.sendEvent({}, 'pike', 'arbiterPMA', event)


def hostFilter(host_list, expr, mode):
    """
    filter hosts or select a host
    @param host_list:
    @param expr:
    @param mode: optional 'select' and 'filter'
    @return:
    """
    if mode == 'select':
        for host in host_list:
            if eval(expr.replace('$HOST', '"'+host+'"')):
                return host
    else:
        ret_host = []
        for host in host_list:
            if eval(expr.replace('$HOST', '"'+host+'"')):
                ret_host.append(host)
        return ret_host
    return None


def getAllHost(instance):
    host_list = _nova.getComputeHosts()
    host_list.remove(getVmHost(instance))
    return host_list


def hostHasInstanceType(host, vm_type):
    vms = _nova.getInstancesOnHost(host)
    dbu = DbUtil()
    for vm in vms:
        if dbu.query_vm(vm)['type'] == vm_type:
            return 1
    return 0


def last_n_avg_statistic(host, meter, time_range):
    if meter == 'cpu_util':
        meter = 'compute.node.cpu.percent'
    return _ceilometer.last_n_average_statistic(time_range, host+'_'+host, meter)


def hostRankFilter(host_list, obj_host, expr):
    """
    @param host_list:
    @param obj_host: e.g., matlab master host or host where the hadoop file on
    @param expr:
    @return:
    """
    dest_host = host_list[0]
    if 'getTimeDelay' in expr:
        min_delay = sys.maxint
        for host in host_list:
            expr = expr.replace('$HOST', '"'+host+'"').replace('$MASTER', '"'+obj_host+'"')
            delay = eval(expr)
            if delay < min_delay:
                dest_host = host
                min_delay = delay
    return dest_host


def getTimeDelay(host, obj_host):
    """
    network time delay between hosts
    @param host:
    @param obj_host:
    @return:
    """
    return random.randint(50, 100)


def getVmHost(instance):
    """
    return host where the vm lives on
    @param instance:
    @return:
    """
    return _nova.inspect_instance(instance)['OS-EXT-SRV-ATTR:host']


def Migrate(src_host, instance, dest_host):
    """
    @param src_host:
    @param instance:
    @param dest_host:
    @return:
    """
    print '>>action: migrate ' + instance + ' to ' + dest_host
    _nova.liveMigration(instance, dest_host)


def hostPredictData(host, meter, time_range, meter_section):
    """
    @param host
    @param meter
    @param time_range
    @param meter_section
    @return
    """
    # for bandwidth testing now
    return 500


# added by cshuo #


# filter #
# properties = '{"cpu_util" : {"min" : 0.5, "max" : 70}}'
# def Host_Filter(hostIds, threshold):
#     """
#     filter hosts by specific meters.
#     NOTE support cpu utils only now NOTE
#     """
#     print "Host to filter: " + hostIds
#     hostIds = eval(hostIds)
#     properties = eval(threshold)
#
#     filteredHosts = []
#
#     for property in properties:
#         if property == 'compute.node.cpu.percent':
#             for hostId in hostIds:
#                 resource_id = hostId + '_' + hostId
#                 q = '''[{"field": "timestamp",
#                     "op": "ge",
#                     "value": "2016-03-08T10:00:00"},
#                     {"field": "timestamp",
#                     "op": "lt",
#                     "value": "2016-03-08T12:00:00"},
#                     {"field": "resource_id",
#                     "op": "eq",
#                     "value": "%s"}]''' % resource_id
#
#                 cpuUtil = Collect_Data_Statistics(meter_name='compute.node.cpu.percent', queryFilter=q)
#                 print hostId + " : " + str(cpuUtil)
#                 if ((properties[property].has_key('min') and properties[property]['min'] > cpuUtil) or
#                         (properties[property].has_key('max') and properties[property]['max'] < cpuUtil)):
#                     pass
#                 else:
#                     filteredHosts.append(hostId)
#     print "filtered hosts is: ", filteredHosts
#     return str(filteredHosts)
#
#
# # cost function ###############################
#
# def Host_CpuUtil_Cost(host_id):
#     resource_id = host_id + '_' + host_id
#     q = '''[{"field": "timestamp",
#     "op": "ge",
#     "value": "2016-03-08T10:00:00"},
#     {"field": "timestamp",
#     "op": "lt",
#     "value": "2016-03-08T12:00:00"},
#     {"field": "resource_id",
#     "op": "eq",
#     "value": "%s"}]''' % resource_id
#     score = (100 - Collect_Data_Statistics(meter_name='compute.node.cpu.percent', queryFilter=q)) / 100.0
#     # score = random.randint(1,99)
#     return score
#
#
# cost_functions = {
#     "Host_CpuUtil_Cost": Host_CpuUtil_Cost
# }
#
#
# # monitor ###############################
#
#
# def Collect_Data(meter_name, queryFilter, result="counter_volume"):
#     print "Collect_Data"
#
#     data = ceilometer.getMeter(meter_name, queryFilter)
#     return data[result]
#
#
# def Collect_Data_Statistics(meter_name, queryFilter, groupBy=None, period=None, aggregate=None, metric="avg"):
#     # print meter_name
#     # print queryFilter
#     data = ceilometer.getMeterStatistics(meter_name, queryFilter, groupBy, period, aggregate)
#     return data[metric]
#
#
# def Get_Vms_On_Host(resourceId):
#     hostName = Resource_Id_To_Name(resourceId)
#     instances = nova.getInstancesOnHost(hostName)
#     instanceIds = []
#     for instance in instances:
#         instanceIds.append(str(instance.getId()))
#     return str(instanceIds)
#
#
# def Host_Set_Threshold(resourceId, meter_name, value, threshold):
#     print "Host_Set_Threshold: {res}, {meter}, {value}".format(res=resourceId, meter=meter_name, value=value)
#     properties = eval(threshold)
#
#     if properties.has_key(meter_name):
#         print "deal ", meter_name
#         if (properties[meter_name].has_key("min")):
#             min = properties[meter_name]["min"]
#             if value < min:
#                 event = "(host_violation %s %s)" % (resourceId, meter_name)
#                 eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
#                 print event
#         if (properties[meter_name].has_key("max")):
#             max = properties[meter_name]["max"]
#             if value > max:
#                 print "value too large..."
#                 event = "(host_violation %s %s)" % (resourceId, meter_name)
#                 eventService.sendEvent({}, 'pike', 'arbiterPMA', event)
#                 print event
#
#
# # arbiter ###############################
#
# # input params are all lists
# def Host_Generic_Selector(hostIds, costFunctions, factors):
#     """
#     get optimal dest hosts selection with respect to cost functions and according factors
#     """
#     hostIds = eval(hostIds)
#     costFunctions = eval(costFunctions)
#     factors = eval(factors)
#
#     host_cost = {}
#
#     for host in hostIds:
#         cost = 0
#         for i in range(len(costFunctions)):
#             cost += cost_functions[costFunctions[i]](host) * factors[i]
#         host_cost[host] = cost
#     dest_h = max(host_cost, key=host_cost.get)
#     print "dest host is: ", dest_h
#     return dest_h
#
#
# def Vm_Random_Selector(instanceIds):
#     instanceIds = eval(instanceIds)
#     index = random.randint(0, len(instanceIds) - 1)
#     vm = instanceIds[index]
#     print "selected vm is: ", vm
#     return vm
#
#
# def Migrate(instanceId, hostId):
#     vm_lists = Get_Vms_On_Host(Host_Name_To_Id(hostId))
#     if instanceId in vm_lists:
#         print "vm already in dest host..."
#         return
#     hostName = hostId
#     print "migrate: " + instanceId + " to " + hostName
#     nova = Nova()
#     nova.liveMigration(instanceId, hostName)
#
#
# def Resource_Id_To_Name(hostId):
#     return hostId.split('_')[0]
#
#
# def Host_Name_To_Id(hostName):
#     return "%s_%s" % (hostName, hostName)


if __name__ == "__main__":
    print "this is external function..."
    Migrate('compute1', '7d01bee3-52ab-4e2f-acbf-9508cd2769c4', 'compute2')
    print hostHasInstanceType('compute1', 'master')
    print last_n_avg_statistic('compute1', 'cpu_util', 2)
    print getTimeDelay('compute1', 'compute2')
    print getVmHost('7d01bee3-52ab-4e2f-acbf-9508cd2769c4')
    print hostPredictData('compute1', 'cpu_util', 2, 'avg')
    print getAllHost('7d01bee3-52ab-4e2f-acbf-9508cd2769c4')
    print hostFilter(['compute1', 'compute2'], 'hostHasInstanceType($HOST, "master") >0', 'select')
    print hostFilter(['compute1', 'compute2'], 'last_n_avg_statistic($HOST, "cpu_util", 2) < 85', 'filter')
    print hostRankFilter(['compute1', 'compute2'], 'compute1', "getTimeDelay($HOST, $MASTER)")

    # generateEvent('evacuation', '1212', 'master')
    # properties = '{"cpu_util" : {"min" : 0.5, "max" : 70}}'
    # Host_Set_Threshold("compute1_compute1", "cpu_util" , 5, properties)
    # test = {'a' : 1, 'b' : 2, 'c' : 0}
    # print sorted(test.items(), lambda x,y : cmp(x[1], y[1]))
    # print Host_CpuUtil_Cost('compute1')
    # print Host_CpuUtil_Cost('compute2')
    # print simple_host_filter()
    # hosts = '["compute1", "compute2"]'
    # costFunctions = '["Host_CpuUtil_Cost"]'
    # factors = '[1]'
    # list =  Get_Vms_On_Host('compute2')
    # Migrate("5bdbf476-f046-4986-9e1d-5b078414a298", "compute1")
    # properties = '{"compute.node.cpu.percent" : {"min" : 0.5, "max" : 70}}'
    # print Host_Filter("['compute1','compute2']", properties)
    # vms = Get_Vms_On_Host("compute2")
    # print Vm_Random_Selector(vms)
