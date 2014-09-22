
__author__ = 'pike'

from Openstack.Service.OpenstackService import *
from Openstack.Conf import OpenstackConf
from Openstack.Entity.Instance import *
from Openstack.Entity.Host import *
import urllib2
import json



class Nova(OpenstackService):

    def __init__(self):

        OpenstackService.__init__(self)


    # get instances that belong to a tenant
    def getInstances(self):

        url = "%s/v2/%s/servers" % (OpenstackConf.NOVA_URL, self.tenantId)

        serverRequest = urllib2.Request(url)
        serverRequest.add_header("Content-type", "application/json")
        serverRequest.add_header("X-Auth-Token", self.tokenId)

        response = urllib2.urlopen(serverRequest)
        result = json.loads(response.read())
        servers = result['servers']

        instances = []
        #print len(servers)
        for i in range(len(servers)):
            instances.append(Instance(servers[i]))


        return instances

    def getHosts(self):

        url = "%s/v2/%s/os-hosts" % (OpenstackConf.NOVA_URL, self.tenantId)

        serverRequest = urllib2.Request(url)
        serverRequest.add_header("Content-type", "application/json")
        serverRequest.add_header("X-Auth-Token", self.tokenId)

        response = urllib2.urlopen(serverRequest)
        result = json.loads(response.read())

        hostsList = result['hosts']
        hosts = []
        for i in range(len(hostsList)):
            hosts.append(Host(hostsList[i]['host_name'], hostsList[i]['service']))

        return hosts

    def getComputeHosts(self):

        hosts = self.getHosts()
        computeHosts = []
        for i in range(len(hosts)):
            if (hosts[i].getService() == "compute"):
                computeHosts.append(hosts[i])
        return computeHosts



    @staticmethod
    def liveMigration(instance, host):

        # connect to host
        ssh = Ssh_tool(OpenstackConf.CONTROLLER_HOST, 22, OpenstackConf.HOST_USERNAME, OpenstackConf.HOST_PASSWORD)

        #execute shell command to migrate the instance
        ssh.remote_cmd("nova " + OpenstackConf.PARAMS + " live-migration " + instance.getId() + " " + host.getHostName())




if __name__ == "__main__":
    nova = Nova()
    instances = nova.getInstances()
    print instances[0].getId()

    #host = Host("compute1", OpenstackConf.COMPUTE1_HOST)

    #Nova.liveMigration(instances[0], host)
    hosts = nova.getComputeHosts()
    print hosts[0].getHostName()
    print hosts[1].getHostName()