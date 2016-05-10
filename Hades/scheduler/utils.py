# -*- coding: utf-8 -*-
import requests
import time
from ...Openstack.Conf import OpenstackConf


def get_queue_msg_num(queue_name):
    url = 'http://{host}:{port}/api/queues/{vhost}/{queue}'.format(
            host='localhost',
            port=OpenstackConf.RABBIT_HTTP_PORT,
            vhost='%2F',
            queue=queue_name
    )
    response = requests.get(url, auth=(OpenstackConf.RABBIT_HTTP_USER, OpenstackConf.RABBIT_HTTP_PASSWORD))
    info = response.json()
    if 'messages' in info:
        return response.json()['messages']
    else:
        print 'no message'
        return 0


if __name__ == '__main__':
    while 1:
        print get_queue_msg_num('hades_arbiterPMA_topic.pike')
        time.sleep(0.5)

