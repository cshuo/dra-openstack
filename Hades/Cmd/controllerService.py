# -*- coding: utf-8 -*-

"""
Start script for service on compute node
"""

from oslo_config import cfg
from dra.Hades.Cmd.startScript import startService
import socket


CONF = cfg.CONF


if __name__ == '__main__':
    startService(CONF.hades_exchange, 'hades-controller-service', CONF.hades_controller_topic, 
            'pike', CONF.hades_controller_manager)
