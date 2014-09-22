__author__ = 'pike'

from Hades.Common.ThreadGroup import *

class Service(object):

     """Service object for binaries running on hosts."""

     def __init__(self, threads = 1000):
         self.tg = ThreadGroup