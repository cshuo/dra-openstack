from oslo_config import cfg
from dra.Hades import Rpc


# CONF is a global instance
CONF = cfg.CONF

rpcapi_opts = [
    cfg.StrOpt('hades_scheduler_topic',
               default='hades_scheduler_topic',
               help='the topic hades nodes listen on'),
    cfg.StrOpt('hades_controller_topic',
               default='hades_controller_topic',
               help='the topic hades nodes listen on'),
    cfg.StrOpt('hades_compute_topic',
               default='hades_compute_topic',
               help='the topic hades nodes listen on'),
    cfg.StrOpt('hades_arbiter_topic',
               default='hades_arbiter_test',
               help='the topic hades arbiter nodes listen on'),
    cfg.StrOpt('hades_policyService_topic',
               default='hades_policyService_topic',
               help='the topic hades policyService nodes listen on'),
    cfg.StrOpt('hades_arbiterPMA_topic',
               default='hades_arbiterPMA_topic',
               help='the topic hades arbiterPMA nodes listen on'),
    cfg.StrOpt('hades_midPMA_topic',
               default='hades_midPMA_topic',
               help='the topic hades PMA for eliminate rpc block'),
    cfg.StrOpt('hades_monitorPMA_topic',
               default='hades_monitorPMA_topic',
               help='the topic hades monitorPMA nodes listen on'),
    cfg.StrOpt('hades_eventService_topic',
               default='hades_eventService_topic',
               help='the topic hades eventService nodes listen on')
]

manager_opts = [
    cfg.StrOpt('hades_scheduler_manager',
               default='dra.Hades.scheduler.manager.DynamicSchedulerManager',
               help='hades scheduler manager'),
    cfg.StrOpt('hades_controller_manager',
               default='dra.Hades.controller.manager.ControllerManager',
               help='hades controller manager'),
    cfg.StrOpt('hades_compute_manager',
               default='dra.Hades.compute.manager.ComputeManager',
               help='hades compute manager'),
    cfg.StrOpt('hades_arbiter_manager',
               default='dra.Hades.Arbiter.Manager.ArbiterManager',
               help='hades arbiter manager'),
    cfg.StrOpt('hades_policyService_manager',
               default='dra.Hades.PolicyService.Manager.PolicyServiceManager',
               help='hades policyService manager'),
    cfg.StrOpt('hades_arbiterPMA_manager',
               default='dra.Hades.PMA.Manager.ArbiterPMAManager',
               help='hades arbiterPMA manager'),
    cfg.StrOpt('hades_midPMA_manager',
               default='dra.Hades.PMA.Manager.MidPMAManager',
               help='hades midPMA manager'),
    cfg.StrOpt('hades_monitorPMA_manager',
               default='dra.Hades.PMA.Manager.MonitorPMAManager',
               help='hades monitorPMA manager'),
    cfg.StrOpt('hades_eventService_manager',
               default='dra.Hades.EventService.Manager.EventServiceManager',
               help='hades eventService manager')
]

transport = [
    cfg.StrOpt('hades_rabbit_url',
               default='rabbit://openstack:jPdCcwusY1njEZdzH4y7671bLmcUOjVOer4CD32c@20.0.1.10:5672/',
               help='rabbit url'),
    cfg.StrOpt('hades_exchange',
               default='hades',
               help='exchange for hades service'),
    cfg.StrOpt('nova_exchange',
               default='nova',
               help='nova exchange')
]


CONF.register_opts(rpcapi_opts)
CONF.register_opts(manager_opts)
CONF.register_opts(transport)


def config_init(exchange, argv = None, default_config_files = None):
    Rpc.set_defaults(control_exchange=exchange)
    Rpc.init(CONF)
