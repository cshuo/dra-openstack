# -*- coding: utf-8 -*-

import threading
import sys, time
import tornado.web
import tornado.ioloop
import tornado.websocket


class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        print "new connection..., num: ", len(SocketHandler.clients)
        SocketHandler.clients.append(self)

    def on_message(self, message):
        pass

    @classmethod
    def write_to_clients(cls, vm_id, host):
        # print "Writing to all clients..."
        for client in cls.clients:
            if not client.ws_connection or not client.ws_connection.stream.socket:
                cls.clients.remove(client)
            else:
                client.write_message({'vm_id': vm_id, 'host': host})


class ServerThread(threading.Thread):
    def run(self):
        app = tornado.web.Application([
            ('/soc', SocketHandler)
        ])
        app.listen(8070)
        tornado.ioloop.IOLoop.instance().start()

    @classmethod
    def stop_tornado(cls):
        print "stop tornado..."
        iolp = tornado.ioloop.IOLoop.instance()
        iolp.add_callback(iolp.stop)


def stop_tornado():
    iolp = tornado.ioloop.IOLoop.instance()
    iolp.add_callback(iolp.stop)
    print 'stopping tornado...'


if __name__ == '__main__':
    server_tornado = ServerThread()
    server_tornado.start()
    i = 0
    while i < 10:
        if i % 2 ==0 :
            hosts = "kolla3"
        else:
            hosts = "kolla2"
        print i, ": send a msg.."
        SocketHandler.write_to_clients('b7e9dd7c-4c5b-4614-8b04-4caaaf4c9792', hosts);
        i += 1
        time.sleep(2)
    ServerThread.stop_tornado()
