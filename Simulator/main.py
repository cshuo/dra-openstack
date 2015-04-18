__author__ = 'pike'

# in our simulation, the workload refers to the load of each hour in a day, and is periodical
# each host has 24 vcpu and allocate 2 vcpu to each instance
# each host has 1G bandwidth each instance usually use 100M

import threading
import random
import matplotlib.pyplot as plt

import tornado.web
import tornado.ioloop
import tornado.websocket

import threading
import time
import json

from Utils.SshUtil import Ssh_tool

exp = 5

#global host and instance list
host_list = {}
instance_list = {}
time_count = 0

host_distance_matrix = [[0.5, 2, 3, 4],
                        [2, 0.5, 2, 3],
                        [3, 2, 0.5, 2],
                        [4, 3, 2, 0.5]]


host_mapper = {'host_1' : 0, 'host_2' : 1, 'host_3' : 2, 'host_4' : 3}

game_migration = []
storage_migration = []

#enum
class ResourceType:
    (CPU_UTIL, BANDWIDTH, DISK_IO) = ('CPU_UTIL', 'BANDWIDTH', 'DISK_IO')

class InstanceType:
    (ALL, MATLAB_1, MATLAB_1_MASTER, MATLAB_2, MATLAB_2_MASTER, WEB_SERVER_1, GAME_1, STORAGE_1, HADOOP) = ('ALL', 'MATLAB', 'MATLAB_MASTER', 'MATLAB_2', 'MATLAB_2_MASTER', 'WEB_SERVER_1', 'GAME', 'STORAGE_1', 'HADOOP')

############################################### base entity ###############################################

class Host(object):
    def __init__(self, hostId, host_list):
        self.id = hostId
        self.vCpu = 24
        self.bandwidth = 1000
        self.instanceList = {}

        #add to host_list
        host_list[self.id] = self

        #use lock to ensure one thread modify the instanceList
        self.lock = threading.RLock()

    def getId(self):
        return self.id

    def addInstance(self, instance):
        self.lock.acquire()
        self.instanceList[instance.getId()] = instance
        self.lock.release()

    def removeInstance(self, instance):
        self.lock.acquire()
        del self.instanceList[instance.getId()]
        self.lock.release()

    def getInstanceNum(self, instanceType):
        return len(self.getInstance(instanceType))

    def getInstance(self, instanceType):
        result = []
        for instanceId in self.instanceList:
            instance = self.instanceList[instanceId]
            if instanceType == InstanceType.ALL:
                result.append(instance)
            elif instance.getType() == instanceType:
                result.append(instance)
        return result

    def getStatisticData(self, flag, resourceType, time, interval):
        if resourceType == ResourceType.CPU_UTIL:
            total = 0
            for instanceId in self.instanceList:
                instance = self.instanceList[instanceId]
                total += instance.getStatisticData(flag, resourceType, time, interval)
            return total / (self.vCpu / 2)
        elif resourceType == ResourceType.BANDWIDTH:
            total = 0
            for instanceId in self.instanceList:
                instance = self.instanceList[instanceId]
                total += instance.getStatisticData(flag, resourceType, time, interval)
            return total
        elif resourceType == ResourceType.DISK_IO:
            pass
        else:
            print 'invalid resourceType'
            return None



class Instance(object):
    def __init__(self, instanceId, instanceType, host, instance_list):
        self.id = instanceId
        self.type = instanceType

        #add instance to host
        self.host = host
        self.host.addInstance(self)

        #add instance to instance_list
        instance_list[self.id] = self

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def getHost(self):
        return self.host

    def setHost(self, host):
        self.host = host

    def getStatisticData(self, flag, resourceType, time, interval):
        # judge the resource type
        generateFunc = None
        if resourceType == ResourceType.CPU_UTIL:
            generateFunc = self.generateCpuUtil
        elif resourceType == ResourceType.BANDWIDTH:
            generateFunc = self.generateBandwidth
        elif resourceType == ResourceType.DISK_IO:
            generateFunc = self.generateDiskIo
        else:
            print 'getAvgCpuUtil type error'
            return None

        result = 0
        #predict future data
        if flag == 'future':
            for i in range(interval):
                result += generateFunc(time + i)
            result = result / interval
        #analyze history data
        elif flag == 'history':
            for i in range(interval):
                result += generateFunc(time - i)
            result = result / interval
        else:
            print 'not a valid flag'
            return None
        return result

    def generateCpuUtil(self, time):
        return None

    def generateBandwidth(self, time):
        return None

    def generateDiskIo(self, time):
        return None


############################################### specific entity ###############################################

class Instance_Matlab_1(Instance):
    # time refers to the time point in a day (0-24)
    def __init__(self, instanceId, instanceType, host, instance_list):
        super(Instance_Matlab_1, self).__init__(instanceId, instanceType, host, instance_list)
        self.cpu = [95, 95, 95, 95, 95, 95,
                    95, 95, 95, 95, 95, 95,
                    95, 95, 95, 95, 95, 95,
                    95, 95, 95, 95, 95, 95]

        self.bandwidth = [30, 30, 30, 30, 30, 30,
                          40, 40, 40, 40, 40, 40,
                          30, 30, 30, 30, 30, 30,
                          40, 40, 40, 40, 40, 40,]

    def generateCpuUtil(self, time):
        result = self.cpu[time % 24] + random.randint(0, 5)
        return result

    def generateBandwidth(self, time):
        result = self.bandwidth[time % 24] + random.randint(0, 5)
        return result

class Instance_Matlab_2(Instance):
    def __init__(self, instanceId, instanceType, host, instance_list):
        super(Instance_Matlab_2, self).__init__(instanceId, instanceType, host, instance_list)
        self.cpu = [95, 95, 95, 95, 95, 95,
                    95, 95, 95, 95, 95, 95,
                    95, 95, 95, 95, 95, 95,
                    95, 95, 95, 95, 95, 95]

    def generateCpuUtil(self, time):
        result = self.cpu[time % 24] + random.randint(0, 5)
        return result

