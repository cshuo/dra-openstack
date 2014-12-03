__author__ = 'pike'

import clips


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




if __name__ == "__main__":
    rule = """
    (defrule duck
        (animal-is duck)
        =>
        (python-call clipsFunction [woshipike,wo]))
    """

    engine = ClipsEngine()
    engine.registerPythonFunction(clipsFunction)
    engine.addRule(rule)
    engine.assertFact("(animal-is duck)")
    engine.removeRule("s")
    engine.run()
    #print clips.StdoutStream.Read()
    #print clips.ErrorStream.Read()
    #print clips.TraceStream.Read()
