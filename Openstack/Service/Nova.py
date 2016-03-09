__author__ = 'pike'

import urllib2
import json

from dra.Openstack.Service.OpenstackService import *
from dra.Utils.HttpUtil import OpenstackRestful
from dra.Openstack.Conf import OpenstackConf
from dra.Openstack.Entity.Instance import *
from dra.Openstack.Entity.Host import *


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
        for i in range(len(servers)):
            instances.append(Instance(servers[i]['id']))

        return instances

    def getInstancesOnHost(self, host):
        url = "%s/v2/%s/servers?host=%s" % (OpenstackConf.NOVA_URL, self.tenantId, host)

        result = self.restful.getResult(url)
        servers = result['servers']

        instances = []
        for i in range(len(servers)):
            instances.append(Instance(servers[i]['id']))

        return instances

    #def getHosts(self):
    #
    #    url = "%s/v2/%s/os-hosts" % (OpenstackConf.NOVA_URL, self.tenantId)
    #
    #    result = self.restful.getResult(url)
    #
    #    hostsList = result['hosts']
    #    hosts = []
    #    for host in hostsList:
    #        hosts.append(Host(host['host_name'], host['service']))
    #
    #    return hosts

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


if __name__ == "__main__":
    nova = Nova()
    #instances = nova.getInstances()
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
    #
    nova.liveMigration('c3f12b05-d9ed-4691-a41e-4de8def65d58', "compute2")
    #nova.getInstancesOnHost('compute2')
    #nova.liveMigration('007a49ac-9f7e-4440-8b3d-514b4737879f', "compute1")
    #print nova.getComputeHosts()
