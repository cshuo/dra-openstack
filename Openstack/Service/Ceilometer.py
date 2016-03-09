__author__ = 'pike,cshuo'


from dra.Openstack.Service.OpenstackService import  *
from dra.Openstack.Conf import OpenstackConf
from dra.Utils.HttpUtil import OpenstackRestful


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
        if result:
            return result[0]
        else:
            print "query result is None"
            return None


if __name__=="__main__":

    import time, datetime
   
    now_t = time.gmtime()
    end_t = datetime.datetime(*now_t[:6])
    begin_t = end_t - datetime.timedelta(hours=1)

    ceilometerTest = Ceilometer()
    q = '''[{"field": "timestamp",
    "op": "ge",
    "value": "%s"},
    {"field": "timestamp",
    "op": "lt",
    "value": "%s"},
    {"field": "resource_id",
    "op": "eq",
    "value": "compute1_compute1"}]''' % (begin_t.isoformat(), end_t.isoformat())
    print q
      
    q2 = '''[{"field": "resource_id",
    "op": "eq",
    "value": "compute1_compute1"}]'''

    print ceilometerTest.getMeterStatistics("compute.node.cpu.percent", q)['avg']
    #print ceilometerTest.getMeter("compute.node.cpu.percent", q2)
    #print ceilometerTest.getCpuStat("2014-12-12T00:00:00", "2014-12-16T00:00:00", "feebf6dc-2f04-4e1d-977e-6c7fde4e4cb3")
    #print ceilometerTest.getAllResources()
