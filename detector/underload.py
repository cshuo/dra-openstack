# coding: utf-8
# this file contains algorithms for detecting when a host is underload

from ..Openstack.Service.Ceilometer import Ceilometer


METER_NAME = 'compute.node.cpu.percent'
_ceil = Ceilometer()


def last_n_average_threshold(threshold, n, hostname):
    """
    judging whether a host is underlaod according to its n hours average cpu statistics
    :param threshold: the threshold set in dra.conf
    :param n: the number of hours to average
    :param hostname: the host to judge
    :return: bool value
    """
    avg_statistic = _ceil.last_n_average_statistic(n, hostname+'_'+hostname, METER_NAME)
    print 'avg_statistic: ', avg_statistic
    if avg_statistic < threshold:
        return True
    return False
