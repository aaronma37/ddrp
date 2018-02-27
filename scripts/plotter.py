#!/usr/bin/env python3
import matplotlib.pyplot as plt
import time
import sys
import pickle
import cPickle

class PerformanceData():
    def __init__(self,filename,name,marker):
        self.t,self.avg,self.var=self._parse(filename)
        self.name=name
        self.marker=marker

    def _parse(self,filename):
        f = open(filename, 'r')
        t=pickle.load(f)
        #t = [x * 10 for x in t] 
        avg=pickle.load(f)
        var=pickle.load(f)
        return t,avg,var


def main():
    data_list=[]
    data_list.append(PerformanceData("DDRP","DDRP",'-o'))
    data_list.append(PerformanceData("DDRP-OO","DDRP-OO",'-D'))
    #data_list.append(PerformanceData("DDRP-OO2","DDRP-OO2"))
    data_list.append(PerformanceData("MCTS","MCTS",'-s'))
    #data_list.append(PerformanceData("MCTS2","MCTS2",'-s'))
    #data_list.append(PerformanceData("DDRPTest","DDRPTest",'-s'))
    # ddrp=PerformanceData("ddrp",'DDRP')

    plt.figure(figsize=(8,6))
    #plt.xlim((-.03,.53))
    #plt.ylim((0,11))
    #plt.xlim((-.03,1))
    plt.ylim((0,11))
    plt.ylabel('Episode reward',fontsize=20)
    plt.xlabel('Think time (s)',fontsize=20)
    plt.xscale('log',basex=10)
    #plt.title('Online algorithm performance',fontsize=16)
    for d in data_list:
        plt.errorbar(d.t,d.avg, yerr=d.var,label=d.name, fmt=d.marker,markersize=8,elinewidth=1)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=0.,prop={'size':15},frameon=False)
    plt.show()



if __name__ == '__main__':
    main()
