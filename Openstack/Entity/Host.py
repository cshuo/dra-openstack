__author__ = 'pike'

class Host:

    def __init__(self, hostName, service):
        self.hostName = hostName
        self.service = service

    def getHostName(self):
        return self.hostName


    def getService(self):
        return self.service

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