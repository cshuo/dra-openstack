# -*- coding: utf-8 -*-
from .OpenstackService import *
from ...Utils.HttpUtil import OpenstackRestful
from ..Conf import OpenstackConf


class Nova(OpenstackService):

    def __init__(self):

        OpenstackService.__init__(self)
        self.restful = OpenstackRestful(self.tokenId)

    def getInstances(self):
        """
        get instances that belong to a tenant
        """
        url = "%s/v2/%s/servers" % (OpenstackConf.NOVA_URL, self.tenantId)

        result = self.restful.getResult(url)
        servers = result['servers']
        instances = []
        for s in servers:
            instances.append(str(s['id']))
        return instances

    def inspect_instance(self, vm_uuid):
        """
        Get detail info of a instance
        :param vm_uuid: the uuid of the instance
        :return: dict info of the instance
        """
        url = "{0}/v2/{1}/servers/{2}".format(OpenstackConf.NOVA_URL, self.tenantId, vm_uuid)
        return self.restful.get_req(url)['server']

    def getInstancesOnHost(self, host):
        url = "%s/v2/%s/servers?host=%s" % (OpenstackConf.NOVA_URL, self.tenantId, host)

        result = self.restful.getResult(url)
        servers = result['servers']

        instances = []
        for s in servers:
            instances.append(str(s['id']))

        return instances

    def getComputeHosts(self):
        url = "%s/v2/%s/os-hosts" % (OpenstackConf.NOVA_URL, self.tenantId)
        result = self.restful.getResult(url)
        hostsList = result['hosts']
        hosts = []
        for host in hostsList:
            print host
            if host['service'] == 'compute':
                hosts.append(str(host['host_name']))
        return hosts

    def inspect_host(self, host):
        """
        Get the detail msg of a specific host
        :param host: host to inspect
        :return: dict info of a host
        """
        url = "%s/v2/%s/os-hosts/%s" % (OpenstackConf.NOVA_URL, self.tenantId, host)
        results = self.restful.get_req(url)['host']
        assert results[0]['resource']['project'] == '(total)'
        assert results[1]['resource']['project'] == '(used_now)'
        info = dict()
        info['cpu'] = {'total': results[0]['resource']['cpu'], 'used': results[1]['resource']['cpu']}
        info['mem'] = {'total': results[0]['resource']['memory_mb'], 'used': results[1]['resource']['memory_mb']}
        info['disk'] = {'total': results[0]['resource']['disk_gb'], 'used': results[1]['resource']['disk_gb']}
        return info

    def liveMigration(self, instance_id, host):
        """ live migrate an instance to dest host """
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=OpenstackConf.NOVA_URL,
                                                                    tenant=self.tenantId, instance=instance_id)
        values = {"os-migrateLive": {"block_migration": "true", "host": host, 'disk_over_commit': "false"}}
        self.restful.post_req(url, values)


if __name__ == "__main__":
    nova = Nova()
    # print nova.getInstances()
    # for instance in instances:
    #    print instance.getId()
    #
    # host = Host("compute1", OpenstackConf.COMPUTE1_HOST)
    #
    # Nova.liveMigration(instances[0], host)
    # hosts = nova.getHosts()
    # for host in hosts:
    #    print host.getHostName()
    #
    # nova.liveMigration('c3f12b05-d9ed-4691-a41e-4de8def65d58', "compute2")
    # print nova.getInstancesOnHost('compute1')
    # nova.liveMigration('007a49ac-9f7e-4440-8b3d-514b4737879f', "compute1")
    # print nova.getComputeHosts()
    # nova.test('compute1')
    # print nova.inspect_host('compute1')
    print nova.inspect_instance('c3f12b05-d9ed-4691-a41e-4de8def65d58')['status']
