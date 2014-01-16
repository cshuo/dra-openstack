__author__ = 'pike'

import os
import matplotlib.pyplot as plt
import sys
import string

class VMfile:


    def __init__(self):pass

    '''get the specific vm x,y axis data'''

    def getData(self,filename):
        file=open(filename,"r")
        alllines=file.readlines();
        x_axis=[]
        y_axis=[]

        time=0;
        for line in alllines:
            split=line.split(",")
            #if (split[0].startswith('"Gart')):
            if (split[0].startswith('"wangyi')):
            #if (split[0].startswith('"JiaoTong-ETC')):
            #if (split[0].startswith('"JiaoTong_Shuiyun')):

                y_axis.append(float(split[4].strip('"')))
                x_axis.append(time)
                time+=2
        return (x_axis,y_axis)


    def plot(self,x,y):
        plt.figure()
        plt.plot(x,y)
        plt.title("cpu usage")
        plt.xlabel("time")
        plt.ylabel("cpu utility")
        #plt.ylim([0,100])
        plt.show()


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


if __name__=="__main__":
    vmdata=VMfile()
    (x,y)=vmdata.getData('../VMs.csv')
    vmdata.plot(x,y)