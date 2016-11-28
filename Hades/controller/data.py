# -*- coding: utf-8 -*-

from ...Openstack.Service.Nova import Nova
_nova = Nova()

class ComputeNodeInfo():
    compute_node_info = {}

    def __init__(self):
        pass

    def clean_node_info(self):
        """
        @doc:
        """
        self.compute_node_info.clear()
    
    
    def add_node_info(self, node_id, node_info):
        """
        """
        self.compute_node_info[node_id] = node_info


    def check_node_nums(self):
        """
        """
        return len(_nova.getComputeHosts()) == len(self.get_node_info())

    
    def get_node_info(self):
        """
        """
        return self.compute_node_info
