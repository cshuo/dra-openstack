__author__ = 'pike'

from Utils.FileUtil import VMfile
from Utils.MathUtil import *
class Predictor:

    def __init__(self,filename):
        self.vmdata=VMfile()
        self.filename=filename


    # add wave lengths with intensity > max/2
    def getFFTCandidate(self):

        (x,y)=self.vmdata.getData(self.filename)
        fft=FFT(x,y)
        (x1,y1)=fft.computeFFT()

        #get local maximum and global maximum
        global_maximum=0
        local_maximum=[]
        for i in range(1,y1.__len__()-1):
            if (y1[i]>=y1[i-1] and y1[i]>=y1[i+1]):
                local_maximum.append([x1[i],y1[i]])
                if y1[i]>global_maximum:
                    global_maximum=y1[i]

        print local_maximum.__len__()

        #add local_maximum with intensity that > global_maximum/2
        result=[]
        for i in range(0,local_maximum.__len__()):
            if (local_maximum[i][1]>=global_maximum/2):
                result.append(local_maximum[i])
        return result



    def getAutoCorrCandidate(self):
        (x,y)=self.vmdata.getData(self.filename)
        auto=AutoCorelation(y)
        y1=auto.autocorr()
        x1=doubleList(range(0,y1.__len__()))

        #get local maximum and global maximum
        global_maximum=0
        local_maximum=[]
        for i in range(1,y1.__len__()-1):
            if (y1[i]>=y1[i-1] and y1[i]>=y1[i+1]):
                local_maximum.append([x1[i],y1[i]])
                if y1[i]>global_maximum:
                    global_maximum=y1[i]

        #add local_maximum with p that > global_maximum/2
        result=[]
        for i in range(0,local_maximum.__len__()):
            if (local_maximum[i][1]>=global_maximum/2):
                result.append(local_maximum[i])
        return result



if __name__=="__main__":
    predictor=Predictor('../VMs.csv')
    #predictor.getFFTCandidate()
    predictor.getAutoCorrCandidate()