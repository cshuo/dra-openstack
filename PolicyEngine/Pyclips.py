__author__ = 'pike'

import clips

def clipsFunction(x):
    #print type(x)
    #str = "hello world: " + x + "\n"
    #print str
    #return str
    print x

def test(x):
    print "test"
    eval(x)

def new(y, z=None):
    print y, 'ok'
    if z == None:
        print "None"


class ClipsEngine:

    def __init__(self):
        self.env = clips.Environment()
        self.env.Clear()

    def assertFact(self, fact):
        try:
            self.env.Assert(fact)
        except:
            print "assert fact failed..."

    def buildTemplate(self, name, slots, comment=""):
        """
        @param name:
        @param slots:
        @param comment:
        @return:
        """
        self.env.BuildTemplate(name, slots, comment)

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

    def listRules(self):
        return self.env.PrintRules()
    
    def listFacts(self):
        return self.env.PrintFacts()



if __name__ == "__main__":
    #rule = """
    #(defrule duck
    #    (animal-is duck)
    #    =>
    #    (printout stdout "clipsFunction" crlf))

    rule = """
        (defrule new_vm
        (newVM cpubound test.new.ow)
        =>
        (python-call test "clipsFunction('hello')"))
    """

    rule2 = """
        (defrule test_rule
        (newVM ?para1 ?para2 ?para3)
        =>
    	(printout stdout ?para1 crlf)
        (python-call new ?para2 ))
    """

    #"""
    #rule = """
    #    (printout stdout ?para1 crlf))
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
    engine.registerPythonFunction(test)
    engine.registerPythonFunction(new)
    #engine.registerPythonFunction(Host_CpuUtil_Filter)
    #engine.registerPythonFunction(Host_CpuUtil_Cost)
    #engine.registerPythonFunction(Get_Host_Resource)
    #engine.registerPythonFunction(Host_resource_upperBound)
    #engine.addRule(rule1)
    engine.addRule(rule2)
    engine.addRule(rule)
    engine.assertFact("(newVM cpubound test.new.ow)")
    engine.assertFact("(newVM cpubound vmInfo1 None)")
    #engine.reset()
    #engine.run()
    # print engine.getStdout()
    print engine.listFacts()
    print engine.listRules()

    eng = ClipsEngine()
    eng.registerPythonFunction(clipsFunction)
    eng.registerPythonFunction(test)
    eng.registerPythonFunction(new)
    eng.addRule(rule2)
    eng.addRule(rule)
    eng.assertFact("(newVM cpubound test.new.ow)")
    eng.assertFact("(newVM cpubound vmInfo1 None)")
    print eng.listFacts()
    print eng.listRules()
