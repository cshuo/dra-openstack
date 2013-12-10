__author__ = 'pike'

from Utils.Ssh_tool import *
from Openstack import HOST,USERNAME,PASSWORD


class Instance:


    # environment variables
    param="--os-username admin"+" "+\
              "--os-tenant-name admin"+" "+\
              "--os-auth-url http://controller:35357/v2.0"+" "+\
              "--os-password ADMIN_PASS"

    def __init__(self):
        self.id="690761eb-8c27-4112-bc42-e25d732029ae"


    def liveMigration(self,host):

        # connect to host
        ssh=Ssh_tool(HOST,22,USERNAME,PASSWORD)

        #execute shell command to migrate the instance
        ssh.remote_cmd("nova"+" "+Instance.param+" "+"live-migration"+" "+self.id+" "+host)

    def getID(self):
        return self.id

if __name__=="__main__":
    instance=Instance()
    instance.liveMigration("compute")