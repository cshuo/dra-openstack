__author__ = 'pike'


"""Starter script for arbiter."""


from startScript import startService
from oslo_config import cfg

CONF = cfg.CONF

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    startService(CONF.hades_exchange, 'hades-arbiter', CONF.hades_arbiter_topic,
                 'pike', CONF.hades_arbiter_manager)

