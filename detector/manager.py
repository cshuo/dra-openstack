# coding: utf-8

import socket
import time
from oslo_config import cfg

from . import (
    overload,
    underload,
    vm_selection
)
from ..Utils.common import cal_migration_time
from ..Openstack.Service import (
    utils,
    Ceilometer,
    Nova
)
from ..Hades.scheduler.rpcapi import DynamicSchedulerApi


CONF = cfg.CONF

# TODO read from conf file
LOOP_INTERVAL = 240  # seconds
UNDERLOAD_THRESHOLD = 20
OVERLOAD_THRESHOLD = 90
OTF_THRESHOLD = 0.8
TIME_LENGTH = 1  # for 1 hour statistics
HOSTNAME = socket.gethostname()

_nova = Nova.Nova()
_ceil = Ceilometer.Ceilometer()
# FIXME topic and exchange here may not registered
_sche_api = DynamicSchedulerApi(CONF.hades_scheduler_topic, CONF.hades_exchange)


def start():
    """
    start local manager to detect underload or overload
    """
    while True:
        try:
            execute()
            time.sleep(LOOP_INTERVAL)
            print "looping..."
        except (KeyboardInterrupt, SystemExit):
            print "Local manager exit now..."
            break


def execute():
    """
    Execute an iteration of compute node's load detection
    """
    vms_ram = utils.get_host_vms_ram(HOSTNAME)
    bandwidths = _nova.get_interhost_bandwidth(HOSTNAME)
    migration_time = cal_migration_time(vms_ram.values(), bandwidths.values())

    # FIXME: read from conf file
    underload_detect = underload.last_n_average_threshold
    # overload_detect = overload.last_n_average_threshold
    overload_detect = overload.otf

    underld = underload_detect(UNDERLOAD_THRESHOLD, TIME_LENGTH, HOSTNAME)
    # overld = overload_detect(migration_time, OVERLOAD_THRESHOLD, TIME_LENGTH, HOSTNAME)
    overld = overload_detect(migration_time, OTF_THRESHOLD, TIME_LENGTH, HOSTNAME)

    if underld:
        # FIXME here should add some response info
        print 'underload detected...'
        ret_dict = _sche_api.handle_underload({}, HOSTNAME)
        if ret_dict['done']:
            print "underload exception processed ok..."
        elif ret_dict['info'] == 'delay':
            print "delay detector to get new statistics, as new vms were placed..."
            time.sleep(LOOP_INTERVAL)  # NOTE: sleep sometime to wait new statistics
        else:
            print ret_dict['info']
    elif overld:
        # NOTE here selecting only one vm, may modify later...
        selected_vm = list()
        # FIXME: use vm selection algo defined in conf file
        selected_vm.append(vm_selection.random_selection(HOSTNAME, TIME_LENGTH))
        print 'underload detected..., selected vm list is: ', str(selected_vm)
        ret_dict = _sche_api.handle_overload({}, HOSTNAME, selected_vm)
        print ret_dict['info']
    else:
        print 'system resource status ok...'


if __name__ == '__main__':
    start()
