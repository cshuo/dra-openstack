# -*- coding: utf-8 -*-
#
#Inside this file are some vm selection algorithms when a host is overload
#

import random
import time

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
    @param host: host that overloaded
    @param n: last n hours cpu usage to analyze
    @return: selected vm
    """
    vms_cpu, vms_ram = utils.get_host_vms_cpu_ram(host, n)
    print vms_cpu.keys(), vms_ram.keys()
    select_vm = min(vms_ram, key=vms_ram.get)
    min_ram = vms_ram[select_vm]
    max_cpu = 0

    for vm, cpu in vms_cpu.items():
        if vms_ram[vm] > min_ram:
            continue
        if cpu > max_cpu:
            max_cpu = cpu
            select_vm = vm
    return select_vm


if __name__ == '__main__':
    # vm = random_selection('compute1', 1)
    vm_s = minimum_migration_time_max_cpu('compute1', 1)
    print vm_s
