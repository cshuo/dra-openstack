__author__ = 'pike'


"""Starter script for customized scheduler."""

from Openstack import Service

def main():

    server = Service.Service.create()
    Service.serve(server)
    Service.wait()
