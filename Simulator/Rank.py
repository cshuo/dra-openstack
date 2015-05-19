__author__ = 'pike'

import random
from Conf import *
from Util import getDistance

############################################### rank ###############################################
def select_host_max_instance(host_list, instanceType):
    if type(host_list) == list:
        temp = {}
        for host in host_list:
            temp[host.getId()] = host
        host_list = temp

    result_host = None
    max = 0
    for hostId in host_list:
        host = host_list[hostId]
        if host.getInstanceNum(instanceType) >= max:
            result_host = host
            max = host.getInstanceNum(instanceType)
    return result_host

def select_host_min_instance(host_list, instanceType):
    if type(host_list) == list:
        temp = {}
        for host in host_list:
            temp[host.getId()] = host
        host_list = temp

    result_host = None
    min = 10000
    for hostId in host_list:
        host = host_list[hostId]
        if host.getInstanceNum(instanceType) <= min and host.getInstanceNum(instanceType) != 0:
            result_host = host
            min = host.getInstanceNum(instanceType)
    return result_host

def select_instance_random(host, instanceType):
    instances = host.getInstance(instanceType)
    if len(instances) == 0:
        return None
    index = random.randint(0, len(instances) - 1)
    return instances[index]

def select_instance_random_1(host, instanceType, flag):
    if not flag:
        return
    instances = host.instanceList
    list = []
    for instanceId in instances:
        instance = instances[instanceId]
        if instance.getType() != instanceType:
            list.append(instance)

    if len(list) == 0:
        return None
    index = random.randint(0, len(list) - 1)
    return list[index]

def select_host_random(host_list):
    index = random.randint(0, len(host_list) - 1)
    return host_list[index]

def select_host_min_cpu(host_list, flag, time_count, interval):
    minCpu = 1000
    resultHost = None

    for host in host_list:
        cpu = host.getStatisticData(flag, ResourceType.CPU_UTIL, time_count, interval)
        if cpu < minCpu:
            minCpu = cpu
            resultHost = host
    return resultHost

def select_host_max_cpu(host_list, flag, time_count, interval):
    maxCpu = 0
    resultHost = None

    for host in host_list:
        cpu = host.getStatisticData(flag, ResourceType.CPU_UTIL, time_count, interval)
        if cpu > maxCpu:
            maxCpu = cpu
            resultHost = host
    return resultHost

def select_host_min_bandwidth(host_list, flag, time_count, interval):
    minBandwidth = 10000
    resultHost = None

    if type(host_list) == list:
        temp = {}
        for host in host_list:
            temp[host.getId()] = host
        host_list = temp

    for hostId in host_list:
        host = host_list[hostId]
        bandwidth = host.getStatisticData(flag, ResourceType.BANDWIDTH, time_count, interval)
        if bandwidth < minBandwidth:
            minBandwidth = bandwidth
            resultHost = host
    return resultHost

def select_host_max_bandwidth(host_list, flag, time_count, interval):
    maxBandwidth = 0
    resultHost = None

    for host in host_list:
        bandwidth = host.getStatisticData(flag, ResourceType.BANDWIDTH, time_count, interval)
        if bandwidth > maxBandwidth:
            maxBandwidth = bandwidth
            resultHost = host
    return resultHost


# select the best host : rank = cpuutil - distance * 50
def select_host_cpu_distance(host, host_list, distance_matrix, flag, time_count, interval):
    maxRank = -1000
    resultHost = None
    for destHost in host_list :
        #distance
        srcHostIndex = host_mapper[host.getId()]
        destHostIndex = host_mapper[destHost.getId()]
        distance = distance_matrix[srcHostIndex][destHostIndex]

        #cpuutil
        cpu = destHost.getStatisticData(flag, ResourceType.CPU_UTIL, time_count, interval)

        rank = cpu - distance * 50
        if rank > maxRank:
            resultHost = destHost
            maxRank = rank
    return resultHost

def select_host_file_distance_max(file_host_list, host_list, distance_matrix):
    result = None
    maxRank = -1000
    for host in host_list:
        totalDistance = 0
        for file_host in file_host_list:
            totalDistance += getDistance(file_host, host, distance_matrix)
        if totalDistance >= maxRank:
            result = host
            maxRank = totalDistance
    return result

def select_host_file_distance_min(file_host_list, host_list, distance_matrix):
    result = None
    minRank = 1000
    for host in host_list:
        totalDistance = 0
        for file_host in file_host_list:
            totalDistance += getDistance(file_host, host, distance_matrix)
        if totalDistance <= minRank:
            result = host
            minRank = totalDistance
    return result


