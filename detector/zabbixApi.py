# -*- encoding: utf-8 -*-

import json
import urllib2

"""bsed url and required header"""
url = "http://30.0.1.150/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}

def fetch_req_result(data):
    # create request object
    request = urllib2.Request(url,data)
    for key in header:
       request.add_header(key,header[key])
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
       result.close()
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
       "jsonrpc":"2.0",
       "method":"hostgroup.get",
       "params":{
           "output":["groupid","name"],
       },
       # theauth id is what auth script returns, remeber it is string
       "auth":token, 
       "id":1,
    })
    # create request object
    return fetch_req_result(data)
    

def get_hosts(token, group_id):
    # request json
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"host.get",
       "params":{
           "output":["hostid","name"],
           "groupids":str(group_id),
       },
       # theauth id is what auth script returns, remeber it is string
       "auth":token, 
       "id":1,
    })
    return fetch_req_result(data)
   

def get_metrics(token, host_id):
    # request json
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"item.get",
       "params":{
           "output":["itemids","key_"],
           "hostids":host_id,
           # NOTE:This is for including web items in the querying result
           "webitems": 1
       },
       # theauth id is what auth script returns, remeber it is string
       "auth":token, 
       "id":1,
    })
    return fetch_req_result(data)


def get_web_scn(token, host_id):
    # request json
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"httptest.get",
       "params":{
           "output":"extend",
           "hostids":host_id,
       },
       # theauth id is what auth script returns, remeber it is string
       "auth":token, 
       "id":1,
    })
    return fetch_req_result(data)


def get_web_detail(token, web_id):
    # request json
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"httptest.get",
       "params":{
           "output":"extend",
           "selectSteps": "extend",
           "httptestids":web_id
       },
       # theauth id is what auth script returns, remeber it is string
       "auth":token, 
       "id":1,
    })
    return fetch_req_result(data)


def get_metric_history(token, item_id, limit):
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"history.get",
       "params":{
           "output":"extend",
           "history":0,
           "itemids":item_id,
           "limit":limit
       },
       "auth":token, # theauth id is what auth script returns, remeber it is string
       "id":1,
    })
    # create request object
    return fetch_req_result(data)


def get_prbl_triggers(token):
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"trigger.get",
       "params":{
           "output":[
               "triggerid",
               "description",
               "priority"
           ],
           "filter": {
               "value": 1
           },
           "sortfield": "priority",
           "sortorder": "DESC"
       },
       "auth":token,
       "id":1,
    })
    # create request object
    return fetch_req_result(data)


if __name__ == '__main__':
    token = get_token('Admin', 'zabbix')
    print token
    #  print get_hostgroup(token)
    #  print get_hosts(token, '4')
    # print get_metrics(token, '10084')
    # print get_web_scn(token, "10084")
    # print get_web_detail(token, "1")
    # print get_metric_history(token, '25400', 10)
    print get_prbl_triggers(token)
