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

    def getMeter(self, meter_name, queryFilter):
        url = "%s/v2/meters/%s" % (OpenstackConf.CEILOMETER_URL, meter_name)

        #transfer str to list
        queryFilter = eval(queryFilter)
        print queryFilter

        params = ""
        for queryItem in queryFilter:
            param = ""
            for key in queryItem:
                param += "&q.%s=%s" % (key, queryItem[key])
            params += param

        url = url + "?" + params

        result = self.restful.getResult(url)
        return result[0]



    def getMeterStatistics(self, meter_name, queryFilter, groupby = None, period = None, aggregate = None):
        url = "%s/v2/meters/%s/statistics" % (OpenstackConf.CEILOMETER_URL, meter_name)

        #transfer str to list
        queryFilter = eval(queryFilter)
        #print queryFilter

        params = ""
        for queryItem in queryFilter:
            param = ""
            for key in queryItem:
                param += "&q.%s=%s" % (key, queryItem[key])
            params += param

        url = url + "?" + params

        result = self.restful.getResult(url)
        return result[0]


    #def getCpuStat(self, startTime, endTime, resourceId):
    #
    #    #url = "%s/v2/meters/%s/statistics" % (OpenstackConf.CEILOMETER_URL, "cpu_util")
    #    url = "%s/v2/meters/%s/statistics" % (OpenstackConf.CEILOMETER_URL, "compute.node.cpu.idle.time")
    #
    #    #add params (use "Get" not "Post")
    #    urlParam = "?&q.field=timestamp&q.op=ge&q.value=%s" % startTime + \
    #               "&q.field=timestamp&q.op=lt&q.value=%s" % endTime + \
    #               "&q.field=resource_id&q.op=eq&q.value=%s" % "compute1_compute1"
    #    url += urlParam
    #
    #    result = self.restful.getResult(url)
    #    return result[0]
    #
    #def getAvgCpuFromStat(self, cpuStat):
    #    return cpuStat["avg"]



if __name__=="__main__":

    ceilometerTest = Ceilometer()

    q = '''[{"field": "timestamp",
    "op": "ge",
    "value": "2014-12-12T00:00:00"},
    {"field": "timestamp",
    "op": "lt",
    "value": "2014-12-16T00:00:00"},
    {"field": "resource_id",
    "op": "eq",
    "value": "feebf6dc-2f04-4e1d-977e-6c7fde4e4cb3"}]'''

    print ceilometerTest.getMeterStatistics("cpu_util", q)
    #print ceilometerTest.getCpuStat("2014-12-12T00:00:00", "2014-12-16T00:00:00", "feebf6dc-2f04-4e1d-977e-6c7fde4e4cb3")
    #print ceilometerTest.getAllResources()
