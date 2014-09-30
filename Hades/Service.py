__author__ = 'pike'


from Utils import ImportUtils
from Hades.Common import Service as service
from oslo import messaging
from Hades import BaseRpc
from Hades import Rpc
from oslo.config import cfg

CONF = cfg.CONF


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

        #self.servicegroup_api = servicegroup.API(db_allowed=db_allowed)

        manager_class = ImportUtils.import_class(self.manager_class_name)
        self.manager = manager_class(host=self.host, *args, **kwargs)
        self.rpcserver = None
        self.report_interval = report_interval
        self.periodic_enable = periodic_enable
        self.periodic_fuzzy_delay = periodic_fuzzy_delay
        self.periodic_interval_max = periodic_interval_max
        self.saved_args, self.saved_kwargs = args, kwargs
        self.backdoor_port = None
        #self.conductor_api = conductor.API(use_local=db_allowed)
        #self.conductor_api.wait_until_ready(context.get_admin_context())

    def start(self):
        #verstr = version.version_string_with_package()
        verstr = '1.0'
        print 'Starting %(topic)s node (version %(version)s)' % {'topic': self.topic, 'version': verstr}

        #self.basic_config_check()
        self.manager.init_host()

        #self.model_disconnected = False
        #ctxt = context.get_admin_context()
        #try:
        #    self.service_ref = self.conductor_api.service_get_by_args(ctxt,
        #            self.host, self.binary)
        #    self.service_id = self.service_ref['id']
        #except exception.NotFound:
        #    try:
        #        self.service_ref = self._create_service_ref(ctxt)
        #    except (exception.ServiceTopicExists,
        #            exception.ServiceBinaryExists):
        #        # NOTE(danms): If we race to create a record with a sibling
        #        # worker, don't fail here.
        #        self.service_ref = self.conductor_api.service_get_by_args(ctxt,
        #            self.host, self.binary)

        self.manager.pre_start_hook()

        if self.backdoor_port is not None:
            self.manager.backdoor_port = self.backdoor_port

        print "Creating RPC server for service %s" % self.topic

        target = messaging.Target(topic = self.topic, server = self.host, exchange = CONF.exchange)

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

        print "Join ServiceGroup membership for this service %s" % self.topic
        # Add service to the ServiceGroup membership group.
        #self.servicegroup_api.join(self.host, self.topic, self)
        #
        #if self.periodic_enable:
        #    if self.periodic_fuzzy_delay:
        #        initial_delay = random.randint(0, self.periodic_fuzzy_delay)
        #    else:
        #        initial_delay = None
        #
        #    self.tg.add_dynamic_timer(self.periodic_tasks,
        #                             initial_delay=initial_delay,
        #                             periodic_interval_max=
        #                                self.periodic_interval_max)


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
            print 'Service error occurred during cleanup host'
            pass

        super(Service, self).stop()


# NOTE(vish): the global launcher is to maintain the existing
#             functionality of calling service.serve +
#             service.wait
_launcher = None

def serve(server, workers=None):
    print 'serve service\n'
    global _launcher
    if _launcher:
        raise RuntimeError('serve() can only be called once')

    _launcher = service.launch(server, workers=workers)


def wait():
    print 'service wait\n'
    _launcher.wait()


if __name__ == "__main__":
    print "nova-compute".rpartition('nova-')