class Instance_WebServer_1(Instance):
    def __init__(self, instanceId, instanceType, host, instance_list):
        super(Instance_WebServer_1, self).__init__(instanceId, instanceType, host, instance_list)
        self.cpu = [20, 20, 20, 20, 20, 20,
                    30, 40, 60, 80, 70, 60,
                    60, 80, 80, 80, 60, 50,
                    50, 40, 40, 30, 30, 20]
    def generateCpuUtil(self, time):
        return self.cpu[time % 24] + random.randint(-5, 5)

class Instance_Game_1(Instance):
    def __init__(self, instanceId, instanceType, host, instance_list):
        super(Instance_Game_1, self).__init__(instanceId, instanceType, host, instance_list)
        self.bandwidth = [70, 55, 50, 45, 40, 35,
                          35, 35, 40, 40, 40, 45,
                          45, 50, 50, 60, 70, 80,
                          90, 95, 95, 95, 95, 85]
        self.cpu = [50, 35, 30, 25, 20, 15,
                    15, 15, 20, 20, 20, 25,
                    25, 30, 30, 40, 50, 60,
                    70, 75, 75, 75, 75, 65]

    def generateCpuUtil(self, time):
        return self.cpu[time % 24] + random.randint(-5, 5)

    def generateBandwidth(self, time):
        return self.bandwidth[time % 24] + random.randint(-5, 5)

class Instance_Storage_1(Instance):
    def __init__(self, instanceId, instanceType, host, instance_list):
        super(Instance_Storage_1, self).__init__(instanceId, instanceType, host, instance_list)
        self.bandwidth = [45, 40, 40, 40, 40, 40,
                          50, 50, 50, 55, 60, 60,
                          60, 70, 70, 65, 65, 70,
                          70, 70, 70, 70, 60, 50]
    def generateBandwidth(self, time):
        return self.bandwidth[time % 24] + random.randint(-5, 5)
    def generateDiskIo(self, time):
        pass

class Instance_Hadoop(Instance):
    def __init__(self, instanceId, instanceType, host, instance_list):
        super(Instance_Hadoop, self).__init__(instanceId, instanceType, host, instance_list)

        self.cpu = [30, 30, 30, 30, 30, 30,
                    40, 40, 40, 40, 40, 40,
                    30, 30, 30, 30, 30, 30,
                    40, 40, 40, 40, 40, 40,]

        self.bandwidth = [40, 40, 40, 40, 40, 40,
                          50, 50, 50, 50, 50, 50,
                          40, 40, 40, 40, 40, 40,
                          50, 50, 50, 50, 50, 50,]

    def generateCpuUtil(self, time):
        return self.cpu[time % 24] + random.randint(-5, 5)

    def generateBandwidth(self, time):
        return self.bandwidth[time % 24] + random.randint(-5, 5)

    def setFileHostList(self, hostList):
        self.hostList = hostList

    def getFileHostList(self):
        return self.hostList

class Host_Hadoop(Host):
    def __init__(self, hostId, host_list):
        super(Host_Hadoop, self).__init__(hostId, host_list)
        self.fileList = []

    def addFile(self, file):
        self.fileList.append(file)

    def containsFile(self, file):
        if file in self.fileList:
            return True
        else:
            return False



############################################### filter ###############################################
def filter_instance_type(instanceType):
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


def getDistance(host1, host2, distance_matrix):
    index1 = host_mapper[host1.getId()]
    index2 = host_mapper[host2.getId()]
    return distance_matrix[index1][index2]


############################################### migrate ###############################################
def migrate_instance(srcHost, destHost, instance):
        if not instance:
            print 'no instance to migrate'
            return
        if srcHost.getId() == destHost.getId():
            return
        if srcHost == None or destHost == None:
            print 'no host to migrate'
            return
        srcHost.removeInstance(instance)
        destHost.addInstance(instance)
        instance.setHost(destHost)
        print '%s\t==>\t%s\t==>\t%s' % (srcHost.id, instance.getId(), destHost.getId())

        if instance.getType() == InstanceType.GAME_1:
            global game_migration_num
            game_migration.append(time_count)
        if instance.getType() == InstanceType.STORAGE_1:
            global storage_migration_num
            storage_migration.append(time_count)

############################################### work thread ###############################################

def matlab_1_consolidate(period):
    if (time_count % period == 0):
        #srcHost = select_host_min_instance(host_list, InstanceType.MATLAB_1)
        #migrateInstance = select_instance_random(srcHost, InstanceType.MATLAB_1)
        #destHost = select_host_max_instance(host_list, InstanceType.MATLAB_1)
        #migrate_instance(srcHost, destHost, migrateInstance)
        src_host_list = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, False)
        src_host_list = filter_host_instanceType(src_host_list, InstanceType.MATLAB_1, True)
        #srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        srcHost = select_host_random(src_host_list)

        migrateInstance = select_instance_random(srcHost, InstanceType.MATLAB_1)

        masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)

        migrate_instance(srcHost, destHost, migrateInstance)

def matlab_2_consolidate(period):
    if (time_count % period == 0):
        src_host_list = filter_host_instanceType(host_list, InstanceType.MATLAB_2_MASTER, False)
        src_host_list = filter_host_instanceType(src_host_list, InstanceType.MATLAB_2, True)
        #srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        srcHost = select_host_random(src_host_list)

        migrateInstance = select_instance_random(srcHost, InstanceType.MATLAB_2)

        masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_2_MASTER, True)[0]
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)

        migrate_instance(srcHost, destHost, migrateInstance)

def matlab_1_consolidate_comparison(period):
    if (time_count % period == 0):
        src_host_list = filter_host_instanceType(host_list, InstanceType.ALL, True)
        srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_max_cpu(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)

def matlab_2_consolidate_comparison(period):
    if (time_count % period == 0):
        src_host_list = filter_host_instanceType(host_list, InstanceType.ALL, True)
        srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_max_cpu(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)


def game_1_guarantee_qos(period):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                srcHost = host
                migrateInstance = select_instance_random(host, InstanceType.STORAGE_1)
                destHost = select_host_random(filter_host_instanceType(host_list, InstanceType.GAME_1, False))
                migrate_instance(srcHost, destHost, migrateInstance)

