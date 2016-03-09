__author__ = 'pike'

from dra.Hades import Service
from dra.Hades import Config


def startService(exchange, serviceBinary, serviceTopic, serviceHost, serviceManager):

    Config.config_init(exchange)

    server = Service.Service.create(binary = serviceBinary,
                                    topic = serviceTopic,
                                    host = serviceHost,
                                    manager = serviceManager)
    Service.serve(server)
    Service.wait()

if __name__ == "__main__":

    #for entry in iter_entry_points(group='oslo.messaging.drivers', name=None):
    #    print entry
    pass
