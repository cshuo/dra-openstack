# -*- coding: utf-8 -*-
#
# Inside this file are some vm selection algorithms when a host is overload
#

import random
import time

from ..Openstack.Service import utils
from ..Openstack.Service.Nova import Nova
# from ..db.utils import DbUtil


def random_selection(host, n):
    """
    Select a vm from overload host randomly
    :param host: host that overloaded
    :return: selected vm
    """
    nova = Nova()
    vms = nova.getInstancesOnHost(host)
    select_vm = random.choice(vms)
    # dbu = DbUtil()
    # vm_type = dbu.query_vm(select_vm)['type']
    return select_vm


def min_migrt_time_max_cpu(host, n):
    """
    Select a vm with the minimum ram usage and maximum cpu usage
    @param host: host that overloaded
    @param n: last n hours cpu usage to analyze
    @return: selected vm id
    """
    vms_cpu, vms_ram = utils.get_host_vms_cpu_ram(host, n)
    print vms_cpu.keys(), vms_ram.keys()
    select_vm = min(vms_ram, key=vms_ram.get)
    min_ram = vms_ram[select_vm]
    max_cpu = 0

    sel_vms = []
    for vm, cpu in vms_cpu.items():
        if vms_ram[vm] > min_ram:
            continue
        if cpu > max_cpu:
            max_cpu = cpu
            select_vm = vm
    # dbu = DbUtil()
    # vm_type = dbu.query_vm(select_vm)['type']
    sel_vms.append(select_vm)
    return sel_vms


def od_vm_select(host, n):
    """
    VM selection of overload hosts based on the concept "OD"(overload degree).
    OD = sigma(U_ri/UT_ri - 1)
    NOTE: consider only cpu now... only one vm is selected...
    """
    sel_vms = []
    vms_cpu_load = utils.get_vms_cpu_load(host, n)
    sel_vms.append(max(vms_cpu_load, key=vms_cpu_load.get))
    return sel_vms


if __name__ == '__main__':
    # vm = random_selection('compute1', 1)
    begin = time.time()
    vms = od_vm_select("compute0", 1)
    print vms
    print time.time() - begin
