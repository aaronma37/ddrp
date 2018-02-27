#!/usr/bin/env python3
import os, logging, gym
import ddrp_options
import numpy as np
from ddrp import DDRP
from mcts import MCTS 
import matplotlib.pyplot as plt
import time
import sys
import pickle
import cPickle

def train(env_id,filename,model, num_timesteps, seed, num_cpu,IMPORT_OPTION,ITER_OPTION):

    results=[]
    avg=[]
    var=[]
    t=[]
    values=None

    think_times=[.01,.05,.1,.5,1,5,10]
    think_times=[.01,.2,.4,.6,.8,1,1.5,2,2.5,3,3.5,4,4.5,5]
    think_times=[.001,.01,.02,.03,.04,.1,.2,.3,.4,.5]
    think_times=[.001,.01,.02,.03,.04,.1,.2,.3,.4,.5]
    think_times=[.0001,.000699,.001,.00699,.01,.0699,.1,.699]
    think_times=[10**(-4),10**(-3.5),10**(-3),10**(-2.5),10**(-2),10**(-1.5),10**(-1),10**(-.5),10**(0),10**(.5)]
    #think_times=[10**(1),10**(1.5)]
    #think_times=[10**(2),10**(2.5)]
    #think_times=[x / 10.0 for x in range(1, 30, 5)]

    for think_steps in reversed(think_times):
        results.append([])
        for trial in range(100):
            env=ddrp_options.ddrpOptionsEnv()
            env._reset()
            if model == "ddrp":
                ddrp=DDRP(env)
            elif model == "mcts":
                ddrp=MCTS(env)

            if IMPORT_OPTION is True:
                ddrp.import_values(values)
            if ITER_OPTION=="time":
                start=time.time()
                while time.time()-start < think_steps:
                    ddrp.step()
            if ITER_OPTION=="steps":
                steps=0
                while steps < think_steps*1000:
                    ddrp.step()
                    steps+=1
            results[-1].append(ddrp.evaluate())
            #ddrp.completed_node_tree.printValues()
            if IMPORT_OPTION is True:
                values=ddrp.values
                ddrp=None
        avg.append(sum(results[-1])/len(results[-1]))
        var.append(np.var(results[-1]))
        t.append(think_steps)
        print 'think time: ', think_steps, ' avg: ',sum(results[-1])/len(results[-1]), 'var: ', var[-1], 'results: ', results[-1]

    with open(filename,'wb') as fp:
        pickle.dump(t,fp)
        pickle.dump(avg,fp)
        pickle.dump(var,fp)

def main():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', help='environment ID', default='ddrp_options-v0')
    parser.add_argument('--seed', help='RNG seed', type=int, default=0)
    parser.add_argument('--num-timesteps', type=int, default=int(10e6))
    args = parser.parse_args()

    plt.figure()

    # train(args.env,"DDRP", num_timesteps=args.num_timesteps, seed=args.seed, num_cpu=14,IMPORT_OPTION=False,ITER_OPTION="steps")

    train(args.env,"DDRP","ddrp", num_timesteps=args.num_timesteps, seed=args.seed, num_cpu=14,IMPORT_OPTION=False,ITER_OPTION="time")
    # t2,avg2,var2=train(args.env, num_timesteps=args.num_timesteps, seed=args.seed, num_cpu=14,IMPORT_OPTION=True,ITER_OPTION="steps")




if __name__ == '__main__':
    main()
