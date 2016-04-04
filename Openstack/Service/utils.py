# coding: utf-8

from .Ceilometer import Ceilometer
from .Nova import Nova

_nova = Nova()
_ceil = Ceilometer()


def get_host_vms_cpu(host, n):
    """
    Get all vms' cpu statistic of a overload host
    :param host: overload host
    :param n: last n hours to statistic
    :return: dict type cpu msg
    """
    vms = _nova.getInstancesOnHost(host)
    vms_cpu = dict()
    for vm in vms:
        vms_cpu[vm] = _ceil.last_n_vm_cpu_statistic(n, vm)['avg']
    return vms_cpu


def get_host_vms_ram(host):
    """
    Get all vms' ram info of a overload host
    :param host: overload host
    :return: dict type ram msg
    """
    vms = _nova.getInstancesOnHost(host)
    vms_ram = dict()
    for vm in vms:
        vms_ram[vm] = _ceil.get_vm_ram(vm)
    return vms_ram


def migrate_vms(sche_place):
    """
    Live migrating a set of vms according to schedule results synchronously
    :param sche_place: schedule result made
    """
    pass
