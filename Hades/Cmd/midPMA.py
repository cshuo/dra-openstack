# -*- coding: utf-8 -*-
"""Starter script for arbiterPMA."""

from oslo_config import cfg
from .startScript import startService
from ...Openstack.Conf import OpenstackConf

CONF = cfg.CONF

if __name__ == "__main__":
    startService(CONF.hades_exchange, 'hades-midPMA', CONF.hades_midPMA_topic,
                 OpenstackConf.DEFAULT_RPC_SERVER, CONF.hades_midPMA_manager)
