__author__ = 'pike'


from Openstack.Service.OpenstackService import  *
from Openstack.Conf.OpenstackConf import *


class Ceilometer(OpenstackService):

    def __init__(self):

        OpenstackService.__init__(self)

    def urlGenerate(self, version, type, name, statistics):

        url = "http://%s:8777/%s/%s/%s" % (CONTROLLER_HOST, version, type, name)
        if (statistics == "statistics"):
            url += "/statistics"
        return url


    def getAllMeters(self):pass



    def getCpuStat(self, startTime, endTime, resourceId):

        url = self.urlGenerate("v2", "meters", "cpu_util", "statistics")

        #add params (use "Get" not "Post")
        urlParam = "?&q.field=timestamp&q.op=ge&q.value=%s" % startTime + \
                   "&q.field=timestamp&q.op=lt&q.value=%s" % endTime + \
                   "&q.field=resource_id&q.op=eq&q.value=%s" % resourceId
        url += urlParam

        serverRequest = urllib2.Request(url)
        serverRequest.add_header("Content-type", "application/json")
        serverRequest.add_header("X-Auth-Token", self.tokenId)

        request = urllib2.urlopen(serverRequest)
        result = json.loads(request.read())
        return result[0]

    def getAvgCpuFromStat(self, cpuStat):
        return cpuStat["avg"]



if __name__=="__main__":

    ceilometerTest = Ceilometer()
    cpuStat = ceilometerTest.getCpuStat("2014-08-01T00:00:00", "2014-09-01T00:00:00", "c07c4077-cda0-4907-bc76-536c6fc3afb2")
    print ceilometerTest.getAvgCpuFromStat(cpuStat)