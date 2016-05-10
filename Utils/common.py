# coding: utf-8
import numpy as np


def cal_migration_time(vm_rams, bandwidths):
    """
    calculate average migration time from list of vms ram usage of a host
    and list of bandwidth
    :param vm_rams: list of vms' ram usage in MB
    :param bandwidths: list of bandwidth between the hosts and others in MB/s
    :return: average migration of a host
    """
    if vm_rams:
        return np.mean(vm_rams) / np.mean(bandwidths)
    return 0
