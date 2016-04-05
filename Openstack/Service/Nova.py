__author__ = 'pike'

import urllib2
import json

from .OpenstackService import *
from ...Utils.HttpUtil import OpenstackRestful
from ..Conf import OpenstackConf
from ..Entity.Instance import *
from ..Entity.Host import *


class Nova(OpenstackService):

    def __init__(self):

        OpenstackService.__init__(self)
        self.restful = OpenstackRestful(self.tokenId)


    # get instances that belong to a tenant
    def getInstances(self):

        url = "%s/v2/%s/servers" % (OpenstackConf.NOVA_URL, self.tenantId)

        result = self.restful.getResult(url)
        servers = result['servers']

        instances = []
        for s in servers:
            instances.append(str(s['name']))

        return instances

    def getInstancesOnHost(self, host):
        url = "%s/v2/%s/servers?host=%s" % (OpenstackConf.NOVA_URL, self.tenantId, host)

        result = self.restful.getResult(url)
        servers = result['servers']

        instances = []
        for s in servers:
            instances.append(str(s['name']))

        return instances

    def getComputeHosts(self):
        url = "%s/v2/%s/os-hosts" % (OpenstackConf.NOVA_URL, self.tenantId)
        result = self.restful.getResult(url)
        hostsList = result['hosts']
        hosts = []
        for host in hostsList:
            if host['service'] == 'compute':
                hosts.append(str(host['host_name']))
        return hosts

    def liveMigration(self, instance_id, host):
        """ live migrate an instance to dest host """
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=OpenstackConf.NOVA_URL,
                tenant=self.tenantId, instance=instance_id)
        values = {"os-migrateLive":{"block_migration": "true", "host":host, 'disk_over_commit':"false"}}
        self.restful.post_req(url, values)

    def vm_name_to_uuid(self, vm):
        """
        Get vm's uuid according to its name
        :param vm: name of a vm
        :return: the vm's uuid
        """
        # FIXME
        return 'random_str'

    def vm_hostname(self, vm):
        """
        Get name of the host in provision of the specific vm
        :param vm: name of vm
        :return: name of host holding the vm
        """
        # FIXME
        return 'compute1'

    def vm_status(self, vm):
        """
        Get status of a vm
        """
        # FIXME
        return 'ACTIVE'

    def inspect_hosts(self, host):
        """
        Get the detail msg of a specific host
        """
        import random
        # TODO get real msg of the host
        mem_list = [2048, 4096]  # in MB
        cpu_list = [4, 8]  # virtual cpu core in num
        disk_list = [4, 8]  # in GB
        info = dict()
        cpu_total, mem_total, disk_total = random.choice(cpu_list), random.choice(mem_list), random.choice(disk_list)

        info['cpu'] = {'total': cpu_total, 'used': random.randint(0, cpu_total)}
        info['mem'] = {'total': mem_total, 'used': random.randint(0, mem_total)}
        info['disk'] = {'total': disk_total, 'used': random.randint(0, disk_total)}
        return info

if __name__ == "__main__":
    nova = Nova()
    print nova.getInstances()
    #for instance in instances:
    #    print instance.getId()
    #
    ##host = Host("compute1", OpenstackConf.COMPUTE1_HOST)
    #
    ##Nova.liveMigration(instances[0], host)
    #hosts = nova.getHosts()
    #for host in hosts:
    #    print host.getHostName()
    #
    # nova.liveMigration('c3f12b05-d9ed-4691-a41e-4de8def65d58', "compute2")
    #print nova.getInstancesOnHost('compute1')
    #nova.liveMigration('007a49ac-9f7e-4440-8b3d-514b4737879f', "compute1")
    #print nova.getComputeHosts()
