# coding: utf-8

import time

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
    retry_placement = {}
    failure_placement = {}

    # migrate only 1 vm at a time, as multi migration at same time mail fail
    for vm, dest in sche_place.items():
        start_time = time.time()
        vm_uuid = _nova.vm_name_to_uuid(vm)
        _nova.liveMigration(vm_uuid, dest)

        # wait 10 seconds for migrating ok
        time.sleep(10)

        while True:
            if _nova.vm_hostname(vm) == dest and _nova.vm_status(vm) == 'ACTIVE':
                print "vm {0} migrated to host {1} successfully!".format(vm, dest)
                break
            elif time.time() - start_time > 240 and _nova.vm_hostname(vm) != dest and _nova.vm_status(vm) == 'ACTIVE':
                retry_placement[vm] = dest
                print "vm {0} migrate to host {1} timeout...".format(vm, dest)
                break
            elif _nova.vm_status(vm) == 'ERROR':
                failure_placement[vm] = dest
                print "vm {0} state error during migration".format(vm)
                break
            time.sleep(3)

    if failure_placement:
        print "The following placements {0} are failed".format(str(failure_placement))

    if retry_placement:
        print "Retrying the following migrations {0}..".format(str(retry_placement))
        migrate_vms(retry_placement)

