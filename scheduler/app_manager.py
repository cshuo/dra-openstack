# -*- coding: utf-8 -*-
import requests
from ..Openstack.Conf import OpenstackConf
from ..detector.zabbixApi import (
    get_prbl_triggers,
    get_token,
    get_hostid_by_name,
    create_web_trigger,
    create_web_scenario
)


def get_sick_app():
    """
    获取出现性能故障的应用
    Note: get problemed app from zabbix or by other means
    :return:
    """
    zb_token = get_token(OpenstackConf.ZABBIX_USER, OpenstackConf.ZABBIX_PASSWD)
    problem_triggers = get_prbl_triggers(zb_token)
    sick_apps = []
    for tg in problem_triggers:
        if "web_trigger" in tg['description']:
            sick_apps.append(tg['description'].split("#")[1].strip())
    return sick_apps


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


def init_zabbix_web():
    """
    初始化web应用对应scenario和trigger, 只需要进行一次初始化操作;
    :return:
    """
    apps_url = OpenstackConf.REST_URL + "apps"
    r = requests.get(apps_url)
    if r.status_code != 200:
        print "Fail to fetch app info !!!!!!!!!!!"
    apps = r.json()

    zb_token = get_token(OpenstackConf.ZABBIX_USER, OpenstackConf.ZABBIX_PASSWD)
    default_hostid = get_hostid_by_name(zb_token, OpenstackConf.CONTROLLER)

    for app in apps:
        info = create_web_scenario(zb_token, default_hostid, app['app'], app['url'], OpenstackConf.ZABBIX_WEB_INTERVAL)
        print "#################: init web scenario ", len(info)
        if len(info) > 0:  # tigger not created before
            create_web_trigger(zb_token, OpenstackConf.CONTROLLER, app['app'], app['threshold'], OpenstackConf.ZABBIX_TRIGGER_NUM)


if __name__ == '__main__':
    pass
    # apps = get_sick_app()
    # diagnosis = get_all_diagnosis(apps)
    # print diagnosis
