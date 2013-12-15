__author__ = 'pike'

import threading
import time
import InstanceMonitor
import socket
import pickle

class MonitorThread(threading.Thread):

    def __init__(self,port):
        threading.Thread.__init__(self)

        # connect to the hypervisor
        self.monitor=InstanceMonitor.InstanceMonitor(InstanceMonitor.QEMU)

        # start listening
        self.s=socket.socket()
        self.host="127.0.0.1"

        print "hostname: %s" % self.host
        self.s.bind((self.host,port))
        self.s.listen(1)
        (self.clientsocket,addr)=self.s.accept()
        print "client connected\n"

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

                #calculate the cpu utility
                utility=(newcputime-oldcputime)/(currenttime-pretime)
                self.clientsocket.send(pickle.dumps({"f0591af7-2f8a-4c15-95ee-ec6980170d51":utility}))
                print "%f\n" % utility
            count+=1
            pretime=currenttime
            oldcputime=newcputime
            time.sleep(5)

        print "thread exit"


if __name__=="__main__":
    threadtest=MonitorThread(2000)
    threadtest.start()