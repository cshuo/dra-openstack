__author__ = 'pike'

from oslo.config import cfg
from Hades import Rpc

#CONF is a global instance
CONF = cfg.CONF

rpcapi_opts = [
    cfg.StrOpt('hades_scheduler_topic',
               default = 'hades_scheduler_test',
               help = 'the topic hades nodes listen on'),
    cfg.StrOpt('hades_arbiter_topic',
               default = 'hades_arbiter_test',
               help = 'the topic hades arbiter nodes listen on'),
    cfg.StrOpt('hades_policyService_topic',
               default = 'hades_policyService_topic',
               help = 'the topic hades policyService nodes listen on'),
    cfg.StrOpt('hades_arbiterPMA_topic',
               default = 'hades_arbiterPMA_topic',
               help = 'the topic hades arbiterPMA nodes listen on')
]

manager_opts = [
    cfg.StrOpt('hades_scheduler_manager',
               default = 'Hades.Scheduler.Manager.SchedulerManager',
               help = 'hades scheduler manager'),
    cfg.StrOpt('hades_arbiter_manager',
               default = 'Hades.Arbiter.Manager.ArbiterManager',
               help = 'hades arbiter manager'),
    cfg.StrOpt('hades_policyService_manager',
               default = 'Hades.PolicyService.Manager.PolicyServiceManager',
               help = 'hades policyService manager'),
    cfg.StrOpt('hades_arbiterPMA_manager',
               default = 'Hades.PMA.Manager.ArbiterPMAManager',
               help = 'hades arbiterPMA manager')
]

transport = [
    cfg.StrOpt('hades_rabbit_url',
               default = 'rabbit://guest:RABBIT_PASS@114.212.189.134:5672/',
               help = 'rabbit url'),
    cfg.StrOpt('hades_exchange',
               default = 'hades',
               help = 'exchange for hades service'),
    cfg.StrOpt('nova_exchange',
               default = 'nova',
               help = 'nova exchange')
]


CONF.register_opts(rpcapi_opts)
CONF.register_opts(manager_opts)
CONF.register_opts(transport)

def config_init(exchange, argv = None, default_config_files = None):
    print 'config init\n'
    Rpc.set_defaults(control_exchange = exchange)
    Rpc.init(CONF)