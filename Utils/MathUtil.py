__author__ = 'pike'


import numpy as np
import matplotlib.pyplot as plt
from FileUtil import VMfile
from PlotUtil import Plot
import math

def minusAverage(list):
    average=sum(list)/list.__len__()
    for i in range(0,list.__len__()):
        list[i]-=average
    return list

def doubleList(list):
    for i in range(0,list.__len__()):
        list[i]=2*list[i]
    return list

def even(num):
    if (math.ceil(num)%2==0):
        return math.ceil(num)
    else:
        if (math.floor(num)%2==0):
            return math.floor(num)
        else:
            return math.floor(num)+1

class FFT:

    def __init__(self,x,y):
        self.x=x
        self.y=y


    #compute fft will return (x,y) represent frequency and intensity
    def computeFFT(self):
        if (self.x.__len__()<2):
            return None

        #remove the direct current component
        fft_sig=np.fft.rfft(minusAverage(self.y))

        #Fs : sample frequency ; Fmax : wave's bandwidth ; N : total sampling number
        Fs=1.0/(self.x[1]-self.x[0])
        Fmax=Fs/2
        N=self.x.__len__()

        # feq represents fft figure's x axis
        feq=np.linspace(0,Fmax,N/2+1)

        return (feq,np.abs(fft_sig))





class AutoCorelation:

    def __init__(self,y):
        self.y=y


    def autocorr(self):

        #remove the direct current component
        y=minusAverage(self.y)

        result=np.correlate(y,y,mode="full")

        #count from 0
        return result[result.size/2:]





if __name__=="__main__":


    vmdata=VMfile('../VMs.csv')
    (x,y)=vmdata.getData('"zq-wuliu-liping-5.80"')
    plt.subplot(311)
    plt.plot(x,y)
    plt.xlabel("Hour")
    plt.ylabel("Intensity")
    plt.title("CPU Utility")

    fft=FFT(x,y)
    (x1,y1)=fft.computeFFT()
    plt.subplot(312)
    plt.plot(x1,y1)
    plt.xlabel("Hz")
    plt.ylabel("Intensity")
    plt.title("FFT")

    auto=AutoCorelation(y)
    x2=doubleList(range(0,auto.autocorr().__len__()))
    plt.subplot(313)
    plt.plot(x2,auto.autocorr())
    plt.xlabel("Lag(Hour)")
    plt.ylabel("Corelation")
    plt.title("Auto-Corelation")

    plt.show()
    #ax.xlable("1")
    #vmdata.plot(x,y)
    #fft=FFT(x,y)
    #(x1,y1)=fft.computeFFT()
    #fft.plot(x1,y1)
    #auto=AutoCorelation(y)
    #x_axis=doubleList(range(0,auto.autocorr().__len__()))
    #plt.figure()
    #plt.plot(x_axis,auto.autocorr())
    #plt.show()


