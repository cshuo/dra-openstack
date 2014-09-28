__author__ = 'pike'

from oslo import  messaging

TRANSPORT = None

ALLOWED_EXMODS = []
EXTRA_EXMODS = []

# NOTE(markmc): The nova.openstack.common.rpc entries are for backwards compat
# with Havana rpc_backend configuration values. The nova.rpc entries are for
# compat with Essex values.
TRANSPORT_DRIVERS = {
    'rabbit' : 'oslo.messaging._drivers.impl_rabbit',
    'qpid' : 'oslo.messaging._drivers.impl_qpid:QpidDriver',
    'zmq' : 'oslo.messaging._drivers.impl_zmq:ZmqDriver',

    ## To avoid confusion
    #'kombu = oslo.messaging._drivers.impl_rabbit:RabbitDriver',
    #
    ## For backwards compat
    #'openstack.common.rpc.impl_kombu ='
    #' oslo.messaging._drivers.impl_rabbit:RabbitDriver',
    #'openstack.common.rpc.impl_qpid ='
    #' oslo.messaging._drivers.impl_qpid:QpidDriver',
    #'openstack.common.rpc.impl_zmq ='
    #' oslo.messaging._drivers.impl_zmq:ZmqDriver',
}

# used in Hades/Cmd/scheduler
def init(conf):
    global TRANSPORT
    exmods = get_allowed_exmods()
    #conf.transport_url = 'rabbit://rabbitmq:RABBITMQ_PASS@114.212.189.133:5672/hades'
    TRANSPORT = messaging.get_transport(conf,
                                        url = 'rabbit://rabbitmq:RABBITMQ_PASS@114.212.189.133:5672/',
                                        allowed_remote_exmods = exmods,
                                        aliases = {})
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