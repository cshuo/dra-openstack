# -*- coding: utf-8 -*-

"""
Start script for service on controller node
"""

from oslo_config import cfg
from dra.Hades.Cmd.startScript import startService
import socket


CONF = cfg.CONF


if __name__ == '__main__':
    startService(CONF.hades_exchange, 'hades-compute-service', CONF.hades_compute_topic, 
            socket.gethostname(), CONF.hades_compute_manager)
