#!/usr/bin/env python3
import os, logging, gym
import ddrp_options_large as ddrp_options
import numpy as np
from ddrp import DDRP
import matplotlib.pyplot as plt
import time

def train(env_id, num_timesteps, seed, num_cpu):


    results=[]
    avg=[]
    var=[]
    t=[]

    think_times=[.01,.05,.1,.5,1,5,10]
    think_times=[.01,.2,.4,.6,.8,1,1.5,2,2.5,3,3.5,4,4.5,5]
    think_times=[.01,.1,.2,.3,.4,.5,.6]
    #think_times=[x / 10.0 for x in range(1, 30, 5)]

    for think_steps in think_times:
        results.append([])
        for trial in range(5): 
            env=ddrp_options.ddrpOptionsEnv()
            env._reset()
            ddrp=DDRP(env)
            start=time.time()
            while time.time()-start < think_steps:
                ddrp.step()
            results[-1].append(ddrp.evaluate())
        avg.append(sum(results[-1])/len(results[-1]))
        var.append(np.var(results[-1]))
        t.append(think_steps)
        print 'think time: ', think_steps, ' avg: ',sum(results[-1])/len(results[-1]), 'var: ', var[-1], 'results: ', results[-1]

    plt.figure()
    #plt.xscale('symlog')
    plt.errorbar(t,avg, yerr=var, fmt='-o')
    plt.ylabel('Episode reward')
    plt.xlabel('Think time (s)')
    plt.title('DDRP on 2D env')
    plt.show()

def main():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', help='environment ID', default='ddrp_options_largke-v0')
    parser.add_argument('--seed', help='RNG seed', type=int, default=0)
    parser.add_argument('--num-timesteps', type=int, default=int(10e6))
    args = parser.parse_args()
    train(args.env, num_timesteps=args.num_timesteps, seed=args.seed, num_cpu=14)


if __name__ == '__main__':
    main()
