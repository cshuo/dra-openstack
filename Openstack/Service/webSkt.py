# -*- coding: utf-8 -*-

import threading
import sys, time
import tornado.web
import tornado.ioloop
import tornado.websocket


class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def check_origin(self, origin):
        return True

    def open(self):
        print "new connection..., num: ", len(SocketHandler.clients)
        SocketHandler.clients.add(self)

    def on_close(self):
        SocketHandler.clients.remove(self)

    def on_message(self, message):
        pass

    @classmethod
    def write_to_clients(cls, mtype, **kwargs):
        # print "Writing to all clients..."
        msg = dict()
        msg['type'] = mtype
        if mtype == 'update':
            msg['vm_id'] = kwargs['vm_id']
            msg['host'] = kwargs['host']
        elif mtype == 'status':
            msg['host'] = kwargs['host']
            msg['status'] = kwargs['status']
        elif mtype == 'message':
            msg['host'] = kwargs['host']
            msg['content'] = kwargs['content']
        else:
            msg['content'] = kwargs['content']

        for client in SocketHandler.clients:
            client.write_message(msg)


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
    instance_id = 'af0e525c-fb95-414f-ae2e-13f484b6b972'
    host = 'kolla1'
    while i < 20:
        if i % 2 == 0:
            hosts = "kolla2"
        else:
            hosts = "kolla3"
        print i, ": send a msg.."
        # SocketHandler.write_to_clients('update', vm_id='af0e525c-fb95-414f-ae2e-13f484b6b972', host=hosts);
        SocketHandler.write_to_clients('scheduler', content='虚拟机: %s 迁移到主机: %s' % (instance_id, host))

        i += 1
        time.sleep(3)
    ServerThread.stop_tornado()
