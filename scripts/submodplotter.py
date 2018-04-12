#!/usr/bin/env python3
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import matplotlib.mlab as mlab
import numpy as np
import time
import sys
import pickle
import cPickle

class PerformanceData():
    def __init__(self,filename,name,marker):
        self.greed,self.ratio=self._parse(filename)
        self.name=name
        self.marker=marker

    def _parse(self,filename):
        f = open(filename, 'r')
        t=pickle.load(f)
        avg=pickle.load(f)
        var=pickle.load(f)
        lower_bounds=pickle.load(f)
        upper_bounds=pickle.load(f)
        greed=pickle.load(f)
        ratio=pickle.load(f)

        return greed,ratio


def main():
    data_list=[]
    #data_list.append(PerformanceData("DDRP","DDRP",'-o'))
    #data_list.append(PerformanceData("DDRP-OO","DDRP-OO",'-D'))
    ##data_list.append(PerformanceData("DDRP-OO2","DDRP-OO2"))
    #data_list.append(PerformanceData("MCTS","MCTS",'-s'))
    data_list.append(PerformanceData("testingsubmodularityratio","testingsubmodularityratio",'-3'))
    #data_list.append(PerformanceData("TEST2","TEST2",'-3'))
    #data_list.append(PerformanceData("MCTS2","MCTS2",'-s'))
    #data_list.append(PerformanceData("DDRPTest","DDRPTest",'-s'))
    # ddrp=PerformanceData("ddrp",'DDRP')

    plt.figure(figsize=(8,6))
    #plt.xlim((-.03,.53))
    #plt.ylim((0,11))
    #plt.xlim((-.03,1))
    plt.xlabel('Greedy performance / Optimal performance')
    plt.ylabel('%')
    plt.title('Greedy approach PDF',fontsize=16)
    mu = .75 # mean of distribution
    sigma = .1 # standard deviation of distribution
    num_bins = 20
    weights=np.ones_like(data_list[0].greed)/float(len(data_list[0].greed))
    n, bins, patches = plt.hist(data_list[0].greed, num_bins, facecolor='green', alpha=0.5, weights=weights)
    # add a 'best fit' line
    # for d in data_list:
    #     for v in range(len(d.greed)):
    #         plt.plot(d.ratio[v],d.greed[v],'x')

    plt.show()



if __name__ == '__main__':
    main()
