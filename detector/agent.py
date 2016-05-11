# -*-coding: utf-8-*-
import socket
import time
from oslo_config import cfg

from ..Utils.common import cal_migration_time
from ..Hades.EventService.RpcApi import EventServiceAPI
from ..Openstack.Service import (
    utils,
    Ceilometer,
    Nova
)
from . import (
    overload,
    underload,
    vm_selection
)


CONF = cfg.CONF

# TODO read from conf file
LOOP_INTERVAL = 300  # seconds
UNDERLOAD_THRESHOLD = 50
OVERLOAD_THRESHOLD = 90
OTF_THRESHOLD = 0.5
TIME_LENGTH = 1  # for 1 hour statistics
HOSTNAME = socket.gethostname()

_nova = Nova.Nova()
_ceil = Ceilometer.Ceilometer()
_event_api = EventServiceAPI(CONF.hades_eventService_topic, CONF.hades_exchange)


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
    overld = overload_detect(migration_time, OTF_THRESHOLD, TIME_LENGTH, HOSTNAME)

    if underld:
        print 'underload detected...'
        _event_api.sendEventForResult({}, 'pike', "arbiterPMA",
                                      "(dismiss (host {host}))".format(host=HOSTNAME))
        print "deal underload ended...."
    elif overld:
        # NOTE here selecting only one vm, may modify later...
        # FIXME: use vm selection algo defined in conf file
        selected_vm, vm_type = vm_selection.random_selection(HOSTNAME, TIME_LENGTH)
        print 'overload detected..., selected vm list is: ', str(selected_vm)
        _event_api.sendEventForResult({}, 'pike', "arbiterPMA",
                                      "(evacuation (instance {id}) (type MATLAB_SLAVE))".format(id=selected_vm, type=vm_type))
    else:
        print 'system resource status ok...'


if __name__ == '__main__':
    start()
