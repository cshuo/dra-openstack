# coding: utf-8
"""
Inside this file are some vm selection algorithms when a host is overload
"""

import random

from ..Openstack.Service import utils
from ..Openstack.Service.Nova import Nova


def random_selection(host, n):
    """
    Select a vm from overload host randomly
    :param host: host that overloaded
    :return: selected vm
    """
    nova = Nova()
    vms = nova.getInstancesOnHost(host)
    select_vm = random.choice(vms)
    return select_vm


def minimum_migration_time_max_cpu(host, n):
    """
    Select a vm with the minimum ram usage and maximum cpu usage
    :param host: host that overloaded
    :param n: last n hours cpu usage to analyze
    :return: selected vm
    """
    vms_cpu = utils.get_host_vms_cpu(host, n)
    vms_ram = utils.get_host_vms_ram(host)
    min_ram = min(vms_ram.values())
    max_cpu = 0
    select_vm = None
    for vm, cpu in vms_cpu.items():
        if vms_ram[vm] > min_ram:
            continue
        if cpu > max_cpu:
            max_cpu = cpu
            select_vm = vm
    return select_vm
