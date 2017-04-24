# -*- coding: utf-8 -*- 

import sys
import math
import random
import logging

from ..Openstack.Service.Nova import Nova
from ..Utils.logs import draLogger

_nova = Nova()
CPU_HEALTH_THRESHOLD = 0.75
CPU_OVERCOMMIT_RATIO = 16
MEM_OVERCOMMIT_RATIO = 1.5
logger = draLogger("DRA.vm_placement")



def find_host_for_vm(vm_id, nodes_info, underload_hosts):
    """
    Find a host for the vm using CD_based reallocation
    """
    min_CD = sys.float_info.max
    vm_info = _nova.inspect_instance(vm_id)
    select_host = None

    for host, info in nodes_info.items():
        if info["status"] == "overload" or info["status"] == "underload":
            continue
        if vm_info['cpu'] >= CPU_OVERCOMMIT_RATIO * info['res']['cpu']['total'] - info['res']['cpu']['used']:
             continue
        if vm_info['mem'] >= MEM_OVERCOMMIT_RATIO * info['res']['mem']['total'] - info['res']['mem']['used']:
            continue
        estimate_cpu_util = estimate_util(vm_id, vm_info, host)
        cd = math.pow(estimate_cpu_util-CPU_HEALTH_THRESHOLD, 2)
        if cd < min_CD:
            select_host = host
            min_CD = cd

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
            if cd < min_CD:
                select_host = host
                min_CD = cd

        if select_host:
            underload_hosts.remove(select_host)
            nodes_info[select_host]['status'] = 'healthy'
            nodes_info[select_host]['res']['cpu']['used'] += vm_info['cpu']
            nodes_info[select_host]['res']['mem']['used'] += vm_info['mem']
        else:
            logger.info("Failed to allocate vm: " + vm_id)

    return select_host


def get_migrt_plan(vm_ids, nodes_info, underload_hosts):
    """
    This is for selected vms from overloaded hosts
    """
    vms_migrt_plan = {}
    sort_vms_decreasing(vm_ids)

    for vm in vm_ids:
        dest_host = find_host_for_vm(vm, nodes_info, underload_hosts)
        if dest_host:
            vms_migrt_plan[vm] = dest_host
    return vms_migrt_plan


def get_migrt_plan_underload(underload_host, nodes_info, underload_hosts):
    """
    This is for underloaded hosts' vms dismissing
    """
    vm_ids = _nova.getInstancesOnHost(underload_host)
    migrt_plan = get_migrt_plan(vm_ids, nodes_info, underload_hosts)
    if len(migrt_plan) < len(vm_ids):
        logger.warn("Failed to dismiss all instances on Underload Host: " + underload_host)
        # NOTE reset the nodes_info
        return None
    else:
        return migrt_plan


def sort_vms_decreasing(vm_ids):
    """
    Sort vms by the overall resource utiliztion
    """
    pass    # TODO


def estimate_util(vm_id, vm_info, host):
    """
    estimate the cpu util of host after the vm's migration
    """
    return random.choice([0.7, 0.8, 0.9])


if __name__ == '__main__':
    pass
