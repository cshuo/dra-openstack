__author__ = 'pike'

from setuptools import setup

NAMESPACE = 'oslo.messaging.drivers'

TRANSPORT_DRIVERS = [
    'rabbit = oslo.messaging._drivers.impl_rabbit:RabbitDriver',
    'qpid = oslo.messaging._drivers.impl_qpid:QpidDriver',
    'zmq = oslo.messaging._drivers.impl_zmq:ZmqDriver',

    # To avoid confusion
    'kombu = oslo.messaging._drivers.impl_rabbit:RabbitDriver',

    # For backwards compat
    'openstack.common.rpc.impl_kombu ='
    ' oslo.messaging._drivers.impl_rabbit:RabbitDriver',
    'openstack.common.rpc.impl_qpid ='
    ' oslo.messaging._drivers.impl_qpid:QpidDriver',
    'openstack.common.rpc.impl_zmq ='
    ' oslo.messaging._drivers.impl_zmq:ZmqDriver',
]

entry_points = {NAMESPACE : TRANSPORT_DRIVERS}

setup(
    name = "oslo_driver",
    entry_points = entry_points
)

#[entry_points]
#console_scripts =
#    oslo-messaging-zmq-receiver = oslo.messaging._cmd.zmq_receiver:main
#
#oslo.messaging.drivers =
#    rabbit = oslo.messaging._drivers.impl_rabbit:RabbitDriver
#    qpid = oslo.messaging._drivers.impl_qpid:QpidDriver
#    zmq = oslo.messaging._drivers.impl_zmq:ZmqDriver
#    amqp = oslo.messaging._drivers.protocols.amqp:ProtonDriver
#
#    # To avoid confusion
#    kombu = oslo.messaging._drivers.impl_rabbit:RabbitDriver
#
#    # This is just for internal testing
#    fake = oslo.messaging._drivers.impl_fake:FakeDriver
#
#oslo.messaging.executors =
#    blocking = oslo.messaging._executors.impl_blocking:BlockingExecutor
#    eventlet = oslo.messaging._executors.impl_eventlet:EventletExecutor
#
#oslo.messaging.notify.drivers =
#    messagingv2 = oslo.messaging.notify._impl_messaging:MessagingV2Driver
#    messaging = oslo.messaging.notify._impl_messaging:MessagingDriver
#    log = oslo.messaging.notify._impl_log:LogDriver
#    test = oslo.messaging.notify._impl_test:TestDriver
#    noop = oslo.messaging.notify._impl_noop:NoOpDriver
#    routing = oslo.messaging.notify._impl_routing:RoutingDriver
#
#oslo.config.opts =
#    oslo.messaging = oslo.messaging.opts:list_opts