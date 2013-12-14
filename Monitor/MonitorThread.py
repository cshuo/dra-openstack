__author__ = 'pike'

import threading
import time
import InstanceMonitor

class MonitorThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.monitor=InstanceMonitor.InstanceMonitor(InstanceMonitor.QEMU)


    def run(self):
        count=0
        pretime=0
        currenttime=0
        oldcputime=0
        newcputime=0
        while(count<10):
            currenttime=time.time()
            newcputime=self.monitor.getInfo("f0591af7-2f8a-4c15-95ee-ec6980170d51")[-1]/1e9
            if(count>0):
                utility=(newcputime-oldcputime)/(currenttime-pretime)
                print "%f\n" % utility
            count+=1
            pretime=currenttime
            oldcputime=newcputime
            time.sleep(5)

        print "thread exit"


if __name__=="__main__":
    threadtest=MonitorThread()
    threadtest.start()