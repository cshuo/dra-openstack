__author__ = 'pike'


from Openstack.Service.OpenstackService import  *
from Openstack.Conf import OpenstackConf
from Utils.HttpUtil import OpenstackRestful


class Ceilometer(OpenstackService):

    def __init__(self):

        OpenstackService.__init__(self)
        self.restful = OpenstackRestful(self.tokenId)


    def getAllMeters(self):
        url = "%s/v2/meters" % OpenstackConf.CEILOMETER_URL
        result = self.restful.getResult(url)
        return result

    def getAllResources(self):
        url = "%s/v2/resources" % OpenstackConf.CEILOMETER_URL
        result = self.restful.getResult(url)
        return result


    def getCpuStat(self, startTime, endTime, resourceId):

        url = "%s/v2/meters/%s/statistics" % (OpenstackConf.CEILOMETER_URL, "cpu_util")

        #add params (use "Get" not "Post")
        urlParam = "?&q.field=timestamp&q.op=ge&q.value=%s" % startTime + \
                   "&q.field=timestamp&q.op=lt&q.value=%s" % endTime + \
                   "&q.field=resource_id&q.op=eq&q.value=%s" % resourceId
        url += urlParam

        result = self.restful.getResult(url)
        return result[0]

    def getAvgCpuFromStat(self, cpuStat):
        return cpuStat["avg"]



if __name__=="__main__":

    ceilometerTest = Ceilometer()
    #cpuStat = ceilometerTest.getCpuStat("2014-08-01T00:00:00", "2014-09-01T00:00:00", "c07c4077-cda0-4907-bc76-536c6fc3afb2")
    print ceilometerTest.getAllResources()[0]