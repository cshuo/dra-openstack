__author__ = 'pike'

from Pyclips import ClipsEngine
from ExternalFunction import *

registerFunctions = [
    migrate,
    Host_CpuUtil_Cost,
    Host_CpuUtil_Filter
]

class PolicyManager:

    def __init__(self):
        self.clipsEngine = ClipsEngine()
        self.rules = {}

        for function in registerFunctions:
            self.clipsEngine.registerPythonFunction(function)

    def loadPolicy(self, policy):
        rules = policy['rules']
        for ruleName in rules.keys():
            rule = rules[ruleName]
            self.loadRule(ruleName, rule)

    def loadRule(self, ruleName, rule):
        self.rules[ruleName] = rule
        self.clipsEngine.addRule(rule)

    def unloadRule(self, ruleName):
        self.clipsEngine.removeRule(ruleName)
        self.rules.__delitem__(ruleName)

    def enableRule(self, ruleName):
        rule = self.rules[ruleName]
        self.clipsEngine.addRule(rule)

    def disableRule(self, ruleName):
        self.clipsEngine.removeRule(ruleName)

    def assertFact(self, fact):
        self.clipsEngine.assertFact(fact)

    def run(self):
        self.clipsEngine.run()

    def getStdout(self):
        return self.clipsEngine.getStdout()



if __name__ == "__main__":
    rule = """
        (defrule new_vm
        (newVM cpubound vmInfo)
        =>
        (bind ?hosts (python-call Host_CpuUtil_Filter))
        (bind ?destHost (python-call Host_CpuUtil_Cost ?hosts))
        (printout stdout ?destHost crlf))
    """
    policy = PolicyManager()
    policy.loadRule("new_vm", rule)
    policy.assertFact("(newVM cpubound vmInfo)")
    policy.run()
    print policy.getStdout()
