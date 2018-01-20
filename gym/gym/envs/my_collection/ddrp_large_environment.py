import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from random import randint as randInt

def binaryToNum(state,position,size):
    binary_str=''
    for i in range(size):
        for j in range(size):
            binary_str+=str(state[i][j][0])
    return (position[0]*size+position[1])*2**(size**2)+int(binary_str,2)

class ddrpLargeEnv(gym.Env):
    def __init__(self):
        self.size=20
        self.objectives_size=1
        self.action_space = spaces.Discrete(self.size*self.size*self.objectives_size)
        self.observation_space = spaces.Box(low=0, high=11, shape=(self.size,self.size,1))
        self.action_meaning={}
        for i in range(self.size**2):
            self.action_meaning[i]=i
        self._seed()
        self.viewer = None
        self.state = None
        self.position=None
        self.max_steps=self.size**2
        self.timestep_limit=9#self.size**2
        self.steps=0
        self.r_sum=0

    def get_action_meanings(self):
        return self.action_meaning

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        x=action//self.size
        y=action%self.size
        self.steps+=abs(self.position[0]-x)+abs(self.position[1]-y)
        self.state[self.position[0]][self.position[1]][0]-=10
        self.position=(x,y)
        self.state[self.position[0]][self.position[1]][0]+=10
        reward=int(self.state[x][y][0])-10
        self.r_sum+=reward
        self.state[x][y][0]=10
        if self.steps > self.max_steps:
            done=True
            return self.state, 0, done, {}
        else:
            done=False
            return self.state, float(reward), done, {}



    def _reset(self):
        self.done=False
        self.state = np.zeros((self.size,self.size,1),dtype=np.int8)
        objectives=[]
        for i in range(self.size):
            objectives.append((randInt(0,self.size-1),randInt(0,self.size-1)))

        for o in objectives:
            self.state[o[0]][o[1]][0]+=1

        self.position=(randInt(0,self.size-1),randInt(0,self.size-1))
        self.state[self.position[0]][self.position[1]]+=10
        self.steps=0
        self.r_sum=0
        return self.state

