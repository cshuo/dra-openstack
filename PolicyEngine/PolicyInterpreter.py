__author__ = 'pike'

import xml.etree.cElementTree as ET
from  PolicyObject import PolicyObject

class PolicyInterpreter:

    def __init__(self):
        pass

    @staticmethod
    def getPolicyObjectFromFile(file):
        tree = ET.ElementTree(file = file)
        root = tree.getroot()
        type = root.attrib['type']

        kwarg = {}
        for item in root:
            key = item.tag
            value = item.text
            kwarg[key] = value

        policyObj = PolicyObject(type, **kwarg)

        return policyObj


if __name__ == "__main__":

    pObj = PolicyInterpreter.getPolicyObjectFromFile("../Resource/testPolicy.xml")
    print pObj.type



