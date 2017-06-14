__author__ = 'pike'

import paramiko

from dra.Openstack.Conf import OpenstackConf

class Ssh_tool:

    def __init__(self, hostname, port, username = OpenstackConf.HOST_USERNAME, password = OpenstackConf.HOST_PASSWORD):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(hostname, port, username, password)


    def remote_cmd(self, command):
        stdin, stdout, stderr = self.sshclient.exec_command(command)
        return {"stdin" : stdin,
                "stdout" : stdout,
                "stderr" : stderr}

    def close(self):
        self.sshclient.close()

if __name__=="__main__":
    pass
