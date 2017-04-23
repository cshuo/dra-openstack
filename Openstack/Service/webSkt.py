# -*- coding: utf-8 -*-

import threading
import multiprocessing
import sys, time
import tornado.web
import tornado.ioloop
import tornado.websocket 

class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        print "new connection..."
        SocketHandler.clients.append(self)

    @classmethod
    def write_to_clients(cls, vm_id, host):
        # print "Writing to all clients..."
        for client in cls.clients:
            if not client.ws_connection.stream.socket:
                print "Web socket does not exist anymore!!!"
                cls.clients.remove(client)
            else:
                client.write_message({'vm_id': vm_id, 'host': host})

class TornadoService():
    def __init__(self):
        self.p = None

    def run(self):
        app = tornado.web.Application([
            ('/soc', SocketHandler)
        ])
        app.listen(8070)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except (KeyboardInterrupt, SystemExit):
            self.stop_tornado()

    def start(self):
        self.p = multiprocessing.Process(target=self.run)
        self.p.start()

    def stop_tornado(self):
        iolp = tornado.ioloop.IOLoop.instance()
        iolp.add_callback(iolp.stop)


if __name__ == '__main__':
    server_tornado = ServerThread()
    server_tornado.start()
    i = 0
    while i < 3:
        if i % 2 ==0 :
            hosts = "compute0"
        else:
            hosts = "compute1"
        SocketHandler.write_to_clients('4bd19233-e7b8-4fe8-9ab6-a0cc911bb517', hosts);
        i += 1
        time.sleep(2)
    ServerThread.stop_tornado()
