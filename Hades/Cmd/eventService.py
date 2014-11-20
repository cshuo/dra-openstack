__author__ = 'pike'


"""Starter script for eventService."""

from startScript import startService
from oslo.config import cfg

CONF = cfg.CONF

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    startService(CONF.hades_exchange, 'hades_eventService', CONF.hades_eventService_topic,
                 'pike', CONF.hades_eventService_manager)
