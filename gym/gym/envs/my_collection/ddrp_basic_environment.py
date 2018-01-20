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

class ddrpBasicEnv(gym.Env):
    def __init__(self):
        self.size=4
        self.objectives_size=1
        self.action_space = spaces.Discrete(self.size*self.size*self.objectives_size)
        self.observation_space = spaces.Discrete(2**(self.size**2)*(self.size**2))
        self._seed()
        self.viewer = None
        self.state = None
        self.position=None
        self.max_steps=self.size**2
        self.steps=0


    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        x=action//self.size
        y=action%self.size
        self.steps+=abs(self.position[0]-x)+abs(self.position[1]-y)
        self.state[self.position[0]][self.position[1]][-1]=0
        self.position=(x,y)
        self.state[self.position[0]][self.position[1]][-1]=1
        reward=int(self.state[x][y][0])
        self.state[x][y][0]=0
        if self.steps > self.max_steps:
            done=True
        else:
            done=False

        return binaryToNum(self.state,self.position,self.size), reward, done, {}

    def _reset(self):
        self.done=False
        self.state = self.np_random.randint(2, size=(self.size,self.size,self.objectives_size+1))
        self.position=(randInt(0,self.size-1),randInt(0,self.size-1))
        for i in range(self.size):
            for j in range(self.size):
                if i==self.position[0] and j==self.position[1]:
                    self.state[i][j][-1]=1
                else:
                    self.state[i][j][-1]=0


        self.steps=0
        return binaryToNum(self.state,self.position,self.size)
