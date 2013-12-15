__author__ = 'pike'

import threading
import socket
import pickle

''' get instances's cpu utility data from the monitor'''


class InstanceDataReceiver(threading.Thread):


    # get connect to the monitor server
    def __init__(self,(host,port)):
        threading.Thread.__init__(self)
        self.s=socket.socket()
        self.s.connect((host,port))

        print "connected to %s" % host


    def run(self):
        while (True):
            print pickle.loads(self.s.recv(1024))


if __name__ == "__main__":
    receivertest=InstanceDataReceiver(("114.212.189.133",2000))
    receivertest.start()

