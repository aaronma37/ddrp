#!/usr/bin/env python3
import os, logging, gym
import ddrp_options
from ddrp import DDRP
import matplotlib.pyplot as plt

def train(env_id, num_timesteps, seed, num_cpu):


    results=[]
    avg=[]
    t=[]

    for think_steps in range(1,1000,75):
        results.append([])
        for trial in range(7): 
            env=ddrp_options.ddrpOptionsEnv()
            env._reset()
            ddrp=DDRP(env)
            for i in range(think_steps):
                ddrp.step()
            results[-1].append(ddrp.evaluate())
        avg.append(sum(results[-1])/len(results[-1]))
        t.append(think_steps)
        print 'think time: ', think_steps, ' avg: ',sum(results[-1])/len(results[-1])

    plt.plot(t,avg)
    plt.ylabel('Average episode reward')
    plt.xlabel('# think steps')
    plt.title('DDRP on gym environment')
    plt.show()

def main():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', help='environment ID', default='ddrp_options-v0')
    parser.add_argument('--seed', help='RNG seed', type=int, default=0)
    parser.add_argument('--num-timesteps', type=int, default=int(10e6))
    args = parser.parse_args()
    train(args.env, num_timesteps=args.num_timesteps, seed=args.seed, num_cpu=14)


if __name__ == '__main__':
    main()
