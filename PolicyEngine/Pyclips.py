__author__ = 'pike'

import clips
from ExternalFunction import *

def clipsFunction(x):
    #print type(x)
    #str = "hello world: " + x + "\n"
    #print str
    #return str
    print x


class ClipsEngine:

    def __init__(self):
        self.env = clips.Environment()
        self.env.Clear()

    def assertFact(self, fact):
        self.env.Assert(fact)

    def addRule(self, rule):
        self.env.Build(rule)

    def removeRule(self, ruleName):
        try:
            r = self.env.FindRule(ruleName)
            r.Remove()
        except Exception:
            pass

    def registerPythonFunction(self, function):
        clips.RegisterPythonFunction(function)

    def run(self):
        self.env.Run()
        self.env.Reset()

    def reset(self):
        self.env.Reset()

    def getStdout(self):
        return clips.StdoutStream.Read()




if __name__ == "__main__":
    #rule = """
    #(defrule duck
    #    (animal-is duck)
    #    =>
    #    (printout stdout "clipsFunction" crlf))

    rule = """
        (defrule new_vm
        (newVM cpubound vmInfo)
        =>
        (bind ?hosts 45)
        (python-call clipsFunction hello?hosts))
    """

    #"""
    #rule = """
    #    (defrule new_vm
    #    (newVM cpubound vmInfo)
    #    =>
    #    (bind ?hosts (python-call Host_CpuUtil_Filter))
    #    (bind ?destHost (python-call Host_CpuUtil_Cost ?hosts))
    #    (printout stdout ?destHost crlf))
    #"""


    #rule1 = """
    #    (defrule collect_0
    #    (collect host ?host_id ?resource)
    #    =>
    #    (bind ?value (python-call Get_Host_Resource ?host_id ?resource))
    #    (assert (collected host ?host_id ?resource ?value)))
    #"""
    #rule2 = """
    #    (defrule upperBound_0
    #    (collected host ?host_id ?resource ?value)
    #    =>
    #    (python-call Host_resource_upperBound ?host_id ?resource ?value))
    #"""

    engine = ClipsEngine()
    engine.registerPythonFunction(clipsFunction)
    #engine.registerPythonFunction(Host_CpuUtil_Filter)
    #engine.registerPythonFunction(Host_CpuUtil_Cost)
    #engine.registerPythonFunction(Get_Host_Resource)
    #engine.registerPythonFunction(Host_resource_upperBound)
    #engine.addRule(rule1)
    #engine.addRule(rule2)
    engine.addRule(rule)
    engine.assertFact("(newVM cpubound vmInfo)")
    engine.run()