def storage_1_consolidation(period):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) < 600:
                srcHost = select_host_random(filter_host_instanceType(host_list, InstanceType.GAME_1, False))
                migrateInstance = select_instance_random(srcHost, InstanceType.STORAGE_1)
                destHost = host
                migrate_instance(srcHost, destHost, migrateInstance)

def game_1_guarantee_qos_old(period):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                srcHost = host
                migrateInstance = select_instance_random(host, InstanceType.ALL)
                dest_host_list = filter_host_bandwidth(host_list, 'future', time_count, 2, 600)
                destHost = select_host_min_bandwidth(dest_host_list, 'future', time_count, 2)
                migrate_instance(srcHost, destHost, migrateInstance)

def storage_1_consolidation_old(period):
    if (time_count % period == 0):
        srcHost = select_host_min_bandwidth(host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_bandwidth(host_list, 'future', time_count, 2, 600)
        destHost = select_host_max_bandwidth(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)

def hadoop_consolidation(period, tmpInstance):
    if (time_count % period == 0):
        #for instanceId in instance_list:
        for i in range(4):
            if len(tmpInstance) == 0: break
            instanceId = tmpInstance.pop()
            instance = instance_list[instanceId]
            file_host_list = instance.getFileHostList()

            #file_host1 = filter_host_containsFile(host_list, fileList[0], True)[0]
            #file_host2 = filter_host_containsFile(host_list, fileList[1], True)[0]

            #file_host_list = [file_host1, file_host2]

            #srcHostList = filter_host_instanceType(host_list, InstanceType.HADOOP, True)
            #srcHost = select_host_file_distance_max(file_host_list, srcHostList, host_distance_matrix)
            srcHost = instance.getHost()

            #migrateInstance = select_instance_random(srcHost, InstanceType.HADOOP)
            migrateInstance = instance

            srcHost.removeInstance(migrateInstance)

            destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
            destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)

            srcHost.addInstance(migrateInstance)

            #if srcHost.getInstanceNum(InstanceType.HADOOP) == 8:
            #    return

            migrate_instance(srcHost, destHost, migrateInstance)

def hadoop_consolidation_old(period):
    if (time_count % period == 0):
        srcHostList = filter_host_instanceType(host_list, InstanceType.HADOOP, True)
        srcHost = select_host_min_instance(srcHostList, InstanceType.HADOOP)

        migrateInstance = select_instance_random(srcHost, InstanceType.HADOOP)

        destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
        destHost = select_host_max_instance(destHostList, InstanceType.HADOOP)

        if srcHost.getInstanceNum(InstanceType.HADOOP) == 8:
            return

        migrate_instance(srcHost, destHost, migrateInstance)


def getTotalDistance():
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
            print totalDistance
        elif instance.getType() == InstanceType.MATLAB_2:
            host = instance.getHost()
            distance = host_distance_matrix[host_mapper[host_2.getId()]][host_mapper[host.getId()]]
            totalDistance += distance
            print totalDistance
    return totalDistance

def getMatlabDistance():
    totalDistance = 0

    instance_master_1 = instance_list['instance_16']

    host_1 = instance_master_1.getHost()

    for instanceId in instance_list:
        instance = instance_list[instanceId]
        if instance.getType() == InstanceType.MATLAB_1:
            host = instance.getHost()
            distance = host_distance_matrix[host_mapper[host_1.getId()]][host_mapper[host.getId()]]
            totalDistance += distance
            print totalDistance
    return totalDistance

def getTotalFileDistance():
    totalDistance = 0
    for instanceId in instance_list:
        instance = instance_list[instanceId]
        host = instance.getHost()
        fileHostList = instance.getFileHostList()
        fileHost1 = fileHostList[0]
        fileHost2 = fileHostList[1]
        totalDistance += getDistance(host, fileHost1, host_distance_matrix) + getDistance(host, fileHost2, host_distance_matrix)
    return totalDistance

def getHadoopDistance():
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

def getHostsMapper():
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


############################################### experiment setup ###############################################

def setup_environment_1():
    host_1 = Host('host_1', host_list)
    host_2 = Host('host_2', host_list)
    host_3 = Host('host_3', host_list)
    host_4 = Host('host_4', host_list)

    instance_master_1 = Instance_Matlab_1('instance_master_1', InstanceType.MATLAB_1_MASTER, host_1, instance_list)
    instance_master_2 = Instance_Matlab_2('instance_master_2', InstanceType.MATLAB_2_MASTER, host_2, instance_list)

    instance_1 = Instance_Matlab_1('instance_1', InstanceType.MATLAB_1, host_1, instance_list)
    instance_2 = Instance_Matlab_1('instance_2', InstanceType.MATLAB_1, host_1, instance_list)
    instance_3 = Instance_Matlab_1('instance_3', InstanceType.MATLAB_1, host_4, instance_list)
    instance_4 = Instance_Matlab_1('instance_4', InstanceType.MATLAB_1, host_2, instance_list)
    instance_5 = Instance_Matlab_1('instance_5', InstanceType.MATLAB_1, host_2, instance_list)
    instance_6 = Instance_Matlab_1('instance_6', InstanceType.MATLAB_1, host_4, instance_list)
    instance_7 = Instance_Matlab_1('instance_7', InstanceType.MATLAB_1, host_3, instance_list)
    instance_8 = Instance_Matlab_1('instance_8', InstanceType.MATLAB_1, host_3, instance_list)
    instance_9 = Instance_Matlab_1('instance_9', InstanceType.MATLAB_1, host_3, instance_list)
    instance_10 = Instance_Matlab_1('instance_10', InstanceType.MATLAB_1, host_4, instance_list)
    instance_11 = Instance_Matlab_1('instance_11', InstanceType.MATLAB_1, host_4, instance_list)
    instance_12 = Instance_Matlab_1('instance_12', InstanceType.MATLAB_1, host_4, instance_list)

    instance_13 = Instance_Matlab_2('instance_13', InstanceType.MATLAB_2, host_1, instance_list)
    instance_14 = Instance_Matlab_2('instance_14', InstanceType.MATLAB_2, host_1, instance_list)
    instance_15 = Instance_Matlab_2('instance_15', InstanceType.MATLAB_2, host_4, instance_list)
    instance_16 = Instance_Matlab_2('instance_16', InstanceType.MATLAB_2, host_2, instance_list)
    instance_17 = Instance_Matlab_2('instance_17', InstanceType.MATLAB_2, host_2, instance_list)
    instance_18 = Instance_Matlab_2('instance_18', InstanceType.MATLAB_2, host_4, instance_list)
    instance_19 = Instance_Matlab_2('instance_19', InstanceType.MATLAB_2, host_3, instance_list)
    instance_20 = Instance_Matlab_2('instance_20', InstanceType.MATLAB_2, host_3, instance_list)
    instance_21 = Instance_Matlab_2('instance_21', InstanceType.MATLAB_2, host_3, instance_list)
    instance_22 = Instance_Matlab_2('instance_22', InstanceType.MATLAB_2, host_4, instance_list)
    instance_23 = Instance_Matlab_2('instance_23', InstanceType.MATLAB_2, host_4, instance_list)
    instance_24 = Instance_Matlab_2('instance_24', InstanceType.MATLAB_2, host_4, instance_list)

