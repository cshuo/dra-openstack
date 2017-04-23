# coding: utf-8
# this file contains algorithms for detecting when a host is underload

import logging
from ..Openstack.Service.Ceilometer import Ceilometer
from ..Utils.logs import draLogger


METER_NAME = 'compute.node.cpu.percent'
_ceil = Ceilometer()
# logger = logging.getLogger("DRA.detector")
logger = draLogger("DRA.detector")


def last_n_average_threshold(threshold, n, hostname):
    """
    judging whether a host is underlaod according to its n hours average cpu statistics
    :param threshold: the threshold set in dra.conf
    :param n: the number of hours to average
    :param hostname: the host to judge
    :return: bool value
    """
    avg_statistic = _ceil.last_n_average_statistic(n, hostname+'_'+hostname, METER_NAME)
    logger.info('avg_statistic of cpu: ' + str(avg_statistic))
    if avg_statistic < threshold:
        return True
    return False
