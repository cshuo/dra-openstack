__author__ = 'pike'

import paramiko
from Openstack.Conf import OpenstackConf

class Ssh_tool:

    def __init__(self, hostname, port, username = OpenstackConf.HOST_USERNAME, password = OpenstackConf.HOST_PASSWORD):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(hostname, port, username, password)


    def remote_cmd(self, command):
        stdin, stdout, stderr = self.sshclient.exec_command(command)

        #print "remote command: " + command + "\n"
        #print "stdout: " + stdout.read() + "\n"
        #print "stderr: " + stderr.read() + "\n"

        return {"stdin" : stdin,
                "stdout" : stdout,
                "stderr" : stderr}

    def close(self):
        self.sshclient.close()

if __name__=="__main__":
    ssh = Ssh_tool("114.212.189.132",22,"root","cs")
    ssh.remote_cmd("df")
    ssh.close()
