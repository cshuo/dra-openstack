__author__ = 'cshuo'

from oslo_config import cfg
import logging
from cliff.command import Command

#from dra.cli.startScript import startService
from ..cli.startScript import startService

CONF = cfg.CONF

class Schedule(Command):
    "A command that start scheduler service."
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('scheduler service starting...')
        startService(CONF.hades_exchange, 'hades-arbiter', CONF.hades_arbiter_topic,
                 'pike', CONF.hades_arbiter_manager)


class ArbiterPMA(Command):
    "A command that start arbiterPMA service."
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('arbiterPMA service starting...')
        startService(CONF.hades_exchange, 'hades-arbiterPMA', CONF.hades_arbiterPMA_topic,
                 'pike', CONF.hades_arbiterPMA_manager)


class MonitorPMA(Command):
    "A command that start monitorPMA service."
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('monitorPMA service starting...')
        startService(CONF.hades_exchange, 'hades-monitorPMA', CONF.hades_monitorPMA_topic,
                 'pike', CONF.hades_monitorPMA_manager)


class PolicyService(Command):
    "A command that start arbiterPMA service."
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('policy service starting...')
        startService(CONF.hades_exchange, 'hades-policyService', CONF.hades_policyService_topic,
                 'pike', CONF.hades_policyService_manager)


class EventService(Command):
    "A command that start arbiterPMA service."
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('event service starting...')
        startService(CONF.hades_exchange, 'hades-eventService', CONF.hades_eventService_topic,
                 'pike', CONF.hades_eventService_manager)
