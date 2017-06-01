# -*- coding: utf-8 -*-
# main controller of the dynamic resource allocation

from oslo_config import cfg
import time

from ..Hades.controller.rpcapi import ControllerManagerApi
from ..Hades.compute.rpcapi import ComputeManagerApi
from ..Openstack.Service.Nova import Nova, append_log_db
from ..Openstack.Service.utils import get_host_overview
from ..Openstack.Service.webSkt import ServerThread, SocketHandler
from ..Utils.logs import draLogger
from .vm_placement import (
    get_migrt_plan,
    get_migrt_plan_underload
)
from ..Openstack.Service.utils import migrate_vms
from .app_manager import(
    get_all_diagnosis,
    get_sick_app,
    init_zabbix_web
)

# from ..detector.zabbixApi import (
#     get_token,
#     get_prbl_triggers,
# )


LOOP_INTERVAL = 30  # 300s
ZABBIX_USERNAME = "Admin"
ZABBIX_PASSWORD = "zabbix"
CONF = cfg.CONF
_nova = Nova()
logger = draLogger("DRA.scheduler")


def diagnose_apps():
    """
    对所有应用进行检查, 判断是否有应用出现性能问题, 出现问题进行资源关联性分析, 得到相关诊断信息.
    :return:
    """
    logger.info("应用诊断...")
    s_apps = get_sick_app()
    diagnosis = get_all_diagnosis(s_apps)
    # 没有异常应用, 更新web层拓扑图.
    if len(diagnosis) == 0:
        logger.info("重置拓扑视图...")
        diagnosis = [{'type': 'reset'}]
    else:
        SocketHandler.write_to_clients('scheduler', content='应用: ' + str(s_apps) + ' 出现性能异常.')
    SocketHandler.write_to_clients('rel_status', msg=diagnosis)


def optimize_allocation():
    """
    资源的动态调度.
    :return:
    """
    ctrl_api = ControllerManagerApi(CONF.hades_controller_topic, CONF.hades_exchange)
    compute_nodes = _nova.getComputeHosts()
    for node in compute_nodes:
        ComputeManagerApi(CONF.hades_compute_topic, CONF.hades_exchange, node).res_health_check({})

    while 1:
        # all nodes info are collected
        # NOTE: more properly to set timeout
        if ctrl_api.all_info_fetched({}):
            break
        time.sleep(1)

    logger.info("All nodes' info got")

    # get compute nodes' resource information and health status
    nodes_info = ctrl_api.get_nodes_info({})

    # get app's SLA performance degradation
    # zabbix_token = get_token(ZABBIX_USERNAME, ZABBIX_PASSWORD)
    # problem_triggers = get_prbl_triggers(zabbix_token)
    # update nodes' info
    # update_node_info(nodes_info, problem_triggers)

    allocation_map = {}
    sel_vms = []
    underload_host = []
    sleep_host = []
    meters_updating = []

    for host, info in nodes_info.items():
        SocketHandler.write_to_clients('status', host=host, status=info['status'])
        meters_updating += info['meters']
        if info["select_vms"]:
            sel_vms += info["select_vms"]
            append_log_db(host, 'warn', '计算节点: %s 出现超载状况' % str(host))
        elif info["status"] == "underload":
            underload_host.append(host)
            append_log_db(host, 'warn', '计算节点: %s 出现欠载状况' % str(host))
        elif info["status"] == "sleeping":
            sleep_host.append(host)

    # update pm's and vm's popup meters in topology page
    # print "##################\n", meters_updating
    meters_updating += get_host_overview()
    SocketHandler.write_to_clients('data', data=meters_updating)

    allocation_map.update(get_migrt_plan(sel_vms, nodes_info, underload_host, sleep_host))

    # The consolidation of underloaded server is success <==> all vms on it can be reallocated.
    for host in underload_host:
        info_back = nodes_info.copy()
        migrt_map = get_migrt_plan_underload(host, nodes_info, underload_host, sleep_host)
        if migrt_map:
            allocation_map.update(migrt_map)
        else:
            nodes_info = info_back.copy()

    if not allocation_map:
        logger.info("No migraions in this looping.")
    logger.info("Migration Map is: " + str(allocation_map))

    migrate_vms(allocation_map)
    ctrl_api.clean_node_info({})


def start():
    """
    start main loop of controller
    """
    # 开启websocket server, 向web层推送相关消息.
    server_tornado = ServerThread()
    server_tornado.start()
    logger.info("Starting tornado websocket server...")

    # 初始化web app对应的zabbix web scenario和对应的trigger
    init_zabbix_web()

    while True:
        try:
            logger.info("Looping a iteration...")

            diagnose_apps()  # 对应用进行健康检查

            optimize_allocation()  # 资源动态调度
            time.sleep(LOOP_INTERVAL)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Stopping main looping...")
            ServerThread.stop_tornado()
            break


def update_node_info(nodes_info, prbl_triggers):
    """
    update nodes' info (overload nodes' vms selection) according to app's problem triggers
    @param prbl_triggers:
    @param nodes_info:
    """
    for trigger in prbl_triggers:
        # TODO: add other alert type
        if "RT" in trigger["description"]:
            instance_name = trigger["description"].split("#")[1].strip()
            app_vm_id = _nova.get_id_from_name(instance_name)
            host_node = _nova.get_host_from_vid(app_vm_id)
            # NOTE only one vm is selected for now,
            # so there is no other choice for vm substitution
            if nodes_info[host_node]["status"] == 'overload':
                nodes_info[host_node]["select_vms"] = [app_vm_id]
            elif nodes_info[host_node]["status"] == 'healthy':
                assert (nodes_info[host_node]["select_vms"] == [])
                nodes_info[host_node]["select_vms"].append(app_vm_id)
            else:
                # app performance is bad, while the host is underload...
                # We assume this scenario do not exist.
                pass


if __name__ == '__main__':
    start()
