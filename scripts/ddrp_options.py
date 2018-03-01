import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from random import randint as randInt

def dist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

class Objective():
    def __init__(self,name,r):
        self.name=name
        self.reward=r
        self.objectives=[]

class Region():
    def __init__(self,objective_set):
        self.state={}
        self.objectives={}
        for k,v in objective_set.items():
            self.objectives[k]=[]
            self.state[k]=None

    def calculateState(self):
        for o_name,v in self.objectives.items():
            self.state[o_name]=len(v)

    def getClosest(self,loc,objective_name):
        closest=None
        closest_obj=None
        for o in self.objectives[objective_name]:
            if closest is None:
                closest = dist(o,loc)
                closest_obj = o
            elif closest > dist(o,loc): 
                closest = dist(o,loc)
                closest_obj = o

        if closest_obj is None:
            print(self.state, "none found, shouldnt be here")
            return None,False
        self.objectives[objective_name].remove(closest_obj)
        self.calculateState()
        return closest_obj,True

class ddrpOptionsEnv():
    def __init__(self,num_obj):
        self.summary=''
        self.size=100
        self.possible_actions=None
        self.region={}
        self.region_size=10
        self.objectives={}
        for i in range(1,num_obj+1):
            if i==1:
                self.objectives[i]=Objective(str(i),1)
            else:
                self.objectives[i]=Objective(str(i),0)
            # self.objectives[i]=Objective(str(i),i/float(num_obj))
        self.reg_len=int(self.size/self.region_size)
        self.action_space = spaces.Discrete((int(self.size/self.region_size))**2*len(self.objectives))
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

    def regionToDiscrete(self,r):
        return r[0]*self.region_size+r[1]

    def get_action_meanings(self):
        return self.action_meaning

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _getRegionfromGlobal(self,oneDloc):
        x,y=self._getGlobal(oneDloc)
        return (x//self.reg_len,y//self.reg_len)

    def _getRegion(self,oneDloc):
        return (oneDloc//self.reg_len,oneDloc%self.reg_len)
    
    def _getGlobal(self,oneDloc):
        return (oneDloc//self.size, oneDloc%self.size)

    def step_ddrp(self, action):
        x=action[0]
        y=action[1]
        objective_type=action[2]
        self.summary+=':'+str(int(x))+','+str(int(y))+'v'+str(self.state[x][y][0]) + '@' + str(self.region_position[0]) + ',' + str(self.region_position[1])+ " steps: " + str(self.steps)
        if int(self.state[x][y][objective_type]) is 0:
            self.steps+=100
            if self.steps > self.max_steps:
                done=True
            else:
                done=False
            return self.state, 0, done, {}
        o,got_reward = self.region[(x,y)].getClosest(self.position,objective_type)
        if got_reward is True:
            r=self.objectives[objective_type].reward
        else:
            r=0

        if o is None:
            print(self.state[x][y][0], "error")

        self.steps+=dist(self.position,o)
        self.state[x][y][objective_type]=self.region[(x,y)].state[objective_type]
        self.state[self.region_position[0]][self.region_position[1]][0]=0
        self.position=(o[0],o[1])
        self.region_position=(x,y)
        self.state[x][y][0]=1
        reward=r
        self.r_sum+=reward
        if self.steps > self.max_steps:
            #print("SUMMARY")
            #print(self.summary)
            done=True
            return self.state, 0, done, self.summary
        else:
            done=False
            return self.state, float(reward), done, self.summary

    #def step(self, action):
    #    assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
    #    x,y=self._getRegion(action)
    #    self.summary+=':'+str(int(x))+','+str(int(y))+'v'+str(self.state[x][y][0]) + '@' + str(self.region_position[0]) + ',' + str(self.region_position[1])
    #    if int(self.state[x][y][0]) is 0:
    #        self.steps+=100
    #        if self.steps > self.max_steps:
    #            done=True
    #        else:
    #            done=False
    #        return self.state, 0, done, {}
    #    o,r = self.region[(x,y)].getClosest(self.position)
    #    if o is None:
    #        print(self.state[x][y][0], "error")

    #    self.steps+=dist(self.position,o)
    #    self.state[x][y][0]=self.region[(x,y)].state
    #    self.state[self.region_position[0]][self.region_position[1]][1]=0
    #    self.position=(o[0],o[1])
    #    self.region_position=(x,y)
    #    self.state[x][y][1]=1
    #    reward=r
    #    self.r_sum+=reward
    #    if self.steps > self.max_steps:
    #        #print("SUMMARY")
    #        #print(self.summary)
    #        done=True
    #        return self.state, 0, done, {}
    #    else:
    #        done=False
    #        return self.state, float(reward), done, self.summary

    def getCopy(self):
        copy=ddrpOptionsEnv(len(self.objectives))
        copy.summary=''
        copy.done=False
        copy.state = np.zeros((int(copy.size/copy.region_size),int(copy.size/copy.region_size),len(self.objectives)+1),dtype=np.int8)
        copy.region={}

        for k,a in self.region.items():
            copy.region[k]=Region(self.objectives)
            for o_name,v in a.objectives.items():
                for o in self.region[k].objectives[o_name]:
                    copy.region[k].objectives[o_name].append(o)

        for r in copy.region.values():
            r.calculateState()

        #copy.position=(randInt(0,self.size-1),randInt(0,self.size-1))
        copy.position=(0,0)
        copy.region_position=(copy.position[0]//copy.region_size,copy.position[1]//copy.region_size)
        copy.state[copy.region_position[0]][copy.region_position[1]][0]=1

        for i in range(int(copy.size/copy.region_size)):
            for j in range(int(copy.size/copy.region_size)):
                for k,v in self.objectives.items():
                    copy.state[i][j][k]=copy.region[(i,j)].state[k]

        copy.steps=0
        copy.r_sum=0
        copy.possible_actions=[]
        for r,v in copy.region.items():
            for k,o in self.objectives.items():
                copy.possible_actions.append((r,k))
        return copy

    def _reset(self):
        self.summary=''
        self.done=False
        self.state = np.zeros((int(self.size/self.region_size),int(self.size/self.region_size),len(self.objectives)+1),dtype=np.int8)
        self.region={}
        for i in range(int(self.size/self.region_size)):
            for j in range(int(self.size/self.region_size)):
                self.region[(i,j)]=Region(self.objectives)

        for j in range(len(self.objectives)):
            for i in range(100):
                self.objectives[randInt(1,len(self.objectives))].objectives.append(randInt(0,self.size**2-1))

        for k,v in self.objectives.items():
            for o in v.objectives:
                self.region[self._getRegionfromGlobal(o)].objectives[k].append(self._getGlobal(o))


        for r in self.region.values():
            r.calculateState()

        #self.position=(randInt(0,self.size-1),randInt(0,self.size-1))
        self.position=(0,0)
        self.region_position=(self.position[0]//self.region_size,self.position[1]//self.region_size)
        self.state[self.region_position[0]][self.region_position[1]][0]=1

        for i in range(int(self.size/self.region_size)):
            for j in range(int(self.size/self.region_size)):
                for k,v in self.objectives.items():
                    self.state[i][j][k]=self.region[(i,j)].state[k]

        self.steps=0
        self.r_sum=0

        self.possible_actions=[]
        for r,v in self.region.items():
            for k,v in self.objectives.items():
                self.possible_actions.append((r,k))
        return self.state

    def getObs(self):
        return self.state
