__author__ = 'pike'

class Host:

    def __init__(self, hostName):
        self.hostName = hostName
        self.id = "%s_%s" % (self.hostName, self.hostName)

    def getHostName(self):
        return self.hostName

    def getHostId(self):
        return self.id

    #def getService(self):
    #    return self.service

    #def setTotalMem(self,totalmem):
    #    self.totalmem=totalmem
    #
    #def getTotalMem(self):
    #    return self.totalmem
    #
    #def setFreeMem(self,freemem):
    #    self.freemem=freemem
    #
    #def getFreeMem(self):
    #    return self.freemem