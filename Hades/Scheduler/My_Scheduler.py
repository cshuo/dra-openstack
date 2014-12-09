__author__ = 'pike'

import random
from oslo import messaging
from oslo.config import cfg

from nova.compute import rpcapi as compute_rpcapi
from nova import exception
from nova.openstack.common import log as logging
from nova.openstack.common.gettextutils import _
from nova.scheduler import driver



CONF = cfg.ConfigOpts()
#CONF.import_opt('compute_topic', 'nova.compute.rpcapi')
#LOG = logging.getLogger(__name__)


class HubScheduler(driver.Scheduler):
    """
    Implements Scheduler which queries the arbiter.
    """

    def __init__(self, *args, **kwargs):
        super(HubScheduler, self).__init__(*args, **kwargs)
        self.compute_rpcapi = compute_rpcapi.ComputeAPI()
	#Config.config_init()
	#self.scheduler_api = RpcApi.SchedulerAPI()



    def _schedule(self, context, topic, request_spec, filter_properties):
        """Picks a host that is up at random."""

        #elevated = context.elevated()
        #hosts = self.hosts_up(elevated, topic)

        #if not hosts:
        #    msg = _("Is the appropriate service running?")
        #    raise exception.NoValidHost(reason=msg)
        #host =  self.scheduler_api.testSchedule({}, 'localhost', None)

	messaging.set_transport_defaults('hades')


	TRANSPORT = messaging.get_transport(CONF,
                                        url = 'rabbit://guest:RABBIT_PASS@114.212.189.134:5672/',
                                        allowed_remote_exmods = [],
                                        aliases = {})
	target = messaging.Target(topic = 'hades_scheduler_topic')
	version_cap = None
	serializer = None
	client = messaging.RPCClient(TRANSPORT,
                               target,
                               version_cap = version_cap,
                               serializer = serializer)

	cctxt = client.prepare(server = 'pike')

	host = cctxt.call({}, 'testSchedule', host = 'pike', arg = '')

        return host

    def select_destinations(self, context, request_spec, filter_properties):
        """Selects random destinations."""

        num_instances = request_spec['num_instances']
        # NOTE(timello): Returns a list of dicts with 'host', 'nodename' and
        # 'limits' as keys for compatibility with filter_scheduler.

        dests = []
        for i in range(num_instances):
            host = self._schedule(context, 'nova.compute.rpcapi',
                    request_spec, filter_properties)
            host_state = dict(host=host, nodename=None, limits=None)
            dests.append(host_state)

        if len(dests) < num_instances:
            raise exception.NoValidHost(reason='')
        return dests

    def schedule_run_instance(self, context, request_spec,
                              admin_password, injected_files,
                              requested_networks, is_first_time,
                              filter_properties, legacy_bdm_in_spec):
        """Create and run an instance or instances."""

        instance_uuids = request_spec.get('instance_uuids')
        for num, instance_uuid in enumerate(instance_uuids):
            request_spec['instance_properties']['launch_index'] = num
            try:
                host = self._schedule(context, 'nova.compute.rpcapi',
                                      request_spec, filter_properties)
                updated_instance = driver.instance_update_db(context,
                        instance_uuid)
                self.compute_rpcapi.run_instance(context,
                        instance=updated_instance, host=host,
                        requested_networks=requested_networks,
                        injected_files=injected_files,
                        admin_password=admin_password,
                        is_first_time=is_first_time,
                        request_spec=request_spec,
                        filter_properties=filter_properties,
                        legacy_bdm_in_spec=legacy_bdm_in_spec)
            except Exception as ex:
                # NOTE(vish): we don't reraise the exception here to make sure
                #             that all instances in the request get set to
                #             error properly
                driver.handle_schedule_error(context, ex, instance_uuid,
                                             request_spec)

