

__author__ = 'pike'


"""Starter script for policyService."""

from startScript import startService
from oslo.config import cfg

CONF = cfg.CONF

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    startService(CONF.hades_exchange, 'hades-policyService', CONF.hades_policyService_topic,
                 'pike', CONF.hades_policyService_manager)
