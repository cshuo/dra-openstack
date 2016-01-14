__author__ = 'pike'

import oslo_messaging as messaging

_NAMESPACE = 'baseapi'

class BaseRPCAPI(object):

    """
    Server side of the base RPC API
    """

    target = messaging.Target(namespace = _NAMESPACE, version = '1.1')

    def __init__(self, service_name, backdoor_port):
        self.service_name = service_name
        self.backdoor_port = backdoor_port

    def ping(self, context, arg):
        pass

    def get_backdoor_port(self, context):
        return self.backdoor_port