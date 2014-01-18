__author__ = 'pike'


import matplotlib.pyplot as plt

class Plot:

    @staticmethod
    def plot(x,y,title,xlable,ylable):
        plt.figure(title)
        plt.plot(x,y)
        plt.title(title)
        plt.ylabel(ylable)
        plt.xlabel(xlable)
        plt.show()