def setup_environment_2():
    host_1 = Host('host_1', host_list)
    host_2 = Host('host_2', host_list)
    host_3 = Host('host_3', host_list)
    host_4 = Host('host_4', host_list)

    instance_1 = Instance_Game_1('instance_1', InstanceType.GAME_1, host_1, instance_list)
    instance_2 = Instance_Game_1('instance_2', InstanceType.GAME_1, host_1, instance_list)
    instance_3 = Instance_Game_1('instance_3', InstanceType.GAME_1, host_1, instance_list)
    instance_4 = Instance_Game_1('instance_4', InstanceType.GAME_1, host_1, instance_list)
    instance_5 = Instance_Game_1('instance_5', InstanceType.GAME_1, host_1, instance_list)
    instance_6 = Instance_Game_1('instance_6', InstanceType.GAME_1, host_1, instance_list)
    instance_7 = Instance_Game_1('instance_7', InstanceType.GAME_1, host_1, instance_list)
    instance_8 = Instance_Game_1('instance_8', InstanceType.GAME_1, host_2, instance_list)
    instance_9 = Instance_Game_1('instance_9', InstanceType.GAME_1, host_2, instance_list)
    instance_10 = Instance_Game_1('instance_10', InstanceType.GAME_1, host_2, instance_list)
    instance_11 = Instance_Game_1('instance_11', InstanceType.GAME_1, host_2, instance_list)
    instance_12 = Instance_Game_1('instance_12', InstanceType.GAME_1, host_2, instance_list)
    instance_13 = Instance_Game_1('instance_13', InstanceType.GAME_1, host_2, instance_list)
    instance_14 = Instance_Game_1('instance_14', InstanceType.GAME_1, host_2, instance_list)
    instance_15 = Instance_Game_1('instance_15', InstanceType.GAME_1, host_2, instance_list)

    instance_16 = Instance_Storage_1('instance_16', InstanceType.STORAGE_1, host_1, instance_list)
    instance_17 = Instance_Storage_1('instance_17', InstanceType.STORAGE_1, host_1, instance_list)
    instance_18 = Instance_Storage_1('instance_18', InstanceType.STORAGE_1, host_1, instance_list)
    instance_19 = Instance_Storage_1('instance_19', InstanceType.STORAGE_1, host_1, instance_list)
    instance_20 = Instance_Storage_1('instance_20', InstanceType.STORAGE_1, host_1, instance_list)
    instance_21 = Instance_Storage_1('instance_21', InstanceType.STORAGE_1, host_1, instance_list)
    instance_22 = Instance_Storage_1('instance_22', InstanceType.STORAGE_1, host_1, instance_list)
    instance_23 = Instance_Storage_1('instance_23', InstanceType.STORAGE_1, host_2, instance_list)
    instance_24 = Instance_Storage_1('instance_24', InstanceType.STORAGE_1, host_2, instance_list)
    instance_25 = Instance_Storage_1('instance_25', InstanceType.STORAGE_1, host_2, instance_list)
    instance_26 = Instance_Storage_1('instance_26', InstanceType.STORAGE_1, host_2, instance_list)
    instance_27 = Instance_Storage_1('instance_27', InstanceType.STORAGE_1, host_2, instance_list)
    instance_28 = Instance_Storage_1('instance_28', InstanceType.STORAGE_1, host_2, instance_list)
    instance_29 = Instance_Storage_1('instance_29', InstanceType.STORAGE_1, host_2, instance_list)
    instance_30 = Instance_Storage_1('instance_30', InstanceType.STORAGE_1, host_2, instance_list)

