import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from random import randint as randInt

def dist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

class Region():
    def __init__(self):
        self.state=None
        self.objectives=[]
        self.objectives.append([])

    def calculateState(self):
        self.state=len(self.objectives[0])

    def getClosest(self,loc):
        closest=None
        closest_obj=None
        for o in self.objectives[0]:
            if closest is None:
                closest = dist(o,loc)
                closest_obj = o
            elif closest > dist(o,loc): 
                closest = dist(o,loc)
                closest_obj = o

        if closest_obj is None:
            print(self.state, "none found, shouldnt be here")
            return None,0
        self.objectives[0].remove(closest_obj)
        self.calculateState()
        return closest_obj,1

class ddrpOptionsEnv(gym.Env):
    def __init__(self):
        self.summary=''
        self.size=100
        self.region={}
        self.region_size=10
        self.objectives_size=1
        self.action_space = spaces.Discrete((int(self.size/self.region_size))**2*self.objectives_size)
        self.observation_space = spaces.Box(low=0, high=11, shape=(int(self.size/self.region_size),int(self.size/self.region_size),2))
        self.action_meaning={}
        for i in range((int(self.size/self.region_size))**2):
            self.action_meaning[i]=i
        self._seed()
        self.viewer = None
        self.state = None
        self.position=None
        self.max_steps=100
        self.timestep_limit=100#self.size**2
        self.steps=0
        self.r_sum=0

    def get_action_meanings(self):
        return self.action_meaning

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _getRegionfromGlobal(self,oneDloc):
        x,y=self._getGlobal(oneDloc)
        return (x//self.region_size,y//self.region_size)

    def _getRegion(self,oneDloc):
        return (oneDloc//self.region_size,oneDloc%self.region_size)
    
    def _getGlobal(self,oneDloc):
        return (oneDloc//self.size, oneDloc%self.size)


    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        x,y=self._getRegion(action)
        self.summary+=':'+str(int(x))+','+str(int(y))+'v'+str(self.state[x][y][0]) + '@' + str(self.region_position[0]) + ',' + str(self.region_position[1])
        if int(self.state[x][y][0]) is 0:
            self.steps+=100
            if self.steps > self.max_steps:
                done=True
                print("SUMMARY")
                print(self.summary)
            else:
                done=False
            return self.state, 0, done, {}
        o,r = self.region[(x,y)].getClosest(self.position)
        if o is None:
            print(self.state[x][y][0], "error")

        self.steps+=dist(self.position,o)
        self.state[x][y][0]=self.region[(x,y)].state
        self.state[self.region_position[0]][self.region_position[1]][1]=0
        self.position=(o[0],o[1])
        self.region_position=(x,y)
        self.state[x][y][1]=1
        reward=r
        self.r_sum+=reward
        if self.steps > self.max_steps:
            #print("SUMMARY")
            #print(self.summary)
            done=True
            return self.state, 0, done, {}
        else:
            done=False
            return self.state, float(reward), done, {}

    def getCopy(self):
        copy=ddrpOptionsEnvironment()
        copy.summary=''
        copy.done=False
        copy.state = np.zeros((int(self.size/self.region_size),int(self.size/self.region_size),2),dtype=np.int8)
        copy.region={}
        for i in range(int(self.size/self.region_size)):
            for j in range(int(self.size/self.region_size)):
                copy.region[(i,j)]=Region()
    #TODO

    def _reset(self):
        self.summary=''
        self.done=False
        self.state = np.zeros((int(self.size/self.region_size),int(self.size/self.region_size),2),dtype=np.int8)
        self.region={}
        for i in range(int(self.size/self.region_size)):
            for j in range(int(self.size/self.region_size)):
                self.region[(i,j)]=Region()

        for i in range(100):
            o=randInt(0,self.size**2-1)
            self.region[self._getRegionfromGlobal(o)].objectives[0].append(self._getGlobal(o))


        for r in self.region.values():
            r.calculateState()

        #self.position=(randInt(0,self.size-1),randInt(0,self.size-1))
        self.position=(0,0)
        self.region_position=(self.position[0]//self.region_size,self.position[1]//self.region_size)
        self.state[self.region_position[0]][self.region_position[1]][1]=1

        for i in range(int(self.size/self.region_size)):
            for j in range(int(self.size/self.region_size)):
                self.state[i][j][0]=self.region[(i,j)].state

        self.steps=0
        self.r_sum=0
        return self.state
