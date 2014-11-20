__author__ = 'pike'

from oslo.config import cfg
from Hades import BaseRpcApi
from PolicyEngine.PolicyInterpreter import PolicyInterpreter


CONF =  cfg.CONF

class PolicyServiceAPI(BaseRpcApi.BaseAPI):

    """
    client side of the policyService rpc API
    """

    def __init__(self, topic, exchange):
        super(PolicyServiceAPI, self).__init__(topic, exchange)


    def loadPolicy(self, ctxt, host, policy):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'loadPolicy',
                   host = host, policy = policy)

if __name__ == "__main__":
    print 'policyService rpcapi\n'

    #get policy string from policy file
    fp = open("../../Resource/testPolicy.xml", "r")
    lines = fp.readlines()
    policyStr = ""
    for line in lines:
        policyStr += line

    #print policyStr

    api = PolicyServiceAPI(CONF.hades_policyService_topic, CONF.hades_exchange)
    print api.loadPolicy({}, 'pike', policyStr)
