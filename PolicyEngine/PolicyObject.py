__author__ = 'pike'

from Action import Action
from Event import Event
from Subject import Subject
from Target import Target

class PolicyObject:

    def __init__(self, name, type, **kwargs):
        self.name = name
        self.type = type
        self.enabled = False

        self.subject = Subject(kwargs['subject'])
        self.target = Target(kwargs['target'])
        self.event = Event(kwargs['onEvent'])
        self.action = Action(kwargs['action'])

    def getSubject(self):
        return self.subject

    def getTarget(self):
        return self.target

    def getEvent(self):
        return self.event

    def getAction(self):
        return self.action

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def isEnabled(self):
        return self.enabled


    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

