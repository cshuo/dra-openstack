__author__ = 'pike'


"""Starter script for customized scheduler."""

from Openstack import Service

def main():

    config.parse_args(sys.argv)

    server = Service.Service.create()
    Service.serve(server)
    Service.wait()
