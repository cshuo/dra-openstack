__author__ = 'pike'

from Pyclips import ClipsEngine
from PolicyEngine.Arbiter.Arbiter import *

registerFunctions = [
    migrate
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



if __name__ == "__main__":
    rule = """
    (defrule duck
        (animal-is duck)
        (type str)
        =>
        (python-call migrate))
    """
    policy = PolicyManager()
    policy.loadRule("duck", rule)
    policy.assertFact("(animal-is duck)")
    policy.assertFact("(type str)")
    policy.run()
