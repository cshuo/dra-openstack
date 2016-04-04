# coding: utf-8
from ..Openstack.Service.Ceilometer import Ceilometer


def last_n_average_threshold(migration_time, threshold, n, hostname):
    """
    judging whether a host is overload according to its n hours average cpu statistics
    :param threshold: the threshold set in dra.conf
    :param n: the number of hours to average
    :param hostname: the host to judge
    :param migration_time: not used in this function
    :return: bool value
    """
    ceilometer_inst = Ceilometer()
    if ceilometer_inst.last_n_average_statistic(n, hostname) > threshold:
        return True
    return False


def otf(migration_time, otf_threshold, n, hostname):
    """
    OTF: Overload Time Fraction
    NOTE: when a host is overload, migration time if also taken into account, 'cause
    migration also consumes lots of resource.
    :param migration_time: normalized migration time
    :param otf_threshold: the otf threshold set in dra.conf
    :param n: the number of hours to average
    :param hostname: the host to judge
    :return: bool value
    """
    ceilometer_inst = Ceilometer()
    overload_t, total_t = ceilometer_inst.last_n_otf_statistic(n, hostname)
    return (migration_time + overload_t) / \
           (migration_time + total_t) >= otf_threshold
