__author__ = 'pike'
from MemFileHandler import *

class HostMonitor:

    def __init__(self):
        self.memhandler=MemFileHandler("meminfo")
        #self.statfile=open("stat")

    def display(self):
        print self.memhandler.attributes
        print self.memhandler.getMemFree()
        print self.memhandler.getMemTotal()

hmonitor=HostMonitor()
hmonitor.display()

