__author__ = 'pike'

from dra.PolicyEngine.Pyclips import ClipsEngine
from dra.PolicyEngine.ExternalFunction import *

registerFunctions = [
    test_eva,
    Host_Filter,
    simple_host_filter,
    Collect_Data,
    Collect_Data_Statistics,
    Get_Vms_On_Host,
    Host_Set_Threshold,
    Host_Generic_Selector,
    Vm_Random_Selector,
    Migrate
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

    def buildTemplate(self, name, slots, comment=''):
        self.clipsEngine.buildTemplate(name, slots, comment)

    def run(self):
        self.clipsEngine.run()

    def getStdout(self):
        return self.clipsEngine.getStdout()



if __name__ == "__main__":
    rule = """
        (defrule new_vm
        (newVM cpubound vmInfo)
        =>
        (bind ?vms (python-call Get_Vms_On_Host "compute2"))
        (bind ?vm (python-call Vm_Random_Selector ?vms))
        (bind ?hosts (python-call simple_host_filter))
        (bind ?destHost (python-call Host_Generic_Selector ?hosts "['Host_CpuUtil_Cost']" "[1]"))
        (printout stdout ?destHost crlf)
        (python-call Migrate ?vm ?destHost))
    """
   
    policy = PolicyManager()
    policy.loadRule("new_vm", rule)
    policy.assertFact("(newVM cpubound vmInfo)")
    policy.run()
    print policy.getStdout()