def setup_environment_3():
    host_1 = Host_Hadoop('host_1', host_list)
    host_2 = Host_Hadoop('host_2', host_list)
    host_3 = Host_Hadoop('host_3', host_list)
    host_4 = Host_Hadoop('host_4', host_list)

    host_1.addFile('file1')
    host_1.addFile('file5')
    host_2.addFile('file2')
    host_2.addFile('file6')
    host_3.addFile('file3')
    host_3.addFile('file7')
    host_4.addFile('file4')
    host_4.addFile('file8')

    instance_1 = Instance_Hadoop('instance_1', InstanceType.HADOOP, host_1, instance_list)
    instance_2 = Instance_Hadoop('instance_2', InstanceType.HADOOP, host_1, instance_list)
    instance_3 = Instance_Hadoop('instance_3', InstanceType.HADOOP, host_2, instance_list)
    instance_4 = Instance_Hadoop('instance_4', InstanceType.HADOOP, host_2, instance_list)
    instance_5 = Instance_Hadoop('instance_5', InstanceType.HADOOP, host_2, instance_list)
    instance_6 = Instance_Hadoop('instance_6', InstanceType.HADOOP, host_3, instance_list)
    instance_7 = Instance_Hadoop('instance_7', InstanceType.HADOOP, host_3, instance_list)
    instance_8 = Instance_Hadoop('instance_8', InstanceType.HADOOP, host_3, instance_list)
    instance_9 = Instance_Hadoop('instance_9', InstanceType.HADOOP, host_3, instance_list)
    instance_10 = Instance_Hadoop('instance_10', InstanceType.HADOOP, host_4, instance_list)
    instance_11 = Instance_Hadoop('instance_11', InstanceType.HADOOP, host_4, instance_list)
    instance_12 = Instance_Hadoop('instance_12', InstanceType.HADOOP, host_4, instance_list)
    instance_13 = Instance_Hadoop('instance_13', InstanceType.HADOOP, host_4, instance_list)
    instance_14 = Instance_Hadoop('instance_14', InstanceType.HADOOP, host_4, instance_list)
    instance_15 = Instance_Hadoop('instance_15', InstanceType.HADOOP, host_4, instance_list)
    instance_16 = Instance_Hadoop('instance_16', InstanceType.HADOOP, host_4, instance_list)

    file_list_1 = [host_2, host_3]
    file_list_2 = [host_2, host_4]
    file_list_3 = [host_1, host_1]

    instance_1.setFileHostList(file_list_1)
    instance_2.setFileHostList(file_list_2)
    instance_3.setFileHostList(file_list_2)
    instance_4.setFileHostList(file_list_3)
    instance_5.setFileHostList(file_list_2)
    instance_6.setFileHostList(file_list_1)
    instance_7.setFileHostList(file_list_3)
    instance_8.setFileHostList(file_list_3)
    instance_9.setFileHostList(file_list_1)
    instance_10.setFileHostList(file_list_1)
    instance_11.setFileHostList(file_list_2)
    instance_12.setFileHostList(file_list_3)
    instance_13.setFileHostList(file_list_2)
    instance_14.setFileHostList(file_list_2)
    instance_15.setFileHostList(file_list_1)
    instance_16.setFileHostList(file_list_3)

def setup_environment_4():
    host_1 = Host_Hadoop('host_1', host_list)
    host_2 = Host_Hadoop('host_2', host_list)
    host_3 = Host_Hadoop('host_3', host_list)
    host_4 = Host_Hadoop('host_4', host_list)

    host_1.addFile('file1')
    host_1.addFile('file5')
    host_2.addFile('file2')
    host_2.addFile('file6')
    host_3.addFile('file3')
    host_3.addFile('file7')
    host_4.addFile('file4')
    host_4.addFile('file8')

    instance_1 = Instance_Game_1('instance_1', InstanceType.GAME_1, host_1, instance_list)
    instance_2 = Instance_Game_1('instance_2', InstanceType.GAME_1, host_1, instance_list)
    instance_3 = Instance_Game_1('instance_3', InstanceType.GAME_1, host_1, instance_list)
    instance_4 = Instance_Game_1('instance_4', InstanceType.GAME_1, host_1, instance_list)
    instance_5 = Instance_Game_1('instance_5', InstanceType.GAME_1, host_1, instance_list)
    instance_6 = Instance_Game_1('instance_6', InstanceType.GAME_1, host_1, instance_list)
    instance_7 = Instance_Game_1('instance_7', InstanceType.GAME_1, host_2, instance_list)
    instance_8 = Instance_Game_1('instance_8', InstanceType.GAME_1, host_2, instance_list)

    instance_9 = Instance_Matlab_1('instance_9', InstanceType.MATLAB_1, host_1, instance_list)
    instance_10 = Instance_Matlab_1('instance_10', InstanceType.MATLAB_1, host_1, instance_list)
    instance_11 = Instance_Matlab_1('instance_11', InstanceType.MATLAB_1, host_4, instance_list)
    instance_12 = Instance_Matlab_1('instance_12', InstanceType.MATLAB_1, host_2, instance_list)
    instance_13 = Instance_Matlab_1('instance_13', InstanceType.MATLAB_1, host_1, instance_list)
    instance_14 = Instance_Matlab_1('instance_14', InstanceType.MATLAB_1, host_4, instance_list)
    instance_15 = Instance_Matlab_1('instance_15', InstanceType.MATLAB_1, host_3, instance_list)
    instance_16 = Instance_Matlab_1('instance_16', InstanceType.MATLAB_1_MASTER, host_3, instance_list)

    instance_17 = Instance_Hadoop('instance_17', InstanceType.HADOOP, host_1, instance_list)
    instance_18 = Instance_Hadoop('instance_18', InstanceType.HADOOP, host_1, instance_list)
    instance_19 = Instance_Hadoop('instance_19', InstanceType.HADOOP, host_2, instance_list)
    instance_20 = Instance_Hadoop('instance_20', InstanceType.HADOOP, host_2, instance_list)
    instance_21 = Instance_Hadoop('instance_21', InstanceType.HADOOP, host_2, instance_list)
    instance_22 = Instance_Hadoop('instance_22', InstanceType.HADOOP, host_3, instance_list)
    instance_23 = Instance_Hadoop('instance_23', InstanceType.HADOOP, host_3, instance_list)
    instance_24 = Instance_Hadoop('instance_24', InstanceType.HADOOP, host_3, instance_list)

    file_list_1 = [host_2, host_3]
    file_list_2 = [host_3, host_4]
    file_list_3 = [host_4, host_4]

    instance_17.setFileHostList(file_list_1)
    instance_18.setFileHostList(file_list_2)
    instance_19.setFileHostList(file_list_2)
    instance_20.setFileHostList(file_list_3)
    instance_21.setFileHostList(file_list_2)
    instance_22.setFileHostList(file_list_1)
    instance_23.setFileHostList(file_list_3)
    instance_24.setFileHostList(file_list_3)

