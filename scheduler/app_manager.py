# -*- coding: utf-8 -*-
import random
import requests
from ..Openstack.Conf import OpenstackConf


def get_sick_app():
    """
    获取出现性能故障的应用
    TODO: get problemed app from zabbix or by other means
    :return:
    """
    # for testing...
    return [random.choice(['db-1', 'db-2'])]


def get_all_diagnosis(apps):
    """
    针对所有故障应用进行本体推理获取相关联资源信息,进行合并
    :param apps:
    :return:
    """
    rs = []
    for app in apps:
        rs += get_diagnosis(app)
    return rs


def get_diagnosis(app):
    """
    应用出现性能异常时, 获取本体推理相应消息;
    :param app:
    :return:
    """
    diag_url = OpenstackConf.REST_URL + "diagnosis"
    params = {'app': app}
    r = requests.get(diag_url, params=params)
    if r.status_code != 200:
        return []
    return r.json()


if __name__ == '__main__':
    apps = get_sick_app()
    diagnosis = get_all_diagnosis(apps)
    print diagnosis
