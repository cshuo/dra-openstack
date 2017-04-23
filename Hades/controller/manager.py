import oslo_messaging as messaging
import logging
from oslo_config import cfg
from ..Manager import Manager

from ...Openstack.Service.Nova import Nova
from ...Openstack.Conf import OpenstackConf
from ...Utils.logs import draLogger
from .data import ComputeNodeInfo

CONF = cfg.CONF
# logger = logging.getLogger("DRA.controllerService")
logger = draLogger("DRA.controllerService")


class ControllerManager(Manager):
    """
    @doc:
    """
    target = messaging.Target()
    _compute_node_info = ComputeNodeInfo()

    def __init__(self, *args, **kwargs):
        super(ControllerManager, self).__init__(service_name='hades_controller_manager', 
                *args, **kwargs)

    def collect_compute_info(self, ctxt, host_id, host_info):
        """
        receive information from compute node, and store it.
        """
        logger.info("Info of " + host_id + " :" + str(host_info))
        self._compute_node_info.add_node_info(host_id, host_info)

    def all_info_fetched(self, ctxt):
        """
        whether having received all nodes' information
        """
        # print "ControllerManager: num of nodes' info is ", len(self._compute_node_info.get_node_info()) 
        return self._compute_node_info.check_node_nums()

    def clean_node_info(self, ctxt):
        """
        reset compute node information
        """
        self._compute_node_info.clean_node_info()

    def get_nodes_info(self, ctxt):
        """
        """
        return self._compute_node_info.get_node_info()
