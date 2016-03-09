__author__ = 'pike'

from dra.Hades.DB import Base
from oslo_config import cfg

CONF = cfg.CONF

class Manager(Base.Base):
    def __init__(self, host = None, db_driver = None, service_name = 'undefined'):

        self.host = host
        self.backdoor_port = None
        self.service_name = service_name
        self.additional_endpoints = []
        super(Manager, self).__init__(db_driver)

    def init_host(self):
        """Hook to do additional manager initialization when one requests
        the service be started.  This is called before any service record
        is created.

        Child classes should override this method.
        """
        pass

    def cleanup_host(self):
        """Hook to do cleanup work when the service shuts down.

        Child classes should override this method.
        """
        pass

    def pre_start_hook(self):
        """Hook to provide the manager the ability to do additional
        start-up work before any RPC queues/consumers are created. This is
        called after other initialization has succeeded and a service
        record is created.

        Child classes should override this method.
        """
        pass

    def post_start_hook(self):
        """Hook to provide the manager the ability to do additional
        start-up work immediately after a service creates RPC consumers
        and starts 'running'.

        Child classes should override this method.
        """
        pass
