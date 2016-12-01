# -*- coding: utf-8 -*-
#
# main controller of the dynamic resource allocation
#

from oslo_config import cfg
import time
import datetime

from ..Hades.controller.rpcapi import ControllerManagerApi 
from ..Hades.compute.rpcapi import ComputeManagerApi
from ..Openstack.Service.Nova import Nova
from ..Openstack.Service.utils import migrate_vms
from .vm_placement import (
    get_migrt_plan,
    get_migrt_plan_underload
)
from ..detector.zabbixApi import (
    get_token,
    get_prbl_triggers,
)


LOOP_INTERVAL = 180    # 300s
ZABBIX_USERNAME = "Admin"
ZABBIX_PASSWORD = "zabbix"
CONF = cfg.CONF
_nova = Nova()


def optimize_allocation():
    ctrl_api = ControllerManagerApi(CONF.hades_controller_topic, CONF.hades_exchange)
    compute_nodes = _nova.getComputeHosts()
    for node in compute_nodes:
        ComputeManagerApi(CONF.hades_compute_topic, CONF.hades_exchange, node).res_health_check({})
    
    while 1:
        # all nodes info are collected
        # NOTE: more properly to set a max time to wait.
        if ctrl_api.all_info_fetched({}):
            break
        time.sleep(1)

    print datetime.datetime.now().isoformat(), "all nodes' info got"
    
    # get compute nodes' resource information and health status
    nodes_info = ctrl_api.get_nodes_info({})
 
    # get app's SLA performance degradation
    zabbix_token = get_token(ZABBIX_USERNAME, ZABBIX_PASSWORD)
    problem_triggers = get_prbl_triggers(zabbix_token)

    # update nodes' info
    update_node_info(nodes_info, problem_triggers)

    allocation_map = {}
    sel_vms = []
    underload_host = []

    for host, info in nodes_info.items():
        if info["select_vms"]:
            sel_vms += info["select_vms"]
        elif info["status"] == "underload":
            underload_host.append(host)

    allocation_map.update(get_migrt_plan(sel_vms, nodes_info))
    
    for host in underload_host:
        info_back = nodes_info.copy()
        migrt_map = get_migrt_plan_underload(host, nodes_info)
        if migrt_map:
            allocation_map.update(migrt_map)
        else:
            nodes_info = info_back.copy()
    
    if not allocation_map:
        print datetime.datetime.now().isoformat(), "No migraions in this looping."
    migrate_vms(allocation_map)

    ctrl_api.clean_node_info({})

    
def start():
    """
    start main loop of controller
    """
    while True:
        try:
            print datetime.datetime.now().isoformat(), "Looping a iteration..."
            optimize_allocation()
            time.sleep(LOOP_INTERVAL)
        except (KeyboardInterrupt, SystemExit):
            print "Stopping main looping..."
            break


def update_node_info(nodes_info, prbl_triggers):
    """
    update nodes' info (overload nodes' vms selection) according to app's problem triggers
    """
    for trigger in prbl_triggers:
        # TODO: add other alert type
        if "RT" in trigger["description"]:
            instance_name = trigger["description"].split("#")[1].strip()
            app_vm_id = _nova.get_id_from_name(instance_name)
            host_node = _nova.get_host_from_vid(app_vm_id)
            # NOTE only one vm is selected for now, 
            # so there is no other choice for vm substitution
            if(nodes_info[host_node]["status"] == 'overload'):
                nodes_info[host_node]["select_vms"] = [app_vm_id]
            elif(nodes_info[host_node]["status"] == 'healthy'):
                assert(nodes_info[host_node]["select_vms"] == [])
                nodes_info[host_node]["select_vms"].append(app_vm_id)
            else:
                # app performance is bad, while the host is underload...
                # We assume this scenario do not exist.
                pass


if __name__ == '__main__':
    start()
