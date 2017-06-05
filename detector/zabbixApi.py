# -*- encoding: utf-8 -*-

import json
import urllib2
from ..Openstack.Conf import OpenstackConf

"""bsed url and required header"""
url = "http://20.0.1.12/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
controller = 'kolla0'


def fetch_req_result(data):
    # create request object
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key, header[key])
    # get host list
    try:
        result = urllib2.urlopen(request)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'Fetch result failed: ', e.reason
        elif hasattr(e, 'code'):
            print 'Fatch result failed: ', e.code
        return None
    else:
        response = json.loads(result.read())
        if 'result' not in response:
            return {}
        return response['result']


def get_token(username, password):
    # auth user and password
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": username,
                "password": password
            },
            "id": 0
        })
    return fetch_req_result(data)


def get_hostgroup(token):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": ["groupid", "name"],
            },
            # the auth id is what auth script returns, remeber it is string
            "auth": token,
            "id": 1,
        })
    # create request object
    return fetch_req_result(data)


def get_hosts(token, group_id):
    # request json
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "name"],
                "groupids": str(group_id),
            },
            # theauth id is what auth script returns, remeber it is string
            "auth": token,
            "id": 1,
        })
    return fetch_req_result(data)


def get_hostid_by_name(token, host):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "name"],
                "filter": {
                    "host": [
                        host,
                    ]
                }
            },
            "auth": token,
            "id": 1,
        })
    rs = fetch_req_result(data)
    if not rs:
        return ""
    return rs[0]['hostid']


def get_metrics(token, host_id, keyname=""):
    # request json
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": ["itemids", "key_"],
                "hostids": host_id,
                "search": {
                    "key_": keyname
                },
                # NOTE:This is for including web items in the querying result
                "webitems": 1
            },
            # theauth id is what auth script returns, remeber it is string
            "auth": token,
            "id": 1,
        })
    return fetch_req_result(data)


def get_web_scn(token, host_id):
    # request json
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "httptest.get",
            "params": {
                "output": "extend",
                "hostids": host_id,
            },
            # the auth id is what auth script returns, remeber it is string
            "auth": token,
            "id": 1,
        })
    return fetch_req_result(data)


def get_web_detail(token, web_id):
    # request json
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "httptest.get",
            "params": {
                "output": "extend",
                "selectSteps": "extend",
                "httptestids": web_id
            },
            # the auth id is what auth script returns, remember it is string
            "auth": token,
            "id": 1,
        })
    return fetch_req_result(data)


def get_metric_history(token, item_id, limit):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,
                "itemids": item_id,
                "limit": limit
            },
            "auth": token,  # theauth id is what auth script returns, remeber it is string
            "id": 1,
        })
    # create request object
    return fetch_req_result(data)


def get_prbl_triggers(token):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": [
                    "triggerid",
                    "description",
                    "priority"
                ],
                "only_true": 1,
                "filter": {
                    "value": 1
                },
                "sortfield": "priority",
                "sortorder": "DESC"
            },
            "auth": token,
            "id": 1,
        })
    # create request object
    return fetch_req_result(data)


def create_web_scenario(token, hostid, app_name, url, interval):
    """
    根据本体描述,创建一个web应用对应的zabbix web scenario
    :param token:
    :param hostid:
    :param app_name:
    :param url:
    :param interval: 执行周期
    :return:
    """
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "httptest.create",
        "params": {
            "name": "web#" + app_name,
            "hostid": hostid,
            "delay": interval,
            "steps": [
                {
                    "name": "APP_URL",
                    "url": url,
                    "status_codes": 200,
                    "no": 1
                },
            ]
        },
        "auth": token,
        "id": 1
    })
    return fetch_req_result(data)


def create_web_trigger(token, host, app_name, threshold, interval):
    """
    根据本体描述创建一个web应用的trigger, 一般指相应时间对应的trigger;
    :param token:
    :param host:
    :param app_name:
    :param threshold:
    :param interval:
    :return:
    """
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "trigger.create",
        "params": {
            "description": "web_trigger#" + app_name,
            "expression": "{%s:web.test.time[web#%s,APP_URL,resp].avg(#%s)}>%s" % (host, app_name, interval, threshold),
        },
        "auth": token,
        "id": 1
    })
    return fetch_req_result(data)


def get_metric_avg(token, types, name, limit):
    """
    获取应用性能参数在指定的一段时间内的平均值, 性能参数有：web的RT， DB的qps等；
    :param token: 
    :param types: 应用类型，目前是web 和 db;
    :param name: 应用的名称；
    :param limit: 用来求平均值的监控值得个数；
    :return: 
    """
    # 根据不同的应用类型获取对应metric的item_id
    controller_id = get_hostid_by_name(token, OpenstackConf.CONTROLLER)
    if types == 'web':
        web_items = get_metrics(token, controller_id, 'web.test.time')
        for item in web_items:
            if name in item['key_']:
                mtc_id = item['itemid']
    elif types == 'db':
        # TODO 添加对DB性能数据的获取.
        pass

    return cal_avg(get_metric_history(token, mtc_id, limit))


def cal_avg(datas):
    print datas
    if len(datas) < 1:
        return 0
    sums = 0.0
    for d in datas:
        sums += float(d['value'])
    return round(sums/len(datas), 3)


if __name__ == '__main__':
    token = get_token('Admin', 'zabbix')
    # print token
    # print get_hostgroup(token)
    # print get_hostid_by_name(token, "kolla0")
    # print get_metrics(token, '10105', 'web.test.time')
    # print get_web_scn(token, "10105")
    # print get_web_detail(token, "7")
    print get_metric_avg(token, 'web', 'web-1', 2)
    # print get_metric_history(token, "24084", 10)
    # print get_prbl_triggers(token)
    # print get_sick_app()
    # print create_web_scenario(token, "10105", "web-1", "http://114.212.189.132/html/", "30")
    # print create_web_trigger(token, "kolla0", "web-1", "0.001", "4")
    #
    # print create_web_scenario(token, "10084", "web-2", "http://114.212.189.132/html/", "30")
    # print create_web_trigger(token, "kolla2", "web-2", "0.001", "4")
