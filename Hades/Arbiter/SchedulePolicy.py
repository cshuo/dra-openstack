__author__ = 'pike'

import random

from dra.Openstack.Service import Nova


class SchedulePolicy:
    def __init__(self):
        pass

    def randomSchedule(self):
        novaService = Nova.Nova()
        computeHosts = novaService.getComputeHosts()
        index = random.randint(0, len(computeHosts)-1)
        return computeHosts[index]
        #return host

if __name__ == '__main__':
    policy = SchedulePolicy()
    print policy.randomSchedule()
