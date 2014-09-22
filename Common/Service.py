__author__ = 'pike'


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

        # NOTE(russellb) We want to make sure to create the servicegroup API
        # instance early, before creating other things such as the manager,
        # that will also create a servicegroup API instance.  Internally, the
        # servicegroup only allocates a single instance of the driver API and
        # we want to make sure that our value of db_allowed is there when it
        # gets created.  For that to happen, this has to be the first instance
        # of the servicegroup API.
        #self.servicegroup_api = servicegroup.API(db_allowed=db_allowed)

        #manager_class = importutils.import_class(self.manager_class_name)
        #self.manager = manager_class(host=self.host, *args, **kwargs)
        self.rpcserver = None
        self.report_interval = report_interval
        self.periodic_enable = periodic_enable
        self.periodic_fuzzy_delay = periodic_fuzzy_delay
        self.periodic_interval_max = periodic_interval_max
        self.saved_args, self.saved_kwargs = args, kwargs
        self.backdoor_port = None
        #self.conductor_api = conductor.API(use_local=db_allowed)
        #self.conductor_api.wait_until_ready(context.get_admin_context())


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
        #if not host:
        #    host = CONF.host
        #if not binary:
        #    binary = os.path.basename(sys.argv[0])
        #if not topic:
        #    topic = binary.rpartition('nova-')[2]
        #if not manager:
        #    manager_cls = ('%s_manager' %
        #                   binary.rpartition('nova-')[2])
        #    manager = CONF.get(manager_cls, None)
        #if report_interval is None:
        #    report_interval = CONF.report_interval
        #if periodic_enable is None:
        #    periodic_enable = CONF.periodic_enable
        #if periodic_fuzzy_delay is None:
        #    periodic_fuzzy_delay = CONF.periodic_fuzzy_delay
        #
        #debugger.init()

        db_allowed = False

        service_obj = cls(host, binary, topic, manager,
                          report_interval=report_interval,
                          periodic_enable=periodic_enable,
                          periodic_fuzzy_delay=periodic_fuzzy_delay,
                          periodic_interval_max=periodic_interval_max,
                          db_allowed=db_allowed)

        return service_obj




def serve(server, workers=None):
    global _launcher
    if _launcher:
        raise RuntimeError('serve() can only be called once')

    _launcher = service.launch(server, workers=workers)


def wait():
    _launcher.wait()