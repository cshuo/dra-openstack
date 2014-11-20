__author__ = 'pike'

from PolicyInterpreter import PolicyInterpreter

class PolicyManager:

    #use policy name to be the unique id
    def __init__(self):
        self.policyObjs = {}

    def addPolicy(self, policy):
        self.policyObjs[policy.getName()] = policy

    def addPolicys(self, policys):
        for policy in policys:
            self.addPolicy(policy)


    def addPolicysFromXML(self, xmlPolicy):
        policyObjs = PolicyInterpreter.getPolicyObjectsFromString(xmlPolicy)
        self.addPolicys(policyObjs)

    def deletePolicy(self, name):
        self.policyObjs.__delitem__(name)

    def getPolicyByName(self, name):
        return self.policyObjs.get(name)

    def getPolicysOnEvent(self, event):
        result = []
        for policy in self.policyObjs:
            if (policy.getEvent().getValue() == event):
                result.append(policy)
        return result

    def enablePolicy(self, name):
        policy = self.policyObjs[name]
        policy.enable()

    def disablePolicy(self, name):
        policy = self.policyObjs[name]
        policy.disable()


if __name__ == "__main__":
    #policyObjs = PolicyInterpreter.getPolicyObjectsFromFile("../Resource/testPolicy.xml")
    #policyManager = PolicyManager()
    #
    #policyManager.addPolicy(policyObjs[0])
    #policyManager.addPolicy(policyObjs[1])
    #
    #result = policyManager.getPolicyOnEvent("eventValue")
    #print result[0].getType()
    pass