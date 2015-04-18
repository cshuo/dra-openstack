__author__ = 'pike'

import tornado.web
import tornado.ioloop
import tornado.websocket

import threading
import time

import random

from Utils.SshUtil import Ssh_tool

class Index(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
<head>
<script>
var ws = new WebSocket('ws://localhost:9008/soc');
ws.onmessage = function(event) {
    document.getElementById('message').innerHTML = event.data;
};
</script>
</head>
<body>
<p id='message'></p>
        ''')


class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        self.write_message('Welcome to WebSocket')

        thread = DataPusher(self)
        thread.start()


class DataPusher(threading.Thread):

    def __init__(self, socketHandler):
        super(DataPusher, self).__init__()
        self.socketHandler = socketHandler
        self.sshTool = Ssh_tool("114.212.189.134", 22, "root", "njuics08")

        self.count = 0

    def pushGmetric(self, name, value, host):
        cmd = "gmetric --name %s  --value %d --type uint32 --spoof %s" % (name, value, host)
        print cmd
        self.sshTool.remote_cmd(cmd)

    def pushEvent(self, type, info):
        self.socketHandler.write_message()

    def run(self):
        while True:
            #self.socketHandler.write_message("hello" + str(self.count))
            self.pushGmetric("bandwidth", 1 + random.randint(0, 50), "10.0.0.1:host1")
            self.pushGmetric("bandwidth", 100 + random.randint(-50, 50), "10.0.0.2:host2")
            self.pushGmetric("bandwidth", 200 + random.randint(-50, 50), "10.0.0.3:host3")
            self.pushGmetric("bandwidth", 300 + random.randint(-100, 50), "10.0.0.4:host4")

            self.count += 1
            time.sleep(3)




if __name__ == '__main__':
    app = tornado.web.Application([
        ('/', Index),
        ('/soc', SocketHandler)
    ])

    app.listen(9008)
    tornado.ioloop.IOLoop.instance().start()

    {'value' : 'eventvalue', 'type' : 'event'}
    {'value' : '22', 'type' : 'action'}

    {'value' : {'host1' : [{'type' : 'matlab', 'name': 'instance1'}, {}], }, 'type' : 'hosts'}
