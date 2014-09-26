__author__ = 'pike'

from oslo import  messaging

TRANSPORT = None

ALLOWED_EXMODS = []
EXTRA_EXMODS = []

# NOTE(markmc): The nova.openstack.common.rpc entries are for backwards compat
# with Havana rpc_backend configuration values. The nova.rpc entries are for
# compat with Essex values.
TRANSPORT_ALIASES = {
    'nova.openstack.common.rpc.impl_kombu': 'rabbit',
    'nova.openstack.common.rpc.impl_qpid': 'qpid',
    'nova.openstack.common.rpc.impl_zmq': 'zmq',
    'nova.rpc.impl_kombu': 'rabbit',
    'nova.rpc.impl_qpid': 'qpid',
    'nova.rpc.impl_zmq': 'zmq',
}

# used in Hades/Cmd/scheduler
def init(conf):
    global TRANSPORT
    exmods = get_allowed_exmods()
    TRANSPORT = messaging.get_transport(conf,
                                        allowed_remote_exmods = exmods,
                                        aliases = TRANSPORT_ALIASES)
    #serializer

def cleanup():
    global  TRANSPORT
    assert  TRANSPORT is not None
    TRANSPORT.cleanup()
    TRANSPORT = None


def get_allowed_exmods():
    return ALLOWED_EXMODS + EXTRA_EXMODS

#class RequestContextSerializer(messaging.Serializer):
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

def get_client(target, version_cap = None, serializer = None):
    assert  TRANSPORT is not None
    #serializer = RequestContextSerializer(serializer)
    return messaging.RPCClient(TRANSPORT,
                               target,
                               version_cap = version_cap,
                               serializer = serializer)

def get_server(target, endpoints, serializer = None):
    assert TRANSPORT is not None
    #serializer = RequestContextSerializer(serializer)
    return messaging.get_rpc_server(TRANSPORT,
                                    target,
                                    endpoints,
                                    executor = 'eventlet',
                                    serializer = serializer)

def set_defaults(control_exchange):
    messaging.set_transport_defaults(control_exchange)