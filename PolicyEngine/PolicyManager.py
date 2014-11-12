__author__ = 'pike'

from PolicyInterpreter import PolicyInterpreter

class PolicyManager:

    def __init__(self):
        self.policyObjs = []

    def addPolicy(self, policy):
        self.policyObjs.append(policy)

    def deletePolicy(self):
        pass

    def getPolicyOnEvent(self, event):
        result = []
        for policy in self.policyObjs:
            if (policy.getEvent() == event):
                result.append(policy)
        return result


if __name__ == "__main__":
    policyObj = PolicyInterpreter.getPolicyObjectFromFile("../Resource/testPolicy.xml")
    policyManager = PolicyManager()
    policyManager.addPolicy(policyObj)
    result = policyManager.getPolicyOnEvent("eventValue")
    print result[0].getType()