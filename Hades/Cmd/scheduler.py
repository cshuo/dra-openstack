__author__ = 'pike'


"""Starter script for customized scheduler."""
from pkg_resources import iter_entry_points
from Hades import Service
from Hades import Config
from oslo.messaging import TransportURL
from oslo.messaging import InvalidTransportURL
from oslo.config import cfg

CONF = cfg.CONF

def main():

    Config.config_init()

    server = Service.Service.create(binary = 'hades-scheduler',
                                    topic = CONF.scheduler_topic,
                                    host = 'localhost',
                                    manager = CONF.scheduler_manager)
    Service.serve(server)
    Service.wait()

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    main()
