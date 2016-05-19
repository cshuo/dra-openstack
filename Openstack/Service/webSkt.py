# -*- coding: utf-8 -*-

import threading
import sys
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
        print "Writing to all clients..."
        for client in cls.clients:
            if not client.ws_connection.stream.socket:
                print "Web socket does not exist anymore!!!"
                cls.clients.remove(client)
            else:
                client.write_message({'vm_id': vm_id, 'host': host})


class ServerThread(threading.Thread):
    def run(self):
        print "start server.."
        app = tornado.web.Application([
            ('/soc', SocketHandler)
        ])
        app.listen(8070)
        tornado.ioloop.IOLoop.instance().start()


def stop_tornado():
    iolp = tornado.ioloop.IOLoop.instance()
    iolp.add_callback(iolp.stop)
    print 'stopping tornado...'

# server_tornado = ServerThread()
# server_tornado.start()
