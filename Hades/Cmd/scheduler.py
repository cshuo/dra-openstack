"""Starter script for customized scheduler."""
from oslo_config import cfg
from dra.Hades.Cmd.startScript import startService

CONF = cfg.CONF

if __name__ == "__main__":

    startService(CONF.hades_exchange, 'hades-scheduler', CONF.hades_scheduler_topic,
                 'pike', CONF.hades_scheduler_manager)

