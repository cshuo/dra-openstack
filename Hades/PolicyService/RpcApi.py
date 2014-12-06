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


    def loadPolicy(self, ctxt, host, policys):
        cctxt = self.client.prepare(server = host)
        return cctxt.call(ctxt, 'loadPolicy',
                   host = host, policys = policys)

if __name__ == "__main__":
    print 'policyService rpcapi\n'


    policys = PolicyInterpreter.readPolicyFromFile("../../Resource/testPolicy.xml")



    api = PolicyServiceAPI(CONF.hades_policyService_topic, CONF.hades_exchange)
    print policys
    print api.loadPolicy({}, 'pike', policys)
