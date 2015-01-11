__author__ = 'pike'

import threading

hostList = {}


class Host:
    def __init__(self, hostId, hostList):
        self.id = hostId
        self.instanceList = {}
        self.hostList = hostList
        self.hostList[self.id] = self
        self.lock = threading.RLock()

    def addInstance(self, instance):
        self.lock.acquire()
        self.instanceList[instance.getId()] = instance
        self.lock.release()

    def removeInstance(self, instance):
        self.lock.acquire()
        del self.instanceList[instance.getId()]
        self.lock.release()

    def getAvgCpuUtil(self, type, interval):
        total = 0
        for instance in self.instanceList:
            total += instance.getAvgCpuUtil(type, interval)
        return total / len(self.instanceList)

    def getId(self):
        return self.id

    def migrateInstance(self, instance, destHost):
        print 'host %d : migrate instance %d to host %d' % (self.id, instance.getId(), destHost.getId())
        # more than one thread may migrate the same host
        self.lock.acquire()
        destHost.addInstance(instance)
        self.removeInstance(instance)
        self.lock.release()



class Instance:
    def __init__(self, instanceId, host):
        self.id = instanceId
        self.host = host
        self.host.addInstance(self)

    def setWorkload(self, workload):
        pass

    def getAvgCpuUtil(self, type, interval):
        if type == 'past':
            pass
        elif type == 'future':
            pass
        else:
            pass

    def getId(self):
        return self.id


class ObserveViolation(threading.Thread):
    def __init__(self):
        pass

    def run(self):
        pass



