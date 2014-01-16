__author__ = 'pike'

import commands

from Utils.FileUtil import *

class HostMonitor:

    def __init__(self):
        self.memhandler=MemFileHandler("../meminfo")


    # return (memfree,memtotal)
    def getMemInfo(self):
        return (self.memhandler.getMemFree(),self.memhandler.getMemTotal())

    #return (load in 1 min,load in 5 min,load in 15 min)
    def getCpuLoad(self):
        (status,output)=commands.getstatusoutput("uptime")
        #ubuntu
        #list=output.split("load average:")[-1].strip().split(" ")

        #macos
        list=output.split("load averages:")[-1].strip().split(" ")
        print list


if __name__=="__main__":
    hmonitor=HostMonitor()
    hmonitor.getMemInfo()
    hmonitor.getCpuLoad()

