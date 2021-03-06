'''
Compare predicted series
v0.1 nov 2020
hdaniel@ualg.pt
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from hdlib.base import Base

class ComparePrediction(Base):
    __LABELACT   = "actual"
    __LABELPRED  = "prediction"
    __LABELX     = "value"
    __LABELY     = "time (steps)"
    __TITLECMP   = 'Predictions vs actual'
    __TITLENAIVE = 'Prediction skewed to check naive forecast'
    __LEGENDLOC  = "upper right"

    """Compares series prediction"""
    "It assumes a series are unidimensional numpy arrays"

    def __init__(self, actual:np.array, predict:np.array, horizon:int) -> None:
        """
        :param actual:  the actual series
        :param predict: the predicted series (of actual)
        :param horizon: horizon defines how many steps in the future is the first prediction
                        cannot be larger than series length
        :return:

        ?? BUT that is NOT what we want?!? we want to predict from now n future steps.... right?"
        horizon defines how many steps in future is the first prediction

        both series should have same length but
        predict should be skewed horizon points from actual, so:

        predict starts at point horizon (referring to actual)
        and will predict more horizon points after end of actual
        Eg.:
        If:
        actual = [0, 1, 2, 3, 4, 5, 6]
        horizon = 3
        then:
        predict = [3, 4, 5, 6, 7, 8, 9]
        """

        #force np.array 1D
        self.__actual  = np.array(actual).flatten()
        self.__predict = np.array(predict).flatten()
        self.__horizon = horizon
        self.__nsamples = self.__actual.shape[0]

        #series should have same length
        if self.__actual.shape != self.__predict.shape:
            raise RuntimeError('actual and predicted should have same length')

        #horizon must be in [0, __nsamples]
        if self.__horizon > self.__nsamples or self.__horizon < 0:
            raise RuntimeError('horizon must be in range: [0, series length]')



    def commonPoints(self) -> (np.array, np.array):
        """
        These views have horizon samples less than the originals: actual and predict

            Common points view:
            __actualCommon removes not predicted horizon samples from beginning of actual
            __predictCommon removes horizon predicted points from the end of predict

            This way if prediction is 100% accurate __actualCommon == __predictCommon

            Note: If predict is the same as actual (naive forecasting): actual == predict
        """
        return  (self.__actual[self.__horizon:], \
                 #self.__predict[:self.__nsamples-self.__horizon])
                 self.__predict[:-self.__horizon])
                 

 
    def plot(self, begin=0, end=-1, overlap=False, 
                   labelact=__LABELACT, labelpred=__LABELPRED,
                   labelx=__LABELX, labely=__LABELY,
                   title="", xtatitle=""):
        """
        Plot prediction against actual data

        :param overlap     if true, skew back prediction self.__horizon points
                           to overlap with actual data.
                           If matches it is naive forecasting
                           (prediction is equal to previous points)
        :param begin, end  range of point to predict

        :returns           figure and single axis, so that it can be saved or plotted
        """

        #set range
        if end == -1: end = self.__nsamples
        t0 = range(begin, end)

        #define overlap mode or normal
        if overlap:
            if title == "":
                title = 'Prediction skewed to check naive forecast'
            tp = range(begin, end)
        else:
            if title == "":
                title = 'Predictions vs actual'
            tp = range(begin+self.__horizon, end + self.__horizon)
        
        #Add extra text to title
        title += xtatitle


        #plot
        fig, axs = plt.subplots(1, constrained_layout=True)
        axs.plot(t0, self.__actual[begin:end], 'g', label=labelact)
        axs.plot(tp, self.__predict[begin:end], 'r', label=labelpred)
        axs.grid()

        #legend
        axs.set_title(title)
        axs.set_xlabel(labely)
        axs.set_ylabel(labelx)
        axs.legend(loc=ComparePrediction.__LEGENDLOC) #or: self.__LEGENDLOC
        return fig, axs

                 
