__author__ = 'pike'

import oslo_messaging as messaging
from oslo_config import cfg

CONF = cfg.CONF

TRANSPORT = None

ALLOWED_EXMODS = []
EXTRA_EXMODS = []


# used in Hades/Cmd/scheduler
def init(conf):
    global TRANSPORT
    exmods = get_allowed_exmods()
    # TRANSPORT = messaging.get_transport(conf)
    TRANSPORT = messaging.get_transport(conf,
                                        url=CONF.hades_rabbit_url,
                                        allowed_remote_exmods=exmods,
                                        aliases={})


def cleanup():
    global TRANSPORT
    assert TRANSPORT is not None
    TRANSPORT.cleanup()
    TRANSPORT = None


def get_allowed_exmods():
    return ALLOWED_EXMODS + EXTRA_EXMODS


# class RequestContextSerializer(messaging.Serializer):
#
#    def __init__(self, base):
#        self._base = base
#
#    def serialize_entity(self, context, entity):
#        if not self._base:
#            return entity
#        return self._base.serialize_entity(context, entity)
#
#    def deserialize_entity(self, context, entity):
#        if not self._base:
#            return entity
#        return self._base.deserialize_entity(context, entity)
#
#    def serialize_context(self, context):
#        return context.to_dict()
#
#    def deserialize_context(self, context):
#        return nova.context.RequestContext.from_dict(context)

def get_client(target, version_cap=None, serializer=None):
    assert TRANSPORT is not None
    return messaging.RPCClient(TRANSPORT, target)
    """
    return messaging.RPCClient(TRANSPORT,
                               target,
                               version_cap = version_cap,
                               serializer = serializer)
    """


def get_server(target, endpoints, serializer=None):
    assert TRANSPORT is not None
    # serializer = RequestContextSerializer(serializer)
    return messaging.get_rpc_server(TRANSPORT,
                                    target,
                                    endpoints,
                                    executor='blocking',
                                    access_policy=messaging.DefaultRPCAccessPolicy,
                                    serializer=serializer)


def set_defaults(control_exchange):
    CONF.control_exchange = control_exchange
