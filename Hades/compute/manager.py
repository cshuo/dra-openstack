# -*- coding: utf-8 -*-

import socket
import datetime
import logging
import oslo_messaging as messaging
from oslo_config import cfg
from ..Manager import Manager

from ..controller.rpcapi import ControllerManagerApi
from ...Openstack.Service.Nova import Nova
from ...Openstack.Service.utils import get_vms_overview
from ...Utils.logs import draLogger
from ...detector import (
    overload,
    underload,
    vm_selection
)


CONF = cfg.CONF
_nova = Nova()

UNDERLOAD_THRESHOLD = 0
OVERLOAD_THRESHOLD = 80
TIME_LENGTH = 0.05  # for 1 hour statistics
HOSTNAME = socket.gethostname()
# logger = logging.getLogger("DRA.computeService")
logger = draLogger("DRA.computeService")


class ComputeManager(Manager):
    """
    @doc:
    """
    target = messaging.Target()

    def __init__(self, *args, **kwargs):
        super(ComputeManager, self).__init__(service_name='hades_compute_manager',
                *args, **kwargs)

    def res_health_check(self, ctxt):
        """
        receive a req from controller to check node's health, underload or overload
        """
        logger.info(socket.gethostname() + " resource health check.")
        controller_api = ControllerManagerApi(CONF.hades_controller_topic, CONF.hades_exchange)
        node_info = {'res': _nova.inspect_host(HOSTNAME), 'meters': get_vms_overview(HOSTNAME)}

        vms = _nova.getInstancesOnHost(HOSTNAME)
        if len(vms) < 1:
            logger.info("sleep mode...")
            node_info["status"] = "sleeping"
            node_info["select_vms"] = []
            controller_api.collect_compute_info({}, HOSTNAME, node_info)
            return

        underld = underload.last_n_average_threshold(UNDERLOAD_THRESHOLD,
                TIME_LENGTH, HOSTNAME)
        if underld:
            logger.info("underload detected...")
            node_info["status"] = "underload"
            node_info["select_vms"] = []
            controller_api.collect_compute_info({}, HOSTNAME, node_info)
            return

        overld = overload.last_n_average_threshold(0, OVERLOAD_THRESHOLD,
                TIME_LENGTH, HOSTNAME)
        if overld:
            logger.info("overload detected...")
            node_info["status"] = "overload"
            # NOTE: change this to OD_based selecetion
            node_info["select_vms"] = vm_selection.od_vm_select(HOSTNAME, TIME_LENGTH)
            logger.info("OD selected VMS: " + str(node_info["select_vms"]) + "\n")
            controller_api.collect_compute_info({}, HOSTNAME, node_info)
            return;

        logger.info("Node: " + HOSTNAME + "'s resource status is ok...\n")
        node_info["status"] = "healthy"
        node_info["select_vms"] = []
        controller_api.collect_compute_info({}, HOSTNAME, node_info)