def final_game(period, socket, time_count):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                socket.write_message(json.dumps({'type' : 'event', 'value' : '(host (id %s) (> bandwidth 700))' % host.getId()}))

                srcHost = host
                socket.write_message(json.dumps({'type' : 'action', 'value' : 'srcHost = %s' % host.getId()}))

                migrateInstance = select_instance_random_1(host, InstanceType.GAME_1, True)
                socket.write_message(json.dumps({'type' : 'action', 'value' : 'migrateInstance = %s' % migrateInstance.getId()}))

                destHost = None

                if migrateInstance.getType() == InstanceType.HADOOP:
                    socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s evacuate)' % migrateInstance.getId()}))
                    file_host_list = migrateInstance.getFileHostList()
                    destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))
                    destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min_file_distance'}))
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

                if migrateInstance.getType() == InstanceType.MATLAB_1:
                    socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s evacuate)' % migrateInstance.getId()}))
                    masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]
                    dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))
                    destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min cpu distance'}))
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

                migrate_instance(srcHost, destHost, migrateInstance)
                socket.write_message(json.dumps({'type' : 'action', 'value' : '%s ==> %s ==> %s' % (srcHost.getId(), migrateInstance.getId(), destHost.getId())}))
                socket.write_message(json.dumps(getHostsMapper()))
                print json.dumps(getHostsMapper())

def final_hadoop(period, socket, time_count):
    if (time_count % period == 0):
        instance = filter_instance_type(InstanceType.HADOOP)
        socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s hadoop)' % instance.getId()}))
        srcHost = instance.getHost()
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'srcHost = %s' % srcHost.getId()}))

        file_host_list = instance.getFileHostList()
        destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))

        destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min_file_distance'}))
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

        if destHost.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700 and destHost.getInstanceNum(InstanceType.GAME_1) > 0:
            return
        migrate_instance(srcHost, destHost, instance)
        socket.write_message(json.dumps({'type' : 'action', 'value' : '%s ==> %s ==> %s' % (srcHost.getId(), instance.getId(), destHost.getId())}))
        socket.write_message(json.dumps({'type' : 'hosts', 'value' : getHostsMapper()}))
        #print json.dumps(getHostsMapper())



def final_matlab(period, socket, time_count):
    if (time_count % period == 0):
        instance = filter_instance_type(InstanceType.MATLAB_1)
        socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s matlab)' % instance.getId()}))
        srcHost = instance.getHost()
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'srcHost = %s' % srcHost.getId()}))

        masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))

        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min cpu distance'}))
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

        if destHost.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700 and destHost.getInstanceNum(InstanceType.GAME_1) > 0:
            return
        migrate_instance(srcHost, destHost, instance)
        socket.write_message(json.dumps({'type' : 'action', 'value' : '%s ==> %s ==> %s' % (srcHost.getId(), instance.getId(), destHost.getId())}))
        socket.write_message(json.dumps(getHostsMapper()))


def final_game_old(period):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                srcHost = host
                migrateInstance = select_instance_random_1(host, InstanceType.GAME_1, True)
                destHost = select_host_random(filter_host_instanceType(host_list, InstanceType.GAME_1, False))
                migrate_instance(srcHost, destHost, migrateInstance)

