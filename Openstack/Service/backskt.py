# -*- coding: utf-8 -*-

import threading
import multiprocessing
import sys, time
import tornado.web
import tornado.ioloop
import tornado.websocket

from ...Utils.logs import draLogger

logger = draLogger("DRA.WebSocket")


class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        logger.info("new websocket client connection...")
        SocketHandler.clients.append(self)

    @classmethod
    def write_to_clients(cls, vm_id, host):
        for client in cls.clients:
            if not client.ws_connection.stream.socket:
                logger.warn("Web socket does not exist anymore!!!")
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
    server_tornado = TornadoService()
    server_tornado.start()
    i = 0
    while i < 10:
        if i % 2 == 0:
            hosts = "kolla1"
        else:
            hosts = "kolla2"
        print i, ": send a msg"
        SocketHandler.write_to_clients('6b12712a-a7b0-401e-86d3-370e0a9e9a5f', hosts);
        i += 1
        time.sleep(2)
    server_tornado.stop_tornado()
