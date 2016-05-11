# -*- coding:utf-8 -*-

import random
import sys
from ..Hades.scheduler.utils import get_queue_msg_num
from ..Hades.EventService.RpcApi import *
from ..Hades.PMA.RpcApi import ArbiterPMAAPI
from ..Openstack.Service.Nova import Nova
from ..Openstack.Service.Ceilometer import Ceilometer
from ..Openstack.Conf import OpenstackConf
from ..db.utils import DbUtil

_eventService = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)
_arbiter_api = ArbiterPMAAPI(CONF.hades_midPMA_topic, CONF.hades_exchange)
_nova = Nova()
_ceilometer = Ceilometer()
_involved_host = []


# added by cshuo #
def simple_host_filter():
    """
    @return:
    """
    return str(_nova.getComputeHosts())


def test_eva(instance, vm_type):
    print "--------------------------test_eva-----------------------"
    print "Hi, I am " + instance
    print "type of {0} is {1}".format(instance, vm_type)


def print_log(log):
    """
    @param log:
    @return:
    """
    print "-->>: " + log


def generateEvent(event_name, *args):
    """
    assert a event into Clips
    @param event_name:
    @param args:
    @return:
    """
    if event_name == 'evacuation':
        # print '----------------------------- begin generate evacuation --------------------'
        event = "(evacuation (instance {id}) (type {type}))".format(id=args[0], type=args[1])
        # _eventService.sendEventForResult({}, OpenstackConf.DEFAULT_RPC_SERVER, 'arbiterPMA', event)
        _arbiter_api.handleEventWithResult({}, OpenstackConf.DEFAULT_RPC_SERVER, event)
        # print '----------------------------- end generate evacuation --------------------'
    elif event_name == 'migration':
        # print '----------------------------- begin migration event --------------------'
        event = "(migration (instance {id}) (src {src}) (dest {dest}))".format(id=args[0], src=args[1],
                                                                               dest=args[2])
        _eventService.sendEvent({}, OpenstackConf.DEFAULT_RPC_SERVER, 'arbiterPMA', event)
        # print '----------------------------- end migration event --------------------'


def hostFilter(host_list, expr, mode):
    """
    filter hosts or select a host
    @param host_list:
    @param expr:
    @param mode: optional 'select' and 'filter'
    @return:
    """
    if mode == 'select':
        for host in host_list:
            if eval(expr.replace('$HOST', '"' + host + '"')):
                return host
    else:
        ret_host = []
        for host in host_list:
            if eval(expr.replace('$HOST', '"' + host + '"')):
                ret_host.append(host)
        return ret_host
    return None


def getAllHost(instance):
    host_list = _nova.getComputeHosts()
    host_list.remove(getVmHost(instance))
    return host_list


def hostHasInstanceType(host, vm_type):
    vms = _nova.getInstancesOnHost(host)
    dbu = DbUtil()
    for vm in vms:
        if dbu.query_vm(vm)['type'] == vm_type:
            return 1
    return 0


def last_n_avg_statistic(host, meter, time_range):
    if meter == 'cpu_util':
        meter = 'compute.node.cpu.percent'
    return _ceilometer.last_n_average_statistic(time_range, host + '_' + host, meter)


def hostRankFilter(host_list, obj_host, expr):
    """
    @param host_list:
    @param obj_host: e.g., matlab master host or host where the hadoop file on
    @param expr:
    @return:
    """
    dest_host = host_list[0]
    if 'getTimeDelay' in expr:
        min_delay = sys.maxint
        for host in host_list:
            expr = expr.replace('$HOST', '"' + host + '"').replace('$MASTER', '"' + obj_host + '"')
            delay = eval(expr)
            if delay < min_delay:
                dest_host = host
                min_delay = delay
    return dest_host


def getTimeDelay(host, obj_host):
    """
    network time delay between hosts
    @param host:
    @param obj_host:
    @return:
    """
    return random.randint(50, 100)


def getVmHost(instance):
    """
    return host where the vm lives on
    @param instance:
    @return:
    """
    return _nova.inspect_instance(instance)['OS-EXT-SRV-ATTR:host']


def Migrate(src_host, instance, dest_host):
    """
    @param src_host:
    @param instance:
    @param dest_host:
    @return:
    """
    print '>> action: migrate ' + instance + ' to ' + dest_host
    _nova.liveMigration(instance, dest_host)


def hostPredictData(host, meter, time_range, meter_section):
    """
    @param host
    @param meter
    @param time_range
    @param meter_section
    @return
    """
    # for bandwidth testing now
    return 500


def hostInvolved(host):
    """
    check if underload host has just recvd a new vm during other processing before
    @param host:
    @return:
    """
    if host in _involved_host:
        return 1
    else:
        return 0


def Dismiss(host):
    """
    evacuate all vms of host
    @param host:
    @return:
    """
    # print "---------------------------------------enter dismiss-----------------------------"
    vms = _nova.getInstancesOnHost(host)
    if not vms:
        return
    dbu = DbUtil()
    for vm in vms:
        # NOTE hard code type to test... modify later
        # generateEvent('evacuation', vm, dbu.query_vm(vm)['type'])
        generateEvent('evacuation', vm, 'MATLAB_SLAVE')
        print '--->>: queue status is: '
        print get_queue_msg_num('hades_arbiterPMA_topic.pike'), get_queue_msg_num('hades_midPMA_topic.pike'), \
            get_queue_msg_num('hades_eventService_topic.pike'), get_queue_msg_num('hades_eventService_topic'), \
            get_queue_msg_num('hades_midPMA_topic'), get_queue_msg_num('hades_arbiterPMA_topic')
    # print "---------------------------------------leave dismiss-----------------------------"


def clean_cache(*args):
    """
    reset _involved_host if arbiter queue in rabbitmq is empty
    """
    if get_queue_msg_num(CONF.hades_eventService_topic + '.' + OpenstackConf.DEFAULT_RPC_SERVER) == 0 and \
            get_queue_msg_num(CONF.hades_arbiterPMA_topic + '.' + OpenstackConf.DEFAULT_RPC_SERVER) == 0 and \
            get_queue_msg_num(CONF.hades_midPMA_topic+'.'+OpenstackConf.DEFAULT_RPC_SERVER) == 0:
        print ">> cache cleaned.."
        _involved_host[:] = []
    else:
        if args:
            _involved_host.append(args[0])
            print "****--->>: involved hosts:" + str(_involved_host)

# added by cshuo #


if __name__ == "__main__":
    print "this is external function..."
    Migrate('compute1', '7d01bee3-52ab-4e2f-acbf-9508cd2769c4', 'compute2')
    print hostHasInstanceType('compute1', 'master')
    print last_n_avg_statistic('compute1', 'cpu_util', 2)
    print getTimeDelay('compute1', 'compute2')
    print getVmHost('7d01bee3-52ab-4e2f-acbf-9508cd2769c4')
    print hostPredictData('compute1', 'cpu_util', 2, 'avg')
    print getAllHost('7d01bee3-52ab-4e2f-acbf-9508cd2769c4')
    print hostFilter(['compute1', 'compute2'], 'hostHasInstanceType($HOST, "master") >0', 'select')
    print hostFilter(['compute1', 'compute2'], 'last_n_avg_statistic($HOST, "cpu_util", 2) < 85', 'filter')
    print hostRankFilter(['compute1', 'compute2'], 'compute1', "getTimeDelay($HOST, $MASTER)")
