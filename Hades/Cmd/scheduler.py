

__author__ = 'pike'


"""Starter script for customized scheduler."""

from startScript import startService
from oslo.config import cfg

CONF = cfg.CONF

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    startService(CONF.nova_exchange, 'hades-scheduler', CONF.hades_scheduler_topic,
                 'pike', CONF.hades_scheduler_manager)

