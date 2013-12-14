__author__ = 'pike'

QEMU="qemu:///system"

import libvirt

class InstanceMonitor:

    def __init__(self,hypervisor):
        self.conn=libvirt.open(hypervisor)
        print self.conn.getInfo()

    def getDomainList(self):
        return self.conn.listDomainsID()


    # three ways to get the instance domain
    def lookupInstanceByID(self,id):
        return self.conn.lookupByID(id)

    def lookupInstanceByUUIDString(self,uuidstr):
        return self.conn.lookupByUUIDString(uuidstr)

    def lookupInstanceByName(self,name):
        return self.conn.lookupByName(name)

    # get cpu status
    def getCPUStatus(self,domain):
        return domain.getCPUStats(1)

    def getCPUStatusByUUID(self,uuidstr):
        domain=self.getCPUStatus(uuidstr)
        return domain.getCPUStats(1)

    #get memory status
    def getMemStatus(self,domain):
        return domain.memoryStats()

    def getMemStatusByUUID(self,uuidstr):
        domain=self.conn.lookupByUUIDString(uuidstr)
        return domain.memoryStats()

    def getInfo(self,uuidstr):
        domain=self.conn.lookupByUUIDString(uuidstr)
        return domain.info()





if __name__=="__main__":
    testmonitor=InstanceMonitor(QEMU)


