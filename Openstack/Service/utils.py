# coding: utf-8

import time
import requests

from .Ceilometer import Ceilometer
from .Nova import Nova
from dra.Utils.logs import draLogger
from ..Conf import OpenstackConf


_logger = draLogger("Dra.Openstack.Common")
_nova = Nova()
_ceil = Ceilometer()


def get_host_vms_cpu_ram(host, n):
    """
    Get all vms' cpu statistic of a overload host
    :param host: overload host
    :param n: last n hours to statistic
    :return: dict type cpu,ram msg
    """
    vms = _nova.getInstancesOnHost(host)
    vms_cpu, vms_ram = dict(), dict()
    for vm in vms:
        cpu_avg = _ceil.last_n_average_statistic(n, vm.split('#')[0], 'cpu_util')
        # NOTE code using this function has to judge whether return res is empty
        if cpu_avg:
            vms_cpu[vm] = cpu_avg
        vms_ram[vm] = _nova.inspect_instance(vm.split('#')[0])['ram']
    return vms_cpu, vms_ram


def get_host_vms_ram(host):
    """
    Get all vms' ram info of a overload host
    :param host: overload host
    :return: dict type ram msg
    """
    vms = _nova.getInstancesOnHost(host)
    vms_ram = dict()
    for vm in vms:
        vms_ram[vm] = _nova.inspect_instance(vm.split('#')[0])['ram']
    return vms_ram


def get_vms_cpu_load(host, n):
    """
    Get all vms' cpu info of a overload host
    :param host: overload host
    :return: dict type cpu (VCPUS * CPU_UTIL) msg
    """
    vms = _nova.getInstancesOnHost(host)
    if len(vms) == 0:
        return {}
    vms_cpu_load = dict()
    for vm in vms:
        cpu_avg = _ceil.last_n_average_statistic(n, vm.split('#')[0], 'cpu_util')
        vms_cpu_load[vm] = cpu_avg * _nova.inspect_instance(vm.split('#')[0])['cpu']
    return vms_cpu_load


def get_host_overview():
    """
    获取所有计算节点的计算资源当前监控信息.
    :return: 示例[{type: "data", id: "kolla1", data: {cpu: "30", mem: "50",disk: "30", net: "400"}}]
    """
    rs = []
    hosts = _nova.getComputeHosts()
    url = OpenstackConf.REST_URL + "pmeters"

    for h in hosts:
        h_dict = {'type': 'data', 'id': h, 'data': {'cpu':0, 'mem':0, 'disk':0, 'net':0}}
        params = {'host': h, 'num': 2}
        r = requests.get(url=url, params=params)
        if r.status_code != 200:
            continue
        r = r.json()
        h_dict['data']['cpu'] = round(sum(r['cpu']['value']) / len(r['cpu']['value']), 2)
        h_dict['data']['mem'] = round(sum(r['mem']['value']) / len(r['mem']['value']), 2)
        h_dict['data']['disk'] = round(sum(r['disk']['value']) / len(r['disk']['value']), 2)
        # NOTE net is unavailable now.
        h_dict['data']['net'] = 0
        rs.append(h_dict)
    return rs


def get_vms_overview(host):
    """
    获取一个服务器上所有虚拟机的资源使用预览情况, 过去两分钟的平均值.
    :param host:
    :return:
    """
    vms = _nova.getInstancesOnHost(host=host)
    rs = []
    for vm in vms:
        vm_id, _ = vm.split('#')
        vm_dict = {'type': 'data', 'id': vm_id, 'data': {}}
        vm_dict['data']['cpu'] = round(_ceil.last_n_average_statistic(0.034, vm_id, 'cpu_util'), 2)
        vm_dict['data']['mem'] = round(_ceil.last_n_average_statistic(0.034, vm_id, 'memory.usage'), 2)
        vm_dict['data']['disk'] = round(_ceil.last_n_average_statistic(0.034, vm_id, 'disk.usage'), 2)
        # NOTE net is unavailable now.
        vm_dict['data']['net'] = 0
        rs.append(vm_dict)
    return rs


def migrate_vms(sche_place):
    """
    Live migrating a set of vms according to schedule results synchronously
    :param sche_place: schedule result made
    """
    retry_placement = {}
    failure_placement = {}

    # migrate only 1 vm at a time, as multi migration at same time mail fail
    for vm, dest in sche_place.items():
        start_time = time.time()
        _nova.liveMigration(vm.split('#')[0], vm.split('#')[1], dest)

        # wait 10 seconds for migrating ok
        time.sleep(10)

        while True:
            # get detail information of a vm
            vm_info = _nova.inspect_instance(vm)
            if vm_info['OS-EXT-SRV-ATTR:hypervisor_hostname'] == dest and vm_info['status'] == 'ACTIVE':
                _logger.info("vm {0} migrated to host {1} successfully!".format(vm, dest))
                break
            elif time.time() - start_time > 240 and vm_info['OS-EXT-SRV-ATTR:hypervisor_hostname'] != dest \
                    and vm_info['status'] == 'ACTIVE':
                retry_placement[vm] = dest
                _logger.warn("vm {0} migrate to host {1} timeout...".format(vm, dest))
                break
            elif vm_info['status'] == 'ERROR':
                failure_placement[vm] = dest
                _logger.warn("vm {0} state error during migration".format(vm))
                break
            time.sleep(3)

    if failure_placement:
        _logger.error("The following placements {0} are failed".format(str(failure_placement)))

    if retry_placement:
        _logger.warn("Retrying the following migrations {0}..".format(str(retry_placement)))
        migrate_vms(retry_placement)


if __name__ == '__main__':
    print get_vms_overview('kolla1')
