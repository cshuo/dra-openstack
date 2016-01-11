__author__ = 'pike'

from setuptools import setup

driverGroup = 'oslo_messaging.drivers'

transportDrivers = [
    'rabbit = oslo_messaging._drivers.impl_rabbit:RabbitDriver',
    'qpid = oslo_messaging._drivers.impl_qpid:QpidDriver',
    'zmq = oslo_messaging._drivers.impl_zmq:ZmqDriver',

    # To avoid confusion
    'kombu = oslo_messaging._drivers.impl_rabbit:RabbitDriver',

    # For backwards compat
    'openstack.common.rpc.impl_kombu ='
    ' oslo_messaging._drivers.impl_rabbit:RabbitDriver',
    'openstack.common.rpc.impl_qpid ='
    ' oslo_messaging._drivers.impl_qpid:QpidDriver',
    'openstack.common.rpc.impl_zmq ='
    ' oslo_messaging._drivers.impl_zmq:ZmqDriver',
]

executorGroup = 'oslo_messaging.executors'

executors = [
    'blocking = oslo_messaging._executors.impl_blocking:BlockingExecutor',
    'eventlet = oslo_messaging._executors.impl_eventlet:EventletExecutor'

]


entry_points = {driverGroup : transportDrivers,
                executorGroup : executors}

setup(
    name = "oslo_driver",
    entry_points = entry_points
)
