__author__ = 'pike'

import oslo_messaging as messaging

from dra.Hades import Config
from dra.Hades import Rpc

"""
    client side of rpc api

"""


class BaseAPI(object):

    def __init__(self, topic, exchange):

        Config.config_init(exchange)
        target = messaging.Target(topic=topic)
        version_cap = None
        serializer = None
        self.client = self.get_client(target, version_cap, serializer)

    def get_client(self, target, version_cap, serializer):
        return Rpc.get_client(target,
                              version_cap=version_cap,
                              serializer=serializer)
