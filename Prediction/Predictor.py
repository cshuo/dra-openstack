__author__ = 'pike'

from Utils.FileUtil import VMfile
from Utils.MathUtil import *

class Predictor:

    def __init__(self,filename):
        self.vmdata=VMfile(filename)

    # add wave lengths with intensity > max/2
    def getFFTCandidate(self,vmname):

        (x,y)=self.vmdata.getData(vmname)
        fft=FFT(x,y)
        (x1,y1)=fft.computeFFT()

        #get local maximum and global maximum
        global_maximum=0
        local_maximum=[]
        for i in range(1,y1.__len__()-1):
            if (y1[i]>=y1[i-1] and y1[i]>=y1[i+1]):
                local_maximum.append([int(even(1/x1[i])),y1[i]])
                if y1[i]>global_maximum:
                    global_maximum=y1[i]


        #add local_maximum with intensity that > global_maximum/2
        result=[]
        for i in range(0,local_maximum.__len__()):
            if (local_maximum[i][1]>=global_maximum/2):
                result.append(local_maximum[i])
        return result



    def getAutoCorrCandidate(self,vmname):
        (x,y)=self.vmdata.getData(vmname)
        auto=AutoCorelation(y)
        y1=auto.autocorr()
        x1=doubleList(range(0,y1.__len__()))

        #get local maximum and global maximum
        global_maximum=0
        local_maximum=[]
        for i in range(1,y1.__len__()-1):
            if (y1[i]>=y1[i-1] and y1[i]>=y1[i+1] and y1[i]>0):
                local_maximum.append([x1[i],y1[i]])
                if y1[i]>global_maximum:
                    global_maximum=y1[i]

        #add local_maximum with p that > global_maximum/2
        result=[]
        for i in range(0,local_maximum.__len__()):
            if (local_maximum[i][1]>=global_maximum/2):
                result.append(local_maximum[i])
        return result

    def getBestCandidate(self,vmname):

        (x,y)=self.vmdata.getData(vmname)
        if (x.__len__()<2):
            return 0
        auto=AutoCorelation(y)
        y1=auto.autocorr()
        x1=doubleList(range(0,y1.__len__()))

        list1=self.getFFTCandidate(vmname)
        list2=self.getAutoCorrCandidate(vmname)
        list1.extend(list2)

        #mset contains all the candidate wavelength
        mset=set()
        for i in range(0,list1.__len__()):
            mset.add(list1[i][0])

        maxlen=x1[x1.__len__()-1]
        bestwavelen=0
        maxp=-1e13

        for wavelen in mset:
            multi=1
            total=0
            while(wavelen*multi<=maxlen):
                index=x1.index(wavelen*multi)
                total+=y1[index]
                multi+=1
            if multi==1:
                multi=2
            average=total/(multi-1)
            if average>maxp:
                bestwavelen=wavelen
                maxp=average

        return bestwavelen









if __name__=="__main__":
    file=open('../VMs.csv',"r")
    lines=file.readlines()[1:]

    vmset=set()
    for line in lines:
        vmname=line.split(',')[0]
        vmset.add(vmname)
    vmset.remove('\r\n')
    file.close()

    predictor=Predictor('../VMs.csv')
    outfile=open("../OUTPUT","w")
    for vmname in vmset:
        bestcandidate=predictor.getBestCandidate(vmname)
        resultline=vmname+"\t"+str(bestcandidate)+"\t"+"%.2f" % (bestcandidate/24.0)+'\n'
        outfile.write(resultline)
    outfile.close()



