# -*- coding: utf-8 -*-
# This file contains vm selection algorithm when a host is detected overload,
# the local manager will select am algorithm here and select a proper vm on 
# the host to migrate.


def best_fit_decreasing(hosts_cpu, hosts_ram, vms_cpu_ram):
    """
    The Best Fit Decreasing(BFD) algorithm for selecting optimal schedule for specific vms
    :param hosts_cpu: a map of hosts name to their available cpu in MHZ
    :param hosts_ram: a map of hosts name to their available ram in MB
    :param vms_cpu_ram: tuple list: (vm_name, vm virtual cpu num, vm ram usage in MB)
    :return: a map of vm name to host name, or {} if can not be resolved
    """
    hosts = sorted(((v, hosts_ram[k], k) for k, v in hosts_cpu.items()))
    mapping = {}
    for v_cpu, v_ram, vm_name in vms_cpu_ram:
        mapped = False
        while not mapped:
            for _, _, h in hosts:
                if hosts_cpu[h] >= v_cpu and hosts_ram[h] >= v_ram:
                    mapping[vm_name] = h
                    hosts_cpu[h] -= v_cpu
                    hosts_ram[h] -= v_ram
                    mapped = True
                    break
            else:
                print "There is no proper host to hold vm: ", vm_name
                break
    return mapping
