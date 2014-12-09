__author__ = 'pike'

from Utils.SshUtil import *
from Openstack import HOST,USERNAME,PASSWORD


class Instance:

    def __init__(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getName(self):
        return self.name



if __name__=="__main__":
    instance = Instance()
