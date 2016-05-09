__author__ = 'pike'

import xml.etree.cElementTree as ET

class PolicyInterpreter:

    def __init__(self):
        pass

    @staticmethod
    def readPolicyFromFile(file):
        tree = ET.ElementTree(file=file)
        policyGroup = tree.getroot()
        policys = []
        for policy in policyGroup:
            policyName = policy.attrib['name']
            target = policy.attrib['target']
            rules = {}
            for rule in policy:
                ruleName = rule.attrib['name']
                rule = rule.text
                rules[ruleName] = rule
            policys.append({'name': policyName,
                            'target': target,
                            'rules': rules})
        return policys


if __name__ == "__main__":
    policys = PolicyInterpreter.readPolicyFromFile("dra/Resource/testPolicy.xml")
    print policys
