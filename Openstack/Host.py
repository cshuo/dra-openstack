__author__ = 'pike'

class Host:

    def __init__(self,hostname,hostip):
        self.hostname=hostname
        self.hostip=hostip

    def setTotalMem(self,totalmem):
        self.totalmem=totalmem

    def getTotalMem(self):
        return self.totalmem

    def setFreeMem(self,freemem):
        self.freemem=freemem

    def getFreeMem(self):
        return self.freemem