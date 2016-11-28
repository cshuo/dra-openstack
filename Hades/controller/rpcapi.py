# -*- coding: utf-8 -*_


from oslo_config import cfg
from ..BaseRpcApi import BaseAPI

CONF = cfg.CONF

DEFAULT_SERVER = "pike"
RPC_TIMEOUT = 1000

class ControllerManagerApi(BaseAPI):
    """
    client side of controller manager
    """
    def __init__(self, topic, exchange):
        super(ControllerManagerApi, self).__init__(topic, exchange)

    def collect_compute_info(self, ctxt, host_id, host_info):
        """
        send information to controller node, and store it.
        """
        cctxt = self.client.prepare(server=DEFAULT_SERVER, timeout=RPC_TIMEOUT)
        cctxt.cast(ctxt, "collect_compute_info", host_id=host_id, host_info=host_info)


    def all_info_fetched(self, ctxt):
        """
        whether having received all nodes' information
        """
        cctxt = self.client.prepare(server=DEFAULT_SERVER, timeout=RPC_TIMEOUT)

        return cctxt.call(ctxt, "all_info_fetched")

    def clean_node_info(self, ctxt):
        """
        reset compute node information
        """
        cctxt = self.client.prepare(server=DEFAULT_SERVER, timeout=RPC_TIMEOUT)
        cctxt.cast(ctxt, "clean_node_info")

    def get_nodes_info(self, ctxt):
        """
        get all nodes' info
        """
        cctxt = self.client.prepare(server=DEFAULT_SERVER, timeout=RPC_TIMEOUT)
        return cctxt.call(ctxt, "get_nodes_info")


if __name__ == "__main__":
    ctrlApi = ControllerManagerApi(CONF.hades_controller_topic, CONF.hades_exchange)
    if ctrlApi.all_info_fetched({}) == False:
        print "not complete"
