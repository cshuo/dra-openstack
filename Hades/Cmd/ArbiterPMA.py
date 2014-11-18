__author__ = 'pike'


"""Starter script for policyService."""

from Hades import Service
from Hades import Config
from oslo.config import cfg

CONF = cfg.CONF

def main():

    Config.config_init(CONF.hades_exchange)

    server = Service.Service.create(binary = 'hades-arbiterPMA',
                                    topic = CONF.hades_arbiterPMA_topic,
                                    host = 'pike',
                                    manager = CONF.hades_arbiterPMA_manager)
    Service.serve(server)
    Service.wait()

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    main()
