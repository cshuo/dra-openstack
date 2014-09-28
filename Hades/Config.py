__author__ = 'pike'

from oslo.config import cfg
from Hades import Rpc

#CONF is a global instance
CONF = cfg.CONF

def parse_args(argv = None, default_config_files = None):
    print 'config parse_args\n'
    Rpc.set_defaults(control_exchange = 'hades')
    #CONF(argv[1:],
    #     version = '1.0',
    #     default_config_files = default_config_files)

    #CONF( rabbit_opts = 'oslo.messaging._drivers.impl_rabbit')
    Rpc.init(CONF)