__author__ = 'pike'

import clips
from ExternalFunction import *

def clipsFunction(x):
    print type(x)
    str = "hello world: " + x + "\n"
    print str
    return str


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
    #"""
    rule = """
        (defrule new_vm
        (newVM cpubound vmInfo)
        =>
        (bind ?hosts (python-call Host_CpuUtil_Filter))
        (bind ?destHost (python-call Host_CpuUtil_Cost ?hosts))
        (printout stdout ?destHost crlf))
    """

    engine = ClipsEngine()
    engine.registerPythonFunction(clipsFunction)
    engine.registerPythonFunction(Host_CpuUtil_Filter)
    engine.registerPythonFunction(Host_CpuUtil_Cost)
    engine.addRule(rule)
    engine.assertFact("(newVM cpubound vmInfo)")
    engine.run()
    print clips.StdoutStream.Read()
