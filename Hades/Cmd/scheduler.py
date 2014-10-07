__author__ = 'pike'


"""Starter script for customized scheduler."""

from Hades import Service
from Hades import Config
from oslo.config import cfg

CONF = cfg.CONF

def main():

    Config.config_init(CONF.nova_exchange)

    server = Service.Service.create(binary = 'hades-scheduler',
                                    topic = CONF.hades_scheduler_topic,
                                    host = 'localhost',
                                    manager = CONF.hades_scheduler_manager)
    Service.serve(server)
    Service.wait()

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    main()
