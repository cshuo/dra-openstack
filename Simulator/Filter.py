__author__ = 'pike'

import random
from Entity import ResourceType

############################################### filter ###############################################
def filter_instance_type(instance_list, instanceType):
    list = []
    for instanceId in instance_list:
        instance = instance_list[instanceId]
        if instance.getType() == instanceType:
            list.append(instance)
    if len(list) == 0:
        return None
    index = random.randint(0, len(list) - 1)
    return list[index]



def filter_host_instanceType(host_list, instanceType, flag):
    result = []

    if type(host_list) == list:
        temp = {}
        for host in host_list:
            temp[host.getId()] = host
        host_list = temp

    for hostId in host_list:
        host = host_list[hostId]
        if host.getInstanceNum(instanceType) > 0 and flag:
            result.append(host)
        if host.getInstanceNum(instanceType) == 0 and not flag:
            result.append(host)
    return result

def filter_host_containsFile(host_list, file, flag):
    result = []

    if type(host_list) == list:
        temp = {}
        for host in host_list:
            temp[host.getId()] = host
        host_list = temp

    for hostId in host_list:
        host = host_list[hostId]
        if host.containsFile(file) and flag:
            result.append(host)
        if not host.containsFile(file) and not flag:
            result.append(host)
    return result

# less than threshold
def filter_host_cpu(host_list, flag, time_count, interval, threshold):
    result = []
    for hostId in host_list:
        host = host_list[hostId]
        cpu = host.getStatisticData(flag, ResourceType.CPU_UTIL, time_count, interval)
        if cpu < threshold :
            result.append(host)
    return result

# less than threshold
def filter_host_bandwidth(host_list, flag, time_count, interval, threshold):
    result = []
    for hostId in host_list:
        host = host_list[hostId]
        bandwidth = host.getStatisticData(flag, ResourceType.BANDWIDTH, time_count, interval)
        if bandwidth < threshold :
            result.append(host)
    return result

# instance no more than num
def filter_host_instanceNum(host_list, num, type):
    result = []
    for hostId in host_list:
        host = host_list[hostId]
        instanceNum = host.getInstanceNum(type)
        if instanceNum < num:
            result.append(host)
    return result
