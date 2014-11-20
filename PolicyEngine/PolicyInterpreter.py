__author__ = 'pike'

import xml.etree.cElementTree as ET
from  PolicyObject import PolicyObject

class PolicyInterpreter:

    def __init__(self):
        pass

    @staticmethod
    def getPolicyObjectsFromFile(file):
        tree = ET.ElementTree(file = file)
        root = tree.getroot()
        return PolicyInterpreter.getPolicyObjectsFromRoot(root)

    @staticmethod
    def getPolicyObjectsFromString(xmlStr):
        root = ET.fromstring(xmlStr)
        return PolicyInterpreter.getPolicyObjectsFromRoot(root)

    @staticmethod
    def getPolicyObjectsFromRoot(root):
        policyObjs = []
        # root refers to policygroup
        policyGroup = root

        for policy in policyGroup:
            type = policy.attrib['type']
            name = policy.attrib['name']
            kwargs = {}
            for item in policy:
                key = item.tag
                value = item.text
                kwargs[key] = value
            policyObj = PolicyObject(name, type, **kwargs)
            policyObjs.append(policyObj)

        return policyObjs



if __name__ == "__main__":

    pObjs = PolicyInterpreter.getPolicyObjectsFromFile("../Resource/testPolicy.xml")
    print pObjs[0].type



