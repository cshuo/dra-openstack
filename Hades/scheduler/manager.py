# -*- coding: utf-8 -*-

import oslo_messaging as messaging
from oslo_config import cfg

from ..Manager import Manager
from ...Openstack.Service.Ceilometer import Ceilometer
from ...Openstack.Service.Nova import Nova
from ...Openstack.Service.utils import migrate_vms
from .vm_placement import best_fit_decreasing

CONF = cfg.CONF
_ceil = Ceilometer()
_nova = Nova()


class DynamicSchedulerManager(Manager):
    """
    This class is responsible for making vm migration decisions, including underload and overload detected,
    and conducting specific migration tasks
    """
    target = messaging.Target()

    def __init__(self, *args, **kwargs):
        super(DynamicSchedulerManager, self).__init__(service_name='hades_dynamic_scheduler',
                                                      *args, **kwargs)

    def handle_underload(self, host):
        vms = _nova.getInstancesOnHost(host)
        vms_cpu_ram = []
        for vm in vms:
            vms_cpu_ram.append((_ceil.get_vm_cpu(vm), _ceil.get_vm_ram(vm), vm))

        hosts = _nova.getComputeHosts()
        hosts_cpu, hosts_ram = dict(), dict()
        for h in hosts:
            h_info = _nova.inspect_hosts(h)
            hosts_cpu[h] = h_info['cpu']['total'] - h_info['cpu']['used']
            hosts_ram[h] = h_info['mem']['total'] - h_info['mem']['used']

        sche_place = best_fit_decreasing(hosts_cpu, hosts_ram, vms_cpu_ram)

        if not sche_place:
            print "No available hosts to hold vms on underload hosts..."
        else:
            print "start underload vm migrations"
            migrate_vms(sche_place)
            print "complete underload vm migrations"
        # TODO there may add operation of deactivate underload hosts using STR(Suspend to Ram)

    def handle_overload(self):
        # TODO complete
        pass
