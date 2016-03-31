# coding: utf-8
# this file contains algorithms for detecting when a host is underload

from ..Openstack.Service import Ceilometer

def last_n_average_threshold(threshold, n, hostname):
    """
    judging whether a host is underlaod according to its n hours average cpu statistics
    :param threshold: the threshold set in dra.conf
    :param n: the number of hours to average
    :param hostname: the host to judge
    :return: bool value
    """
    ceilometer_inst = Ceilometer()
    if ceilometer_inst.last_n_average_statistic(n, hostname) < threshold:
        return True
    return False
