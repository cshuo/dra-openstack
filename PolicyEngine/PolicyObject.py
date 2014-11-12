__author__ = 'pike'

import Action
import Condition
import Event
import Subject
import Target

class PolicyObject:

    def __init__(self, type, **kwargs):
        self.type = type
        self.enabled = False

        self.subject = kwargs['subject']
        self.target = kwargs['target']
        self.event = kwargs['onEvent']
        self.action = kwargs['action']

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

    def isEnabled(self):
        return self.enabled


    def enable(self):
        pass

    def disable(self):
        pass

