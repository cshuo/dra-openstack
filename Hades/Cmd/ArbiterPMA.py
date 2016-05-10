# -*- coding: utf-8 -*-
"""Starter script for arbiterPMA."""

from oslo_config import cfg
from .startScript import startService
from ...Openstack.Conf import OpenstackConf

CONF = cfg.CONF

if __name__ == "__main__":
    # for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    startService(CONF.hades_exchange, 'hades-arbiterPMA', CONF.hades_arbiterPMA_topic,
                 OpenstackConf.DEFAULT_RPC_SERVER, CONF.hades_arbiterPMA_manager)

