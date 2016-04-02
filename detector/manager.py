# coding: utf-8

import socket

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


# TODO read from conf file
UNDERLOAD_THRESHOLD = 0.2
OVERLOAD_THRESHOLD = 0.9
# for 1 hour statistics
TIME_LENGTH = 1
HOSTNAME = socket.gethostname()

_nova = Nova.Nova()
_ceil = Ceilometer.Ceilometer()

def start():
    pass


def execute():
    """
    Execute an iteration of compute node's load detection
    """
    vms_ram = utils.get_host_vms_ram(HOSTNAME)
    bandwidths = _ceil.get_interhost_bandwidth(HOSTNAME)
    migration_time = cal_migration_time(vms_ram.values(), bandwidths.values())

    # TODO: read from conf file
    underload_detect = underload.last_n_average_threshold
    overload_detect = overload.last_n_average_threshold

    underld = underload_detect(UNDERLOAD_THRESHOLD, TIME_LENGTH, HOSTNAME)
    overld = overload_detect(migration_time, OVERLOAD_THRESHOLD, TIME_LENGTH, HOSTNAME)

    if underld:
        pass
    elif overld:
        pass
    else:
        print "no violation of load threshold detected"