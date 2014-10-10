__author__ = 'pike'


import numpy as np
import matplotlib.pyplot as plt
from FileUtil import VMFile
import math

def minusAverage(list):
    result = list[:]
    average = sum(result) / result.__len__()
    for i in range(0, result.__len__()):
        result[i] -= average
    return result

def doubleList(list):
    result = list[:]
    for i in range(0, result.__len__()):
        result[i] = 2 * result[i]
    return result

def even(num):
    if (math.ceil(num) % 2 == 0):
        return math.ceil(num)
    else:
        if (math.floor(num) % 2 == 0):
            return math.floor(num)
        else:
            return math.floor(num) + 1

class FFT:

    def __init__(self, x, y):
        self.x = x[:]
        self.y = y[:]


    #compute fft will return (x,y) represent frequency and intensity
    def computeFFT(self):
        if (self.x.__len__() < 2):
            return None

        #remove the direct current component
        fft_sig = np.fft.rfft(minusAverage(self.y))

        #Fs : sample frequency ; Fmax : wave's bandwidth ; N : total sampling number
        Fs = 1.0 / (self.x[1] - self.x[0])
        Fmax = Fs / 2
        N = self.x.__len__()

        # feq represents fft figure's x axis
        feq = np.linspace(0, Fmax, N / 2 + 1)

        return (feq, np.abs(fft_sig))


class AutoCorrelation:

    def __init__(self, y):
        self.y = y[:]


    def autocorr(self):

        #remove the direct current component
        y = minusAverage(self.y)

        autoValue = np.correlate(y, y, mode="full")

        #count from 0
        resultY = autoValue[autoValue.size / 2 :]
        resultX = doubleList(range(0, resultY.__len__()))

        return (resultX, resultY)



if __name__=="__main__":


    vmdata = VMFile('../Resource/VMs.csv')
    (x,y) = vmdata.getData('"zq-wuliu-liping-5.80"')
    plt.subplot(311)
    plt.plot(x, y)
    plt.xlabel("Hour")
    plt.ylabel("Intensity")
    plt.title("CPU Utility")

    fft = FFT(x, y)
    (x1,y1) = fft.computeFFT()
    plt.subplot(312)
    plt.plot(x1, y1)
    plt.xlabel("Hz")
    plt.ylabel("Intensity")
    plt.title("FFT")

    auto = AutoCorrelation(y)
    (x2, y2) = auto.autocorr()
    plt.subplot(313)
    plt.plot(x2, y2)
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


