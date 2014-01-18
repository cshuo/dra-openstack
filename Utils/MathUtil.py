__author__ = 'pike'


import numpy as np
import matplotlib.pyplot as plt
from FileUtil import VMfile
from PlotUtil import Plot

def minusAverage(list):
    average=sum(list)/list.__len__()
    for i in range(0,list.__len__()):
        list[i]-=average
    return list

class FFT:

    def __init__(self,x,y):
        self.x=x
        self.y=y


    #compute fft will return (x,y) represent frequency and intensity
    def computeFFT(self):

        #fft_sig=np.fft.rfft(self.y)
        #remove the direct current component
        fft_sig=np.fft.rfft(minusAverage(self.y))
        print np.abs(fft_sig)

        #Fs : sample frequency ; Fmax : wave's bandwidth ; N : total sampling number
        Fs=1.0/(self.x[1]-self.x[0])
        Fmax=Fs/2
        N=self.x.__len__()
        print Fs,Fmax,N
        # feq represents fft figure's x axis
        feq=np.linspace(0,Fmax,N/2+1)
        print feq
        return (feq,np.abs(fft_sig))

    def plot(self,x,y):

        Plot.plot(x,y,"fft","Hz","Intensity")



class AutoCorelation:
    def __init__(self,x):
        self.x=minusAverage(x)

    def autocorr(self):
        result=np.correlate(self.x,self.x,mode="full")
        return result[result.size/2:]




if __name__=="__main__":


    vmdata=VMfile()
    (x,y)=vmdata.getData('../VMs.csv')
    #vmdata.plot(x,y)
    #fft=FFT(x,y)
    #(x1,y1)=fft.computeFFT()
    #fft.plot(x1,y1)
    auto=AutoCorelation(y)
    print auto.autocorr()
    plt.figure()
    plt.plot(auto.autocorr())
    plt.show()

