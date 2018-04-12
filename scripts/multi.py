from random import randint
import itertools
from sets import Set
import pickle
from random import random
#reward(trajectory)=
#steps=0


#Construct set of all trajectories
#  Pick local max
#  re-evaluate environment
#Calculate total reward

#Construct set of all combinations of trajectories
#  find max
#local/optimal

gamma=.8
class Env():
    def __init__(self):
        self.size=5
        self.state={}
        self.rewards={}
        self.num=0
        self.reseed()
        while self.num>5 or self.num <4:
            self.reseed()
        self.starting_location=(0,0)

    def reseed(self):
        self.num=0
        for i in range(self.size):
            for j in range(self.size):
                if random()>.9:
                    self.state[(i,j)]=1
                    self.rewards[(i,j)]=0
                    self.num+=1
                else:
                    self.state[(i,j)]=0


    def makeCopy(self):
        copy=Env()
        copy.size=self.size
        copy.state={}
        copy.reward={}
        for i in range(self.size):
            for j in range(self.size):
                copy.state[(i,j)]=self.state[(i,j)]
                if self.state[(i,j)]==1:
                    copy.rewards[(i,j)]=self.rewards[(i,j)]
        copy.starting_location=self.starting_location
        return copy

    def dist(self,r1,r2):
        return abs(r1[0]-r2[0])+abs(r1[1]-r2[1])

    def recalculate(self,reward_dict):
        for reg,r in reward_dict.items():
            if r > self.rewards[reg]:
                self.rewards[reg]=r

    def evaluate(self):
        total_r = 0
        for r in self.rewards.values():
            total_r+=r
        return total_r

    def get_reward(self,trajectory):
        r=0
        steps=0
        reg_0=self.starting_location
        reward_dict={}
        for reg in trajectory:
            steps+=self.dist(reg_0,reg)
            reg_0=reg
            if self.state[reg]*gamma**steps>self.rewards[reg]:
                r+=self.state[reg]*gamma**steps-self.rewards[reg]
                reward_dict[reg]=self.state[reg]*gamma**steps
        return r,reward_dict

def get_region_set(env):
    region_set=Set()
    for i in range(5):
        for j in range(5):
            if env.state[(i,j)]==1:
                region_set.add((i,j))
    if len(region_set)==0:
        print "error, no regions"
    return region_set

def get_trajectory_set(region_set,sub_env_length):
    l=list(itertools.permutations(region_set, sub_env_length))
    if len(l)==0:
        print "error, no trajectory list",len(region_set),sub_env_length
        for r in region_set:
            print r
        print list(itertools.permutations(region_set,sub_env_length))
    return l

def get_joint_trajectory_set(trajectory_set,num_agents):
    return list(itertools.combinations(trajectory_set,num_agents))


def greed_reward(env,trajectory_set,num_agents):
    env_copy=env.makeCopy()
    max_r_dict={}
    for a in range(num_agents):
        max_val=0
        for t in trajectory_set:
            v,r_dict=env_copy.get_reward(t)
            if v>max_val:
                max_val=v
                max_r_dict=r_dict
        env_copy.recalculate(max_r_dict)
    return env_copy.evaluate()

def max_reward(env,joint_trajectory_set):
    max_val=0
    for tlist in joint_trajectory_set:
        env_copy=env.makeCopy()
        for t in tlist:
            this_v,r_dict=env_copy.get_reward(t)
            env_copy.recalculate(r_dict)
        v=env_copy.evaluate()
        if v>max_val:
            max_val=v
    return max_val





def sim_once():
    _env=Env()
    sub_env_length=3
    num_agents=2
    region_set=get_region_set(_env)
    trajectory_set=get_trajectory_set(region_set,sub_env_length)
    joint_trajectory_set=get_joint_trajectory_set(trajectory_set,num_agents)
    greed=greed_reward(_env,trajectory_set,num_agents)
    max_r=max_reward(_env,joint_trajectory_set)
    print greed/max_r
    return greed/max_r

v=[]
for i in range(1000):
    v.append(sim_once())

with open('multi','wb') as fp:
    pickle.dump(v,fp)
