__author__ = 'pike'

from Utils.SshUtil import *
from Openstack.Conf import OpenstackConf
import re

rabbitmqCmd = {
    "LIST_VHOSTS" : "rabbitmqctl list_vhosts",
    "LIST_EXCHANGES" : "rabbitmqctl list_exchanges",
    "LIST_QUEUES" : "rabbitmqctl list_queues"
}

class RabbitMq:

    def __init__(self):
        # connect to host
        self.ssh = Ssh_tool(OpenstackConf.CONTROLLER_HOST, 22, OpenstackConf.HOST_ROOT_USERNAME, OpenstackConf.HOST_ROOT_PASSWORD)

    def listVhosts(self):
        result = self.ssh.remote_cmd(rabbitmqCmd["LIST_VHOSTS"])
        stdout = result["stdout"]
        vhosts = re.split("\n", stdout.read())[1:-2]
        return vhosts


    def listExchages(self):
        result = self.ssh.remote_cmd(rabbitmqCmd["LIST_EXCHANGES"])
        stdout = result["stdout"]
        tempList = re.split("\n", stdout.read())[2:-2]
        exchanges = []
        for item in tempList :
            exchanges.append(item.split("\t"))
        return exchanges


    def listQueues(self):
        result = self.ssh.remote_cmd(rabbitmqCmd["LIST_QUEUES"])
        stdout = result["stdout"]
        tempList = re.split("\n", stdout.read())[1:-2]
        queues = []
        for item in tempList :
            queues.append(item.split("\t"))
        return queues


if __name__ == "__main__":
    rabbitmq = RabbitMq()
    print rabbitmq.listQueues()