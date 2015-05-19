__author__ = 'pike'

from Conf import *

def getTotalDistance(instance_list):
    totalDistance = 0

    instance_master_1 = instance_list['instance_master_1']
    instance_master_2 = instance_list['instance_master_2']

    host_1 = instance_master_1.getHost()
    host_2 = instance_master_2.getHost()

    for instanceId in instance_list:
        instance = instance_list[instanceId]
        if instance.getType() == InstanceType.MATLAB_1:
            host = instance.getHost()
            distance = host_distance_matrix[host_mapper[host_1.getId()]][host_mapper[host.getId()]]
            totalDistance += distance
        elif instance.getType() == InstanceType.MATLAB_2:
            host = instance.getHost()
            distance = host_distance_matrix[host_mapper[host_2.getId()]][host_mapper[host.getId()]]
            totalDistance += distance
    return totalDistance


def getMatlabDistance(instance_list):
    totalDistance = 0

    instance_master_1 = instance_list['instance_16']

    host_1 = instance_master_1.getHost()

    for instanceId in instance_list:
        instance = instance_list[instanceId]
        if instance.getType() == InstanceType.MATLAB_1:
            host = instance.getHost()
            distance = host_distance_matrix[host_mapper[host_1.getId()]][host_mapper[host.getId()]]
            totalDistance += distance
    return totalDistance

def getTotalFileDistance(instance_list):
    totalDistance = 0
    for instanceId in instance_list:
        instance = instance_list[instanceId]
        host = instance.getHost()
        fileHostList = instance.getFileHostList()
        fileHost1 = fileHostList[0]
        fileHost2 = fileHostList[1]
        totalDistance += getDistance(host, fileHost1, host_distance_matrix) + getDistance(host, fileHost2, host_distance_matrix)
    return totalDistance

def getDistance(host1, host2, distance_matrix):
    index1 = host_mapper[host1.getId()]
    index2 = host_mapper[host2.getId()]
    return distance_matrix[index1][index2]

def getHadoopDistance(instance_list):
    totalDistance = 0
    for instanceId in instance_list:
        instance = instance_list[instanceId]
        if instance.getType() != InstanceType.HADOOP:
            continue
        host = instance.getHost()
        fileHostList = instance.getFileHostList()
        fileHost1 = fileHostList[0]
        fileHost2 = fileHostList[1]
        totalDistance += getDistance(host, fileHost1, host_distance_matrix) + getDistance(host, fileHost2, host_distance_matrix)
    return totalDistance

def getHostsMapper(host_list):
    dictValue = {}
    for hostId in host_list:
        host = host_list[hostId]
        instanceList = host.instanceList
        listValue = []
        for instanceId in instanceList:
            instance = instanceList[instanceId]
            listValue.append({'type' : instance.getType(), 'name' : instance.getId()})
        dictValue[hostId] = listValue
    return {'type' : 'hosts', 'value' : dictValue}

def display(host_list):
    print '\n'
    for hostId in host_list:
        print '###########' + hostId + '###########'
        instanceList = host_list[hostId].getInstance(InstanceType.ALL)
        for instance in instanceList:
            print instance.getId() + '\t' + str(instance.getType())
    print '\n'


def getStatus(game_migration):
        x = [0]
        y = [10]
        #[24, 24, 26, 33, 34, 34, 36, 39, 40, 40, 42, 44, 46, 63, 64, 64, 65, 65, 66, 70, 74, 78]


        i = 0
        while i < len(game_migration):
            t = game_migration[i]

            k = i + 1
            i = k
            mul = 1
            while k < len(game_migration) and game_migration[k] == t:
                mul += 1
                k += 1
                i = k

            x.append(t)
            y.append(10)
            x.append(t)
            y.append(0)
            x.append(t + 0.2 * mul)
            y.append(0)
            x.append(t + 0.2 * mul)
            y.append(10)
        return (x, y)