def final_consolidation(period):
    if (time_count % period == 0):
        srcHost = select_host_min_bandwidth(host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_bandwidth(host_list, 'future', time_count, 2, 600)
        destHost = select_host_max_bandwidth(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)



def display(host_list):
    print '\n'
    for hostId in host_list:
        print '###########' + hostId + '###########'
        instanceList = host_list[hostId].getInstance(InstanceType.ALL)
        for instance in instanceList:
            print instance.getId() + '\t' + str(instance.getType())
    print '\n'




############################################ WEBSOCKET ############################################
class Index(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
<head>
<script>
var ws = new WebSocket('ws://localhost:9008/soc');
ws.onmessage = function(event) {
    document.getElementById('message').innerHTML = event.data;
};
</script>
</head>
<body>
<p id='message'></p>
        ''')


class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message('Welcome to WebSocket')

        thread = DataPusher(self)
        thread.start()


class DataPusher(threading.Thread):

    def __init__(self, socketHandler):
        super(DataPusher, self).__init__()
        self.socketHandler = socketHandler
        self.sshTool = Ssh_tool("114.212.189.134", 22, "root", "njuics08")

        self.count = 0

    def pushGmetric(self, name, value, host):
        cmd = "gmetric --name %s  --value %d --type uint32 --spoof %s" % (name, value, host)
        print cmd
        self.sshTool.remote_cmd(cmd)

    def pushEvent(self, type, info):
        self.socketHandler.write_message()

    def run(self):
        setup_environment_4()
        while True:
            #self.socketHandler.write_message("hello" + str(self.count))

            bandwidth1 = host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)
            bandwidth2 = host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)
            bandwidth3 = host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)
            bandwidth4 = host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)

            distance_matlab = getMatlabDistance()
            distance_hadoop = getHadoopDistance()

            print str(bandwidth1)

            self.pushGmetric("bandwidth", bandwidth1, "10.0.0.1:host1")
            self.pushGmetric("bandwidth", bandwidth2, "10.0.0.2:host2")
            self.pushGmetric("bandwidth", bandwidth3, "10.0.0.3:host3")
            self.pushGmetric("bandwidth", bandwidth4, "10.0.0.4:host4")

            #self.pushGmetric("communication_cost_matlab", distance_matlab)
            #self.pushGmetric("communication_cost_hadoop", distance_hadoop)


            #display(host_list)

            if self.count > 4:
                final_game(2, self.socketHandler, self.count)
                final_hadoop(2, self.socketHandler, self.count)
                final_matlab(2, self.socketHandler, self.count)

            self.count += 1
            #time_count += 1
            #display(host_list)
            time.sleep(3)


if __name__ == '__main__':

    ####################################### experiment-1 #######################################
    if exp == 1:
        setup_environment_1()
        display(host_list)

        host1_cpuUtil = []
        host2_cpuUtil = []
        host3_cpuUtil = []
        host4_cpuUtil = []
        total_distance = []
        time = []

        while time_count < 80:
            host1_cpuUtil.append(host_list['host_1'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host2_cpuUtil.append(host_list['host_2'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host3_cpuUtil.append(host_list['host_3'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host4_cpuUtil.append(host_list['host_4'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            total_distance.append(getTotalDistance())
            time.append(time_count)
            if time_count > 10:
                #matlab_1_consolidate(4)
                #matlab_2_consolidate(4)
                matlab_1_consolidate_comparison(8)
                #matlab_2_consolidate_comparison(4)
            time_count += 1
        display(host_list)


        setup_environment_1()
        time_count = 0
        display(host_list)

        host1_cpuUtil_1 = []
        host2_cpuUtil_1 = []
        host3_cpuUtil_1 = []
        host4_cpuUtil_1 = []
        total_distance_1 = []
        time_1 = []

        while time_count < 80:
            host1_cpuUtil_1.append(host_list['host_1'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host2_cpuUtil_1.append(host_list['host_2'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host3_cpuUtil_1.append(host_list['host_3'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host4_cpuUtil_1.append(host_list['host_4'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            total_distance_1.append(getTotalDistance())
            time_1.append(time_count)
            if time_count > 10:
                matlab_1_consolidate(4)
                matlab_2_consolidate(4)
                #matlab_1_consolidate_comparison(8)
                #matlab_2_consolidate_comparison(4)
            time_count += 1
        display(host_list)

        #plt.subplot(211)
        #plt.plot(time, host1_cpuUtil, label = 'host-1', linewidth = 2)
        #plt.plot(time, host2_cpuUtil, label = 'host-2', linewidth = 2)
        #plt.plot(time, host3_cpuUtil, label = 'host-3', linewidth = 2)
        #plt.plot(time, host4_cpuUtil, label = 'host-4', linewidth = 2)
        #plt.xlabel('time(h)')
        #plt.ylabel('cpu_util(%)')
        #plt.legend()
        #plt.grid(True)
        #
        #plt.subplot(212)
        plt.plot(time, host1_cpuUtil_1, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_cpuUtil_1, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_cpuUtil_1, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_cpuUtil_1, label = 'host-4', linewidth = 2)
        plt.xlabel('time(h)')
        plt.ylabel('cpu_util(%)')
        plt.legend()
        plt.grid(True)

        #plt.subplot(313)
        #plt.plot(time, total_distance, label = 'MM', linewidth = 2)
        #plt.plot(time, total_distance_1, label = 'Rule-Based', linewidth = 2)
        #plt.xlabel('time(h)')
        #plt.ylabel('total_distance')
        #plt.axis([20, 80, 0, 70])
        #plt.legend()
        #plt.grid(True)

        plt.show()


    ####################################### experiment-2 #######################################
    if exp == 2:
        setup_environment_2()

        display(host_list)
        host1_bandwidth = []
        host2_bandwidth = []
        host3_bandwidth = []
        host4_bandwidth = []
        time = []
        while time_count < 80:
            #plot the host bandwidth pic
            host1_bandwidth.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time.append(time_count)
            if time_count > 23:
                #game_1_guarantee_qos(1)
                #storage_1_consolidation(2)
                game_1_guarantee_qos_old(1)
                storage_1_consolidation_old(2)
            time_count += 1
        display(host_list)

        #plt.subplot(211)
        #plt.plot(time, host1_bandwidth, label = 'host-1', linewidth = 2)
        #plt.plot(time, host2_bandwidth, label = 'host-2', linewidth = 2)
        #plt.plot(time, host3_bandwidth, label = 'host-3', linewidth = 2)
        #plt.plot(time, host4_bandwidth, label = 'host-4', linewidth = 2)
        #plt.xlabel('time(h)')
        #plt.ylabel('bandwidth(MHZ)')
        #plt.grid(True)
        #plt.legend()

        setup_environment_2()
        time_count = 0

        display(host_list)
        host1_bandwidth_1 = []
        host2_bandwidth_1 = []
        host3_bandwidth_1 = []
        host4_bandwidth_1 = []
        time_1 = []
        while time_count < 80:
            #plot the host bandwidth pic
            host1_bandwidth_1.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth_1.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth_1.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth_1.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time_1.append(time_count)
            if time_count > 23:
                game_1_guarantee_qos(1)
                storage_1_consolidation(2)
                #game_1_guarantee_qos_old(1)
                #storage_1_consolidation_old(2)
            time_count += 1
        display(host_list)

        #plt.subplot(212)
        #plt.plot(time_1, host1_bandwidth_1, label = 'host-1', linewidth = 2)
        #plt.plot(time_1, host2_bandwidth_1, label = 'host-2', linewidth = 2)
        #plt.plot(time_1, host3_bandwidth_1, label = 'host-3', linewidth = 2)
        #plt.plot(time_1, host4_bandwidth_1, label = 'host-4', linewidth = 2)
        #plt.xlabel('time(h)')
        #plt.ylabel('bandwidth(MHZ)')
        #plt.grid(True)
        #plt.legend()

        print game_migration
        x = [0]
        y = [10]

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


        #plt.subplot(211)
        #plt.plot(x, y, label = 'game_server', linewidth = 2, color = 'red')
        #plt.axis([20, 60, -5, 15])
        #plt.xlabel('time(h)')
        #plt.ylabel('status')
        #plt.yticks(range(-5, 15, 5), ['', 'down', '', 'running', ''])
        #plt.grid(True)
        #plt.legend()
        #
        #plt.subplot(212)
        plt.plot([0, 60], [10, 10], label = 'game_server', linewidth = 2, color = 'red')
        plt.axis([20, 60, -5, 15])
        plt.xlabel('time(h)')
        plt.ylabel('status')
        plt.yticks(range(-5, 15, 5), ['', 'down', '', 'running', ''])
        plt.grid(True)
        plt.legend()

        plt.show()


    ####################################### experiment-3 #######################################
    if exp == 3:
        setup_environment_3()
        display(host_list)

        totalDistance = []
        time = []

        tmpInstance = []
        for instanceId in instance_list:
            tmpInstance.append(instanceId)

        while time_count < 30:
            if time_count == 10:
                display(host_list)
                host_list_1 = [host_list['host_2'], host_list['host_3']]
                host_list_2 = [host_list['host_2'], host_list['host_1']]
                host_list_3 = [host_list['host_4'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_3)
                instance_list['instance_3'].setFileHostList(host_list_3)
                instance_list['instance_4'].setFileHostList(host_list_2)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_3)
                instance_list['instance_11'].setFileHostList(host_list_3)
                instance_list['instance_12'].setFileHostList(host_list_1)
                instance_list['instance_13'].setFileHostList(host_list_3)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            if time_count == 20:
                display(host_list)
                host_list_1 = [host_list['host_4'], host_list['host_4']]
                host_list_2 = [host_list['host_1'], host_list['host_3']]
                host_list_3 = [host_list['host_3'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_2)
                instance_list['instance_3'].setFileHostList(host_list_1)
                instance_list['instance_4'].setFileHostList(host_list_1)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_2)
                instance_list['instance_11'].setFileHostList(host_list_2)
                instance_list['instance_12'].setFileHostList(host_list_3)
                instance_list['instance_13'].setFileHostList(host_list_1)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            totalDistance.append(getTotalFileDistance())
            time.append(time_count)

            hadoop_consolidation(2, tmpInstance)
            #hadoop_consolidation_old(10)
            time_count += 1
        display(host_list)

        setup_environment_3()
        #display(host_list)
        time_count = 0

        totalDistance_1 = []
        time_1 = []

        while time_count < 30:
            if time_count == 10:
                display(host_list)
                host_list_1 = [host_list['host_2'], host_list['host_3']]
                host_list_2 = [host_list['host_2'], host_list['host_1']]
                host_list_3 = [host_list['host_4'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_3)
                instance_list['instance_3'].setFileHostList(host_list_3)
                instance_list['instance_4'].setFileHostList(host_list_2)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_3)
                instance_list['instance_11'].setFileHostList(host_list_3)
                instance_list['instance_12'].setFileHostList(host_list_1)
                instance_list['instance_13'].setFileHostList(host_list_3)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            if time_count == 20:
                display(host_list)
                host_list_1 = [host_list['host_4'], host_list['host_4']]
                host_list_2 = [host_list['host_1'], host_list['host_3']]
                host_list_3 = [host_list['host_3'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_2)
                instance_list['instance_3'].setFileHostList(host_list_1)
                instance_list['instance_4'].setFileHostList(host_list_1)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_2)
                instance_list['instance_11'].setFileHostList(host_list_2)
                instance_list['instance_12'].setFileHostList(host_list_3)
                instance_list['instance_13'].setFileHostList(host_list_1)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            totalDistance_1.append(getTotalFileDistance())
            time_1.append(time_count)

            #hadoop_consolidation(2)
            hadoop_consolidation_old(2)
            time_count += 1
        #display(host_list)

        plt.plot(time, totalDistance_1, label = 'MM', marker = 's', linewidth = 2, color = 'orange')
        plt.plot(time_1, totalDistance, label = 'Rule-based', marker = 'v', linewidth = 2, color = 'blue')
        plt.xlabel('time(h)')
        plt.ylabel('total_distance')
        plt.axis([0, 30, 0, 110])
        plt.grid(True)
        plt.legend()
        plt.show()

    if exp == 4:
        setup_environment_4()

        display(host_list)
        host1_bandwidth = []
        host2_bandwidth = []
        host3_bandwidth = []
        host4_bandwidth = []
        distance_matlab = []
        distance_hadoop = []
        time = []
        while time_count < 80:
            #plot the host bandwidth pic
            host1_bandwidth.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time.append(time_count)
            distance_matlab.append(getMatlabDistance())
            distance_hadoop.append(getHadoopDistance())
            if time_count > 23:
                final_game(2)
                final_hadoop(2)
                final_matlab(2)
                #final_game_old(1)
                #final_game_old(1)
                #final_consolidation(4)
            time_count += 1
        display(host_list)


        setup_environment_4()
        time_count = 0

        display(host_list)
        host1_bandwidth_1 = []
        host2_bandwidth_1 = []
        host3_bandwidth_1 = []
        host4_bandwidth_1 = []
        distance_matlab_1 = []
        distance_hadoop_1 = []
        time_1 = []
        while time_count < 80:
            #plot the host bandwidth pic
            host1_bandwidth_1.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth_1.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth_1.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth_1.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time_1.append(time_count)
            distance_matlab_1.append(getMatlabDistance())
            distance_hadoop_1.append(getHadoopDistance())
            if time_count > 23:
                #final_game(2)
                #final_hadoop(2)
                #final_matlab(2)
                final_game_old(1)
                final_game_old(1)
                final_consolidation(4)
            time_count += 1
        display(host_list)

        plt.subplot(411)
        plt.plot(time, host1_bandwidth, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_bandwidth, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_bandwidth, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_bandwidth, label = 'host-4', linewidth = 2)

        plt.xlabel('time(h)')
        plt.ylabel('bandwidth(MHZ)')
        plt.legend()
        plt.grid(True)

        plt.subplot(412)
        plt.plot(time, host1_bandwidth_1, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_bandwidth_1, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_bandwidth_1, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_bandwidth_1, label = 'host-4', linewidth = 2)

        plt.xlabel('time(h)')
        plt.ylabel('bandwidth(MHZ)')
        plt.legend()
        plt.grid(True)


        plt.subplot(413)
        plt.plot(time, distance_matlab, label = 'Rule-based', linewidth = 2)
        plt.plot(time, distance_matlab_1, label = 'MM', linewidth = 2)
        plt.xlabel('time(h)')
        plt.ylabel('total_distance')
        #plt.xlabel('time(h)')
        #plt.ylabel('bandwidth(MHZ)')
        plt.legend()
        plt.grid(True)

        plt.subplot(414)
        plt.plot(time, distance_hadoop, label = 'Rule-based', linewidth = 2, color = 'orange')
        plt.plot(time, distance_hadoop_1, label = 'MM', linewidth = 2, color = 'blue')
        plt.xlabel('time(h)')
        plt.ylabel('total_distance')
        #plt.xlabel('time(h)')
        #plt.ylabel('bandwidth(MHZ)')
        plt.legend()
        plt.grid(True)

        plt.show()

    if exp == 5:
        app = tornado.web.Application([
        ('/', Index),
        ('/soc', SocketHandler)
        ])

        app.listen(9008)
        tornado.ioloop.IOLoop.instance().start()
