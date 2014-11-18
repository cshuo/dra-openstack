__author__ = 'pike'

from PolicyInterpreter import PolicyInterpreter

class PolicyManager:

    #use policy name to be the unique id
    def __init__(self):
        self.policyObjs = {}

    def addPolicy(self, policy):
        self.policyObjs[policy.getName()] = policy

    def addPolicyFromXML(self, xmlPolicy):
        policyObj = PolicyInterpreter.getPolicyObjectsFromString(xmlPolicy)
        self.addPolicy(policyObj)

    def deletePolicy(self, name):
        self.policyObjs.__delitem__(name)

    def getPolicyByName(self, name):
        return self.policyObjs.get(name)

    def getPolicyOnEvent(self, event):
        result = []
        for policy in self.policyObjs:
            if (policy.getEvent().getValue() == event):
                result.append(policy)
        return result


if __name__ == "__main__":
    policyObjs = PolicyInterpreter.getPolicyObjectsFromFile("../Resource/testPolicy.xml")
    policyManager = PolicyManager()

    policyManager.addPolicy(policyObjs[0])
    policyManager.addPolicy(policyObjs[1])

    result = policyManager.getPolicyOnEvent("eventValue")
    print result[0].getType()