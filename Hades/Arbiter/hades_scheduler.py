__author__ = 'cshuo'

import random
import oslo_messaging as messaging
from oslo_config import cfg
from nova import exception
from oslo_log import log as logging
from nova.scheduler import driver


manager_opts = [
    cfg.StrOpt('hades_arbiter_topic',
               default = 'hades_arbiter_test',
               help = 'topic of test hades scheduler arbiter')
]

CONF = cfg.CONF
CONF.register_opts(manager_opts)


class HubScheduler(driver.Scheduler):
    """
    Implements Scheduler which queries the arbiter.
    """

    def __init__(self, *args, **kwargs):
        super(HubScheduler, self).__init__(*args, **kwargs)
	#Config.config_init()
	#self.scheduler_api = RpcApi.SchedulerAPI()



    def _schedule(self, context, request_spec, filter_properties):
        """Picks a host that is up at random."""

	messaging.set_transport_defaults('hades')

	TRANSPORT = messaging.get_transport(CONF,
                                        url = 'rabbit://openstack:cshuo@20.0.1.11:5672/',
                                        allowed_remote_exmods = [],
                                        aliases = {})
	target = messaging.Target(topic=CONF.hades_arbiter_topic)
	version_cap = None
	serializer = None
	client = messaging.RPCClient(TRANSPORT,
                               target,
                               version_cap = version_cap,
                               serializer = serializer)

	cctxt = client.prepare(server = 'pike')
	host = cctxt.call({}, 'testArbiter', arg='')
        return host


    def select_destinations(self, context, request_spec, filter_properties):
        """Selects random destinations."""
        num_instances = request_spec['num_instances']
        # NOTE(timello): Returns a list of dicts with 'host', 'nodename' and
        # 'limits' as keys for compatibility with filter_scheduler.
        # NOTE here never raise exception

        dests = []
        for i in range(num_instances):
            host = self._schedule(context, request_spec, filter_properties)
            host_state = dict(host=host, nodename=None, limits=None)
            dests.append(host_state)

        if len(dests) < num_instances:
            raise exception.NoValidHost(reason='')
        return dests
