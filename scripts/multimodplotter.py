#!/usr/bin/env python3
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import matplotlib.mlab as mlab
import numpy as np
import time
import sys
import pickle
import cPickle


def main():

    f = open('multi', 'r')
    ratio=pickle.load(f)

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
    weights=np.ones_like(ratio)/float(len(ratio))
    n, bins, patches = plt.hist(ratio, num_bins, facecolor='green', alpha=0.5, weights=weights)
    # add a 'best fit' line
    # for d in data_list:
    #     for v in range(len(d.greed)):
    #         plt.plot(d.ratio[v],d.greed[v],'x')

    plt.show()



if __name__ == '__main__':
    main()
