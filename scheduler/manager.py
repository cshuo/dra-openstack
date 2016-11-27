# -*- coding: utf-8 -*- 

import time
import datetime

from ..Openstack.Service import Nova
from ..detector.zabbixApi import (
    get_token,
    get_prbl_triggers
)
from ..Utils import ontlg

LOOP_INTERVAL = 180
ZABBIX_USERNAME = 'Admin'
ZABBIX_PASSWORD = 'zabbix'
nova = Nova.Nova()


def exec_sche():
    while True:
        try:
            sche()
            time.sleep(LOOP_INTERVAL)
            print "looping..."
        except (KeyboardInterrupt, SystemExit):
            print "Scheduler exit now..."
            break


"""
scheduling process for dealing application alerts inside the vms
"""
def sche():
    zabbix_token = get_token(ZABBIX_USERNAME, ZABBIX_PASSWORD)
    problem_triggers = get_prbl_triggers(zabbix_token)
    candi_instances = {}

    for prbl_trg in problem_triggers:
        """ TODO: add other alert type """
        if "RT" in prbl_trg['description']:
            print prbl_trg['description']
            instance_name = prbl_trg['description'].split('#')[1].strip()
            app_host_id = nova.get_id_from_name(instance_name)
            """ add response time trigger fact to ontology """
            fact_name = "RTLong_"+datetime.datetime.now().isoformat
            ontlg.add_ontlg_fact(fact_name, "RTLong")
            candi_instances[app_host_id] = ontlg.infer_ontlg(fact_name)

    for vm_id, val in candi_instances.items():
        print "Resize ", vm_id 
        vm_sche(vm_id, val)
        # nova.resize_instance(inst, flavor_sche(inst))


"""
scheduling the host vm of sick apps according to the inferencing results from ontology
"""
def vm_sche(vm_id, infer_result):
    """ 
    Potential Actions:
      - migrate the vm if the load of intered vm is heavy.
      - the load is not heavy, increase the flavor
    """
    nova.resize_instance(vm_id, flavor_sche(vm_id))


"""
schedule a proper flavor for the vm.
"""
def flavor_sche(instance_id):
    flavor_id = nova.inspect_instance(instance_id)['flavor']['id'].strip()
    print flavor_id
    if int(flavor_id) < 5:
        return str(int(flavor_id)+1)
    else:
        return flavor_id


if __name__ == '__main__':
    print "ok"
    # exec_sche()
    # print flavor_sche("aee77f2e-5ffa-4092-8442-4465357a0d36")
