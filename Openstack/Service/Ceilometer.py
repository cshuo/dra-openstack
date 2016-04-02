# coding: utf-8

from dra.Openstack.Service.OpenstackService import  *
from dra.Openstack.Conf import OpenstackConf
from dra.Utils.HttpUtil import OpenstackRestful
from .Nova import Nova

import time
import datetime
import random


# generate random cpu usage for testing
RANDOM_MIN, RANDOM_MAX = 0.1, 0.9
_nova = Nova()

class Ceilometer(OpenstackService):

    def __init__(self):

        OpenstackService.__init__(self)
        self.restful = OpenstackRestful(self.tokenId)
        print self.tokenId

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
    
    def last_n_average_statistic(self, n, hostname, meter_name='compute.node.cpu.percent'):
        """
        get last n hours meter statistics
        """
        now_t = time.gmtime()
        end_t = datetime.datetime(*now_t[:6])
        begin_t = end_t - datetime.timedelta(hours=n)

        resoure_id = hostname + '_' + hostname
        qry = '''[{"field": "timestamp",
        "op": "ge",
        "value": "%s"},
        {"field": "timestamp",
        "op": "lt",
        "value": "%s"},
        {"field": "resource_id",
        "op": "eq",
        "value": "%s"}]''' % (begin_t.isoformat(), end_t.isoformat(), resoure_id)
        return self.getMeterStatistics(meter_name, qry)['avg']

    def last_n_otf_statistic(self, n, hostname, meter_name='compute.node.cpu.percent'):
        """
        NOTE: overload_time and total_time is not actually time, but num of samples
        during n hours
        TODO: get real data
        """
        overload_time, total_time = 0, 0
        # TODO: cal the real time specifically
        return overload_time, total_time

    def last_n_vm_cpu_statistic(self, n, vm_name):
        # TODO get real cpu statistic of a vm
        sttic = dict()
        sttic['avg'] = random.uniform(RANDOM_MIN, RANDOM_MAX)
        return sttic

    def get_vm_ram(self, vm_name):
        # TODO get the ram size of a vm from openstack api
        ram_size_list = [512, 1024, 2048]
        return random.choice(ram_size_list)

    def get_interhost_bandwidth(self, host):
        """
        Get bandwidth between the specific host and others
        :param host: the specific host
        :return dict type of bandwidth msg
        """
        hosts = _nova.getComputeHosts()
        hosts.remove(host)
        bd = dict()
        for h in hosts:
            # TODO get real bandwidth between hosts(MB/s)
            bd[h] = random.uniform(5, 10)
        return bd




if __name__ == "__main__":
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
    "value": "compute2_compute2"}]''' % (begin_t.isoformat(), end_t.isoformat())

    q2 = '''[{"field": "resource_id",
    "op": "eq",
    "value": "compute2_compute2"}]'''

    # print ceilometerTest.getMeterStatistics("compute.node.cpu.percent", q)
    #print ceilometerTest.last_n_average_statistic(1, 'compute1')
    print ceilometerTest.getMeter("compute.node.cpu.percent", q)
    # print ceilometerTest.getCpuStat("2014-12-12T00:00:00", "2014-12-16T00:00:00",
    #                                 "feebf6dc-2f04-4e1d-977e-6c7fde4e4cb3")
    # print ceilometerTest.getAllResources()
