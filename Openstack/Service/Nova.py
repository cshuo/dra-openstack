
__author__ = 'pike'

from Openstack.Service.OpenstackService import *
from Utils.HttpUtil import OpenstackRestful
from Openstack.Conf import OpenstackConf
from Openstack.Entity.Instance import *
from Openstack.Entity.Host import *
import urllib2
import json



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
                hosts.append(Host(host['host_name']))

        return hosts



    @staticmethod
    def liveMigration(instanceId, hostName):

        # change comupute nodes's privilege for dir /var/lib/nova/instances
        ssh_compute1 = Ssh_tool(OpenstackConf.COMPUTE1_HOST, 22, OpenstackConf.COMPUTE1_HOST_USERNAME, OpenstackConf.COMPUTE1_HOST_PASSWORD)
        ssh_compute2 = Ssh_tool(OpenstackConf.COMPUTE2_HOST, 22, OpenstackConf.COMPUTE2_HOST_USERNAME, OpenstackConf.COMPUTE2_HOST_PASSWORD)

        cmd_chmod = "chmod 777 -R /var/lib/nova/instances"
        ssh_compute1.remote_cmd(cmd_chmod)
        ssh_compute2.remote_cmd(cmd_chmod)


        # connect to host
        ssh_controller = Ssh_tool(OpenstackConf.CONTROLLER_HOST, 22, OpenstackConf.HOST_USERNAME, OpenstackConf.HOST_PASSWORD)

        #execute shell command to migrate the instance
        cmd_migrate = "nova %s live-migration %s %s" % (OpenstackConf.PARAMS, instanceId, hostName)



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
    #nova.liveMigration('5bdbf476-f046-4986-9e1d-5b078414a298', "compute2")
    nova.getInstancesOnHost('compute2')

