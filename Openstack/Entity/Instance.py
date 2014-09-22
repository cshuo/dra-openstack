__author__ = 'pike'

from Utils.SshUtil import *
from Openstack import HOST,USERNAME,PASSWORD


class Instance:

    def __init__(self, info):
        self.info = info

    def getId(self):
        return self.info['id']

    def getName(self):
        return self.info['name']



if __name__=="__main__":
    instance = Instance()
