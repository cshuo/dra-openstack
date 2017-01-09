import logging
import oslo_messaging as messaging
from oslo_config import cfg

from dra.Utils import ImportUtils
from dra.Hades.Common import Service as service
from dra.Hades import BaseRpc
from dra.Hades import Rpc

CONF = cfg.CONF
logger = logging.getLogger("DRA.Hades.Service")


class Service(service.Service):

    """Service object for binaries running on hosts.

    A service takes a manager and enables rpc by listening to queues based
    on topic. It also periodically runs tasks on the manager and reports
    it state to the database services table.
    """

    def __init__(self, host, binary, topic, manager, report_interval=None,
                 periodic_enable=None, periodic_fuzzy_delay=None,
                 periodic_interval_max=None, db_allowed=True,
                 *args, **kwargs):
        super(Service, self).__init__()
        self.host = host
        self.binary = binary
        self.topic = topic
        self.manager_class_name = manager

        manager_class = ImportUtils.import_class(self.manager_class_name)
        self.manager = manager_class(host=self.host, *args, **kwargs)
        self.rpcserver = None
        self.report_interval = report_interval
        self.periodic_enable = periodic_enable
        self.periodic_fuzzy_delay = periodic_fuzzy_delay
        self.periodic_interval_max = periodic_interval_max
        self.saved_args, self.saved_kwargs = args, kwargs
        self.backdoor_port = None

    def start(self):

        verstr = '1.0'
        logger.info('Starting %(topic)s node (version %(version)s)' % {'topic': self.topic, 'version': verstr})

        #self.basic_config_check()
        self.manager.init_host()

        self.manager.pre_start_hook()

        if self.backdoor_port is not None:
            self.manager.backdoor_port = self.backdoor_port

        logger.info("Creating RPC server for service %s" % self.topic)

        # exchange is set in CONF.control_exchange
        target = messaging.Target(topic = self.topic, server = self.host)

        endpoints = [
            self.manager,
            BaseRpc.BaseRPCAPI(self.manager.service_name, self.backdoor_port)
        ]
        endpoints.extend(self.manager.additional_endpoints)

        #serializer = objects_base.NovaObjectSerializer()
        serializer = None

        self.rpcserver = Rpc.get_server(target, endpoints, serializer)
        self.rpcserver.start()

        self.manager.post_start_hook()

        logger.info("Join ServiceGroup membership for this service %s" % self.topic)


    @classmethod
    def create(cls, host=None, binary=None, topic=None, manager=None,
               report_interval=None, periodic_enable=None,
               periodic_fuzzy_delay=None, periodic_interval_max=None,
               db_allowed=True):

        """Instantiates class and passes back application object.

        :param host: defaults to CONF.host
        :param binary: defaults to basename of executable
        :param topic: defaults to bin_name - 'nova-' part
        :param manager: defaults to CONF.<topic>_manager
        :param report_interval: defaults to CONF.report_interval
        :param periodic_enable: defaults to CONF.periodic_enable
        :param periodic_fuzzy_delay: defaults to CONF.periodic_fuzzy_delay
        :param periodic_interval_max: if set, the max time to wait between runs

        """
        assert host is not None
        assert binary is not None
        assert manager is not None
        assert topic is not None


        db_allowed = False

        service_obj = cls(host, binary, topic, manager,
                          report_interval=report_interval,
                          periodic_enable=periodic_enable,
                          periodic_fuzzy_delay=periodic_fuzzy_delay,
                          periodic_interval_max=periodic_interval_max,
                          db_allowed=db_allowed)

        return service_obj

    def kill(self):
        self.stop()

    def stop(self):
        try:
            self.rpcserver.stop()
            self.rpcserver.wait()
        except Exception:
            pass

        try:
            self.manager.cleanup_host()
        except  Exception:
            logger.error('Service error occurred during cleanup host')
            pass

        super(Service, self).stop()


# NOTE(vish): the global launcher is to maintain the existing
#             functionality of calling service.serve +
#             service.wait
_launcher = None

def serve(server, workers=None):
    # print 'serve service\n'
    global _launcher
    if _launcher:
        raise RuntimeError('serve() can only be called once')

    _launcher = service.launch(server, workers=workers)


def wait():
    # print 'service wait\n'
    _launcher.wait()


if __name__ == "__main__":
    print "nova-compute".rpartition('nova-')
