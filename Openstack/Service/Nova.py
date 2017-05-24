# -*- coding: utf-8 -*-

from .OpenstackService import *
from ...Utils.logs import draLogger
from ..Conf import OpenstackConf
from .webSkt import SocketHandler
import requests

logger = draLogger("Dra.Openstack.Nova")


class Nova(OpenstackService):
    def __init__(self):

        OpenstackService.__init__(self)

    def get_rest_data(self, url):
        try:
            return self.restful.get_req(url)
        except:
            logger.info("Token expires, update it now...")
            self.update_token()
            return self.restful.get_req(url)

    def post_rest_data(self, url, data):
        try:
            return self.restful.post_req(url, data)
        except:
            logger.info("Token expires, update it now...")
            self.update_token()
            return self.restful.post_req(url, data)

    def getInstances(self):
        """
        get instances that belong to a tenant
        """
        url = "%s/v2/%s/servers" % (OpenstackConf.NOVA_URL, self.tenantId)

        result = self.get_rest_data(url)
        servers = result['servers']
        instances = []
        for s in servers:
            instances.append(str(s['id']))
        return instances

    def get_id_from_name(self, name):
        """
        get instances id with specific name
        """
        url = "%s/v2/%s/servers" % (OpenstackConf.NOVA_URL, self.tenantId)
        servers = self.get_rest_data(url)['servers']
        for s in servers:
            if (str(s['name']) == name):
                return str(s['id'])
        return None

    def get_id_name_maps(self):
        url = "%s/v2/%s/servers" % (OpenstackConf.NOVA_URL, self.tenantId)
        servers = self.get_rest_data(url)['servers']
        rs = dict()
        for s in servers:
            rs[str(s['name'])] = str(s['id'])
        return rs

    def get_host_from_vid(self, vid):
        url = "{0}/v2/{1}/servers/{2}".format(OpenstackConf.NOVA_URL, self.tenantId, vid)
        info = self.get_rest_data(url)['server']
        return info["OS-EXT-SRV-ATTR:host"]

    def getInstancesOnHost(self, host):
        """
        @param host:
        @return:
        """
        url = "%s/v2/%s/servers?host=%s" % (OpenstackConf.NOVA_URL, self.tenantId, host)

        result = self.get_rest_data(url)
        servers = result['servers']

        instances = []
        for s in servers:
            instances.append(str(s['id']) + "#" + str(s['name']))
        return instances

    def getComputeHosts(self):
        url = "%s/v2/%s/os-hosts" % (OpenstackConf.NOVA_URL, self.tenantId)
        result = self.get_rest_data(url)
        hostsList = result['hosts']
        hosts = []
        for host in hostsList:
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
        results = self.get_rest_data(url)['host']
        print results
        assert results[0]['resource']['project'] == '(total)'
        assert results[1]['resource']['project'] == '(used_now)'
        info = dict()
        info['cpu'] = {'total': results[0]['resource']['cpu'], 'used': results[1]['resource']['cpu']}
        info['mem'] = {'total': results[0]['resource']['memory_mb'], 'used': results[1]['resource']['memory_mb']}
        info['disk'] = {'total': results[0]['resource']['disk_gb'], 'used': results[1]['resource']['disk_gb']}
        return info

    def get_hosts_info(self):
        url = "%s/v2/%s/os-hypervisors" % (OpenstackConf.NOVA_URL, self.tenantId)
        results = self.get_rest_data(url)
        rs = dict()
        if 'hypervisors' in results:
            hosts = results['hypervisors']
            for h in hosts:
                rs[str(h['hypervisor_hostname'])] = h['id']
        return rs

    def inspect_flavor(self, flavor_id):
        """
        Get openstack flavor info by its id, flavor contains vm's config of cpu virtual core num, ram and disk size
        :param flavor_id: id of the flavor
        :return: flavor info, disk in GB, RAM in MB, vpus num
        """
        url = "{0}/v2/{1}/flavors/{2}".format(OpenstackConf.NOVA_URL, self.tenantId, flavor_id)
        results = self.get_rest_data(url)['flavor']
        return results

    def inspect_instance(self, vm_uuid):
        """
        Get detail info of a instance
        :param vm_uuid: the uuid of the instance
        :return: dict info of the instance
        """
        url = "{0}/v2/{1}/servers/{2}".format(OpenstackConf.NOVA_URL, self.tenantId, vm_uuid)
        info = self.get_rest_data(url)['server']
        flavor_id = info['flavor']['id']
        flavor_info = self.inspect_flavor(flavor_id)
        info['disk'] = flavor_info['disk']
        info['cpu'] = flavor_info['vcpus']
        info['mem'] = flavor_info['ram']
        return info

    def resize_instance(self, instance_id, flavor_id):
        """ resize a given instance to another flavor with id=flavor_id
        @param instance_id:
        @param host:
        """
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=OpenstackConf.NOVA_URL,
                                                                    tenant=self.tenantId, instance=instance_id)
        values = {"resize": {"flavorRef": flavor_id, "OS-DCF:diskConfig": "AUTO"}}
        status_code = self.post_rest_data(url, values)
        if status_code == 202:
            logger.info("Resizing...")
        else:
            logger.warn("Failing to resizing")

    def liveMigration(self, instance_id, instance_name, host):
        """ live migrate an instance to dest host
        @rtype: None
        @param instance_name:
        @param instance_id:
        @param host:
        """
        instance_name, host = str(instance_name), str(host)
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=OpenstackConf.NOVA_URL,
                                                                    tenant=self.tenantId, instance=instance_id)
        values = {"os-migrateLive": {"block_migration": "False", "host": host, 'disk_over_commit': "False"}}
        status_code = self.post_rest_data(url, values)
        orgin_h = str(self.get_host_from_vid(instance_id))
        if status_code == 202:
            logger.info("update topology graph ...")
            # 更新调度页面信息显示
            SocketHandler.write_to_clients('update', vm_id=instance_id, host=host)
            SocketHandler.write_to_clients('scheduler', content='虚拟机 %s 迁移: 源服务器: %s ==> 目的服务器: %s' % (
                instance_name, orgin_h, host))
            SocketHandler.write_to_clients('message', host=orgin_h, content='虚拟机迁出: %s' % instance_name)
            SocketHandler.write_to_clients('message', host=host, content='虚拟机迁入: %s' % instance_name)

            # 调度过程写入系统日志数据库
            append_log_db(instance_name, 'operation', '虚拟机: %s 从 %s 迁移到 %s' % (instance_name, orgin_h, host))
            append_log_db(orgin_h, 'operation', '虚拟机: %s 迁出到计算节点 %s' % (instance_name, host))
            append_log_db(host, 'operation', '虚拟机: %s 从计算节点: %s 迁入' % (instance_name, orgin_h))

    def get_interhost_bandwidth(self, host):
        """
        Get bandwidth between the specific host and others
        :param host: the specific host
        :return dict type of bandwidth msg
        @param host:
        @return:
        """
        import random
        # TODO get real bandwidth between hosts(MB/s)
        hosts = self.getComputeHosts()
        hosts.remove(host)
        bd = dict()
        for h in hosts:
            bd[h] = random.uniform(5, 10)
        return bd


def append_log_db(holder, types, content):
    post_data = {'holder': holder, 'type': types, 'info': content};
    requests.post(OpenstackConf.LOG_URL, json=post_data)


if __name__ == "__main__":
    nova = Nova()
    # print nova.getInstances()
    # for instance in instances:
    #    print instance.getId()
    #
    # host = Host("compute1", OpenstackConf.COMPUTE1_HOST)
    #
    # nova.liveMigration('b7e9dd7c-4c5b-4614-8b04-4caaaf4c9792', "kolla2")
    # print nova.get_id_from_name('test-1')
    # print nova.inspect_host('kolla1')
    # print nova.get_hosts_info()
    print get_related('app', app='web-1')
    # print nova.getInstancesOnHost('kolla2')
    # print nova.get_host_from_vid('ae69b5fd-5d1e-4452-a90e-bcf3f1460c17')
