__author__ = 'pike'

import paramiko

class Ssh_tool:

    def __init__(self,hostname,port,username,password):
        self.sshclient=paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(hostname,port,username,password)


    def remote_cmd(self,command):
        stdin,stdout,stderr=self.sshclient.exec_command(command)
        print "stdout: "+stdout.read()+"\n"
        print "stderr: "+stderr.read()+"\n"


if __name__=="__main__":
    ssh=Ssh_tool("114.212.189.132",22,"root","cs")
    ssh.remote_cmd("df")
