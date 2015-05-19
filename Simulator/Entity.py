__author__ = 'pike'

import threading
import random
from Conf import *




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

        #self.bandwidth = [30, 30, 30, 30, 30, 30,
        #                  40, 40, 40, 40, 40, 40,
        #                  30, 30, 30, 30, 30, 30,
        #                  40, 40, 40, 40, 40, 40,]
        self.bandwidth = [45, 40, 40, 40, 40, 40,
                          50, 50, 50, 55, 60, 60,
                          60, 70, 70, 65, 65, 70,
                          70, 70, 70, 70, 60, 50]

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
