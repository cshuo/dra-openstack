__author__ = 'pike'

from oslo.config import cfg
from Hades import Rpc

#CONF is a global instance
CONF = cfg.CONF

rpcapi_opts = [
    cfg.StrOpt('scheduler_topic',
               default = 'hades_scheduler',
               help = 'the topic hades nodes listen on'),
]

scheduler_manager_opts = [
    cfg.StrOpt('scheduler_manager',
               default = 'Hades.Scheduler.Manager.SchedulerManager',
               help = 'hades scheduler manager'
    )
]

transport = [
    cfg.StrOpt('rabbit_url',
               default = 'rabbit://guest:RABBIT_PASS@114.212.189.134:5672/',
               help = 'rabbit url'),
    cfg.StrOpt('exchange',
               default = 'hades',
               help = 'exchange for hades service')
]


CONF.register_opts(rpcapi_opts)
CONF.register_opts(scheduler_manager_opts)
CONF.register_opts(transport)

def config_init(argv = None, default_config_files = None):
    print 'config parse_args\n'
    Rpc.set_defaults(control_exchange = 'hades')
    Rpc.init(CONF)