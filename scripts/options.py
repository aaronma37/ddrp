#!/usr/bin/env python3
import os, logging, gym
import ddrp_options
import sub_test
import numpy as np
from ddrp import DDRP
from mcts import MCTS 
import matplotlib.pyplot as plt
import time
import sys
import pickle
import cPickle

NUM_OBJ=1
NUM_ITER=10
MODEL_NAME='testingsubmodularityratio2'
MODEL_TYPE='ddrp'
SUBMOD=True
ITER_OPTION='time'
ENV_TYPE='tiny'

def progressBar(value, endvalue, bar_length=60):

    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def train(env_id,num_iterations,num_obj,filename,model,iter_option):

    submodularity_solver=sub_test.Solver()
    results=[]
    dr=[]
    avg=[]
    var=[]
    t=[]
    lower_bounds=[]
    upper_bounds=[]
    greed=[]
    eta=[]
    if MODEL_TYPE=='ddrp-oo':
        print "loading data"
        with open('saved_values') as fp:
            values=pickle.load(fp)
        print "finished loading"

    think_times=[.01,.05,.1,.5,1,5,10]
    think_times=[.01,.2,.4,.6,.8,1,1.5,2,2.5,3,3.5,4,4.5,5]
    think_times=[.001,.01,.02,.03,.04,.1,.2,.3,.4,.5]
    think_times=[.001,.01,.02,.03,.04,.1,.2,.3,.4,.5]
    think_times=[.0001,.000699,.001,.00699,.01,.0699,.1,.699]
    think_times=[10**(-4),10**(-3.5),10**(-3),10**(-2.5),10**(-2),10**(-1.5),10**(-1),10**(-.5),10**(0),10**(.5)]
    #think_times=[10**(1),10**(1.5)]
    #think_times=[10**(2),10**(2.5)]
    #think_times=[x / 10.0 for x in range(1, 30, 5)]
    if SUBMOD:
        think_times=[10**(0)]

    for think_steps in reversed(think_times):
        results.append([])
        dr.append([])
        completion_progress=0
        print "progress <"
        for trial in range(num_iterations):
            progressBar(trial,num_iterations)

            env=ddrp_options.ddrpOptionsEnv(num_obj,ENV_TYPE)
            env._reset()
            if model == "ddrp":
                ddrp=DDRP(env,ENV_TYPE)
            elif model == "ddrp-oo":
                ddrp=DDRP(env,ENV_TYPE)
                ddrp.import_values(values)
            elif model == "mcts":
                ddrp=MCTS(env)
            elif model == "train":
                ddrp=DDRP(env,ENV_TYPE)
                ddrp.import_values(values)

            if iter_option=="time":
                start=time.time()
                while time.time()-start < think_steps:
                    ddrp.step()
            elif iter_option=="steps":
                steps=0
                while steps < think_steps*1000:
                    ddrp.step()
                    steps+=1
            if SUBMOD:
                greed.append(ddrp.first_step())
                #eta.append(1)
                eta.append(submodularity_solver.test_once(env,.05,ddrp.max_sub_env_length,ddrp.discount))
            r,v=ddrp.evaluate()
            dr[-1].append(v)
            results[-1].append(r)
            #ddrp.completed_node_tree.printValues()
            #if model == "ddrp-oo":
                #values=ddrp.values
                #ddrp=None
            if model == "train":
                values=ddrp.values

        results[-1].sort()
        performance=[]
        for g in range(len(dr[-1])):
            performance.append(greed[g]/dr[-1][g])

        avg.append(sum(results[-1])/len(results[-1]))
        var.append(np.var(results[-1]))
        t.append(think_steps)
        lower_bounds.append(avg[-1]-results[-1][int(.1*num_iterations)])
        upper_bounds.append(results[-1][int(.9*num_iterations)]-avg[-1])
        print 'think time: ', think_steps, ' avg: ',sum(results[-1])/len(results[-1]), 'var: ', var[-1], 'results: ', dr[-1]

    with open(filename,'wb') as fp:
        pickle.dump(t,fp)
        pickle.dump(avg,fp)
        pickle.dump(var,fp)
        pickle.dump(lower_bounds,fp)
        pickle.dump(upper_bounds,fp)
        print greed
        print dr[-1]
        print "performance", performance
        print eta
        pickle.dump(performance,fp)
        pickle.dump(eta,fp)

    if model == "train":
        ddrp.save()

def main():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', help='environment ID', default='ddrp_options-v0')
    parser.add_argument('--seed', help='RNG seed', type=int, default=0)
    parser.add_argument('--num-timesteps', type=int, default=int(10e6))
    args = parser.parse_args()


    train(args.env,NUM_ITER,NUM_OBJ,MODEL_NAME,MODEL_TYPE,ITER_OPTION)



if __name__ == '__main__':
    main()
