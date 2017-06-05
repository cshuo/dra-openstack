# -*- coding: utf-8 -*-

import sys
import math
import random

from ..Openstack.Service.Nova import Nova
from ..Openstack.Service.webSkt import SocketHandler
from ..Utils.logs import draLogger

_nova = Nova()
CES_ALPHA = 0.33
CPU_HEALTH_THRESHOLD = 0.75
CPU_OVERCOMMIT_RATIO = 16
MEM_OVERCOMMIT_RATIO = 1.5
logger = draLogger("DRA.vm_placement")


def find_host_for_vm(vm_id, nodes_info, underload_hosts, sleep_hosts):
    """
    Find a host for the vm using CD_based reallocation
    """
    min_cd = sys.float_info.max
    vm_info = _nova.inspect_instance(vm_id)
    select_host = None

    for host, info in nodes_info.items():
        if info["status"] == "overload" or info["status"] == "underload" or info['status'] == 'sleeping':
            continue
        if vm_info['cpu'] >= CPU_OVERCOMMIT_RATIO * info['res']['cpu']['total'] - info['res']['cpu']['used']:
             continue
        if vm_info['mem'] >= MEM_OVERCOMMIT_RATIO * info['res']['mem']['total'] - info['res']['mem']['used']:
            continue
        estimate_cpu_util = estimate_util(vm_id, vm_info, host)
        cd = math.pow(estimate_cpu_util-CPU_HEALTH_THRESHOLD, 2)
        if cd < min_cd:
            select_host = host
            min_cd = cd

    if select_host:
        # NOTE update nodes_info after reallocate vms
        nodes_info[select_host]['res']['cpu']['used'] += vm_info['cpu']
        nodes_info[select_host]['res']['mem']['used'] += vm_info['mem']
    else:
        # find host in underload hosts;
        for host in underload_hosts:
            info = nodes_info[host]
            if vm_info['OS-EXT-SRV-ATTR:host'] == host:
                continue
            if vm_info['cpu'] >= CPU_OVERCOMMIT_RATIO * info['res']['cpu']['total'] - info['res']['cpu']['used']:
                continue
            if vm_info['mem'] >= MEM_OVERCOMMIT_RATIO * info['res']['mem']['total'] - info['res']['mem']['used']:
                continue

            estimate_cpu_util = estimate_util(vm_id, vm_info, host)
            cd = math.pow(estimate_cpu_util-CPU_HEALTH_THRESHOLD, 2)
            if cd < min_cd:
                select_host = host
                min_cd = cd

        if select_host:
            underload_hosts.remove(select_host)
            nodes_info[select_host]['status'] = 'healthy'
            nodes_info[select_host]['res']['cpu']['used'] += vm_info['cpu']
            nodes_info[select_host]['res']['mem']['used'] += vm_info['mem']
        else:
            # find host in underload hosts;
            for host in sleep_hosts:
                info = nodes_info[host]
                if vm_info['cpu'] >= CPU_OVERCOMMIT_RATIO * info['res']['cpu']['total'] - info['res']['cpu']['used']:
                    continue
                if vm_info['mem'] >= MEM_OVERCOMMIT_RATIO * info['res']['mem']['total'] - info['res']['mem']['used']:
                    continue

                estimate_cpu_util = estimate_util(vm_id, vm_info, host)
                cd = math.pow(estimate_cpu_util-CPU_HEALTH_THRESHOLD, 2)
                if cd < min_cd:
                    select_host = host
                    min_cd = cd
            if select_host:
                # 更新显示主机状态
                SocketHandler.write_to_clients('status', host=select_host, status='underload')
                sleep_hosts.remove(select_host)
                nodes_info[select_host]['status'] = 'healthy'
                nodes_info[select_host]['res']['cpu']['used'] += vm_info['cpu']
                nodes_info[select_host]['res']['mem']['used'] += vm_info['mem']
            else:
                logger.warn("Failed to allocate vm: " + str(vm_id))

    return select_host


def get_migrt_plan(vm_ids, nodes_info, underload_hosts, sleep_hosts):
    """
    This is for selected vms from overloaded hosts
    @param sleep_hosts:
    @param underload_hosts:
    @param vm_ids:
    @param nodes_info:
    """
    vms_migrt_plan = {}
    sort_vms_decreasing(vm_ids)

    for vm in vm_ids:
        dest_host = find_host_for_vm(vm.split('#')[0], nodes_info, underload_hosts, sleep_hosts)
        if dest_host:
            vms_migrt_plan[vm] = dest_host
    return vms_migrt_plan


def get_migrt_plan_underload(underload_host, nodes_info, underload_hosts, sleep_hosts):
    """
    This is for underloaded hosts' vms dismissing
    @param sleep_hosts:
    @param underload_hosts:
    @param nodes_info:
    @param underload_host:
    """
    vm_ids = _nova.getInstancesOnHost(underload_host)
    migrt_plan = get_migrt_plan(vm_ids, nodes_info, underload_hosts, sleep_hosts)
    if len(migrt_plan) < len(vm_ids):
        logger.warn("Failed to dismiss all instances on Underload Host: " + underload_host)
        # NOTE reset the nodes_info
        return None
    else:
        return migrt_plan


def sort_vms_decreasing(vm_ids):
    """
    Sort vms by the overall resource utiliztion
    @param vm_ids:
    """
    pass    # TODO


def estimate_util(vm_id, vm_info, host):
    """
    estimate the cpu util of host after the vm's migration
    @param host:
    @param vm_info:
    @param vm_id:
    """
    return random.choice([0.7, 0.8, 0.9])


def ces_predict(history_data, timestep):
    """
    使用三次指数平滑法进行复杂预测, 历史数据值个数大于2;
    :param history_data:
    :param timestep:
    :return:
    """
    assert len(history_data) > 2
    s_1 = s_2 = s_3 = (history_data[0] + history_data[1]) / 2
    for i in xrange(1, len(history_data)):
        s_1 = CES_ALPHA * history_data[i] + (1 - CES_ALPHA) * s_1
        s_2 = CES_ALPHA * s_1 + (1 - CES_ALPHA) * s_2
        s_3 = CES_ALPHA * s_2 + (1 - CES_ALPHA) * s_3

    a_t = 3 * s_1 - 3 * s_2 + s_3
    b_t = ((6-5*CES_ALPHA)*s_1 - 2*(5-4*CES_ALPHA)*s_2 + (4-3*CES_ALPHA)*s_3) * CES_ALPHA/pow(1-CES_ALPHA, 2) / 2
    c_t = (s_1 - 2*s_2 + s_3) * pow(CES_ALPHA, 2) / pow(1-CES_ALPHA, 2) / 2

    res = a_t + b_t * timestep + c_t * pow(timestep, 2)
    return round(res, 3)


if __name__ == '__main__':
    pass
