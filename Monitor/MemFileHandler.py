__author__ = 'pike'
import string

class MemFileHandler:

    def __init__(self,memfilename):
        self.memfile=open(memfilename)
        self.lines=self.memfile.readlines()
        self.attributes={}
        self.getAllAttributes()


    # store all key-value pairs in the meminfo file in the dictionary attributes
    def getAllAttributes(self):
        for line in self.lines:
            templist=line.split(" ")

            #lines in the file may end with "0\n" or "xxxx kB\n"
            name=templist[0].replace(":","")
            if(templist[-1].__eq__("kB\n")):
                self.attributes[name]=string.atoi(templist[-2])
            else:
                self.attributes[name]=0


    def getMemTotal(self):
        return self.attributes["MemTotal"]

    def getMemFree(self):
        return self.attributes["MemFree"]