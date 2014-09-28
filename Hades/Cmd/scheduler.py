__author__ = 'pike'


"""Starter script for customized scheduler."""
from pkg_resources import iter_entry_points
from Hades import Service
from Hades import Config
from oslo.messaging import TransportURL
from oslo.messaging import InvalidTransportURL
from oslo.config import cfg

def main():

    Config.parse_args()

    server = Service.Service.create(binary = 'hades-scheduler',
                                    topic = 'scheduler',
                                    manager = 'Hades.Scheduler.Manager.SchedulerManager')
    Service.serve(server)
    Service.wait()

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    main()
#    conf = cfg.CONF
#    TRANSPORT_ALIASES = {
#    'nova.openstack.common.rpc.impl_kombu': 'rabbit',
#    'nova.openstack.common.rpc.impl_qpid': 'qpid',
#    'nova.openstack.common.rpc.impl_zmq': 'zmq',
#    'nova.rpc.impl_kombu': 'rabbit',
#    'nova.rpc.impl_qpid': 'qpid',
#    'nova.rpc.impl_zmq': 'zmq',
#}
#    url = 'rabbit://rabbitmq:RABBITMQ_PASS@114.212.189.133:5672/hades'
#    if not isinstance(url, TransportURL):
#        url = url or conf.transport_url
#        parsed = TransportURL.parse(conf, url, aliases=TRANSPORT_ALIASES)
#        if not parsed.transport:
#            raise InvalidTransportURL(url, 'No scheme specified in "%s"' % url)
#        url = parsed
#        print url
