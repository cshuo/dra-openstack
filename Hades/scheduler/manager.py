# -*- coding: utf-8 -*-

import oslo_messaging as messaging
from oslo_config import cfg

from ..Manager import Manager
from ...Openstack.Service.Ceilometer import Ceilometer
from ...Openstack.Service.Nova import Nova
from ...Openstack.Service.utils import migrate_vms
from ...Openstack.Conf import OpenstackConf
from .vm_placement import best_fit_decreasing
from .utils import get_queue_msg_num

CONF = cfg.CONF
_ceil = Ceilometer()
_nova = Nova()


class DynamicSchedulerManager(Manager):
    """
    This class is responsible for making vm migration decisions, including underload and overload detected,
    and conducting specific migration tasks
    """
    target = messaging.Target()
    # as requests is processed serially, the previous req may migrate vm to next underload host in the queue,
    # thus, after the next load_exception host may not underload now.
    # this list add hosts that in sche_place, as long as the rabbitmq is not empty meantime.
    _involved_hosts = []

    def __init__(self, *args, **kwargs):
        super(DynamicSchedulerManager, self).__init__(service_name='hades_dynamic_scheduler',
                                                      *args, **kwargs)

    def handle_underload(self, ctxt, host):
        """
        Handle request for managing underload host detected, evacuate all vms of the underload
        hosts, and set the host to str if possible
        @param ctxt:
        @param host: the underload host name
        @return:
        """
        print "-------------------------before process, inv hosts: ", self._involved_hosts
        if host in self._involved_hosts:
            # rabbitmq is not empty
            if not get_queue_msg_num(CONF.hades_scheduler_topic + '.' + OpenstackConf.DEFAULT_RPC_SERVER):
                self._involved_hosts = []
            return {'done': False, 'info': 'delay'}

        vms = _nova.getInstancesOnHost(host)
        print "vms on underload host is: ", vms
        vms_cpu_ram = []
        for vm in vms:
            vm_info = _nova.inspect_instance(vm)
            vms_cpu_ram.append((vm_info['cpu'], vm_info['ram'], vm))

        hosts = _nova.getComputeHosts()
        # exclude the underload host
        hosts.remove(host)

        # get available cpu and ram msg of all candidate hosts
        hosts_cpu, hosts_ram = dict(), dict()
        for h in hosts:
            h_info = _nova.inspect_host(h)
            print h_info
            hosts_cpu[h] = h_info['cpu']['total'] - h_info['cpu']['used']
            hosts_ram[h] = h_info['mem']['total'] - h_info['mem']['used']

        # get placement decision using specific algo
        sche_place = best_fit_decreasing(hosts_cpu, hosts_ram, vms_cpu_ram)
        print 'schedule plan is: \n', sche_place

        # TODO there may add operation of deactivate underload hosts using STR(Suspend to Ram)
        if not sche_place:
            print "No available hosts to hold vms on underload hosts..."
            if not get_queue_msg_num(CONF.hades_scheduler_topic + '.' + OpenstackConf.DEFAULT_RPC_SERVER):
                self._involved_hosts = []
            return {'done': False, 'info': 'no available hosts to hold vms of the underload hosts'}
        else:
            print "start underload vm migrations"
            migrate_vms(sche_place)
            print "complete underload vm migrations"
            if not get_queue_msg_num(CONF.hades_scheduler_topic + '.' + OpenstackConf.DEFAULT_RPC_SERVER):
                print "------------------rabbit mq is empty..., clear inv_hosts"
                self._involved_hosts = []
            else:
                print "------------------rabbit mq is not empty now..."
                self._involved_hosts = list(set(self._involved_hosts + sche_place.values()))
                print "------------------involved hosts: ", self._involved_hosts
            return {'done': True, 'info': 'evacuate vms of the underload host to others successfully'}

    def handle_overload(self, ctxt, host, vms):
        """
        handle request for managing overload host detected, place vms selected by local manager
        to other hosts.
        @param ctxt:
        @param host: overload host
        @param vms: vms selected from the overload host to migrate
        """
        # NOTE may consolidate with upper underload methods
        vms_cpu_ram = []
        for vm in vms:
            vm_info = _nova.inspect_instance(vm)
            vms_cpu_ram.append((vm_info['cpu'], vm_info['ram'], vm))

        hosts = _nova.getComputeHosts()
        # exclude the overload host
        hosts.remove(host)
        hosts_cpu, hosts_ram = dict(), dict()
        for h in hosts:
            h_info = _nova.inspect_host(h)
            hosts_cpu[h] = h_info['cpu']['total'] - h_info['cpu']['used']
            hosts_ram[h] = h_info['mem']['total'] - h_info['mem']['used']

        sche_place = best_fit_decreasing(hosts_cpu, hosts_ram, vms_cpu_ram)

        if not get_queue_msg_num(CONF.hades_scheduler_topic + '.' + OpenstackConf.DEFAULT_RPC_SERVER):
            self._involved_hosts = []
        else:
            self._involved_hosts = list(set(self._involved_hosts + sche_place.values()))

        if not sche_place:
            print "No available hosts to hold vms on overload hosts..."
            return {'done': False, 'info': 'no available hosts to hold vms of the overload hosts'}
        else:
            # TODO may activate some STR hosts before doing migrations
            print "start overload vm migrations"
            migrate_vms(sche_place)
            print "complete overload vm migrations"
            return {'done': True, 'info': 'vms selected from overload host has placed properly'}

    def test_sche(self, ctxt, arg):
        print 'arg recved is: ', arg
        return {'done': True, 'info': 'this is a test'}
