__author__ = 'pike'

from oslo.config import cfg
from Hades import Rpc

#CONF is a global instance
CONF = cfg.CONF


def parse_args(argv, default_config_files = None):
    Rpc.set_defaults(control_exchange = 'hades')
    CONF(argv[1:],
         version = '1.0',
         default_config_files = default_config_files)
    Rpc.init(CONF)