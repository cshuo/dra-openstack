# -*- coding: utf-8 -*-
import requests
from ...Openstack.Conf import OpenstackConf


def get_queue_msg_num(queue_name):
    url = 'http://{host}:{port}/api/queues/{vhost}/{queue}'.format(
            host='localhost',
            port=OpenstackConf.RABBIT_HTTP_PORT,
            vhost='%2F',
            queue=queue_name
    )
    response = requests.get(url, auth=(OpenstackConf.RABBIT_HTTP_USER, OpenstackConf.RABBIT_HTTP_PASSWORD))
    return response.json()['messages']


if __name__ == '__main__':
    print get_queue_msg_num('hades_scheduler_topic.pike')

