from random import randint
import ddrp_options
import itertools
import math
from sets import Set
import matplotlib.pyplot as plt

gamma=.9

def getReward(L,env,discount):
    time=0
    reward=0
    loc=env.region_position
    for l in L:
        o,r,done,info=env.step_ddrp((l[0],l[1],1))
        loc=l
        reward+=r*discount**env.steps
    return reward

def getValue(C,env,discount):
    max_reward=0.
    perm_list = list(itertools.permutations(C)) 
    for c in perm_list:
        temp_env=env.getCopy()
        r=getReward(c,temp_env,discount)
        if r > max_reward:
            max_reward=r
    return max_reward

def getIndividualSum(A,B,base,env,discount):
    max_sum=0
    for b in B:
        C=Set()
        C.add(b)
        max_sum+=getValue(A|C,env,discount)-base
    return max_sum

def getJointValue(A,B,base,env,discount):
    return getValue(A|B,env,discount)-base

def getRatio(A,B,env,discount):
    base = getValue(A,env,discount)
    I=getIndividualSum(A,B,base,env,discount)
    J=getJointValue(A,B,base,env,discount)
    # print "Individual: ", I, "Joint: ", J
    if J ==0:
        return 1
    return I/J
    try:
        ratio = (base-getIndividualSum(A,B,env,discount))/(base-getJointValue(A,B,env,discount))
    except ZeroDivisionError:
        ratio = 1
    return ratio 

def generateRandomLocSet(k,size):
    a_size=randint(0,k)
    b_size=k=a_size
    A=Set()
    B=Set()
    while len(A) < a_size:
        A.add((randint(0,size-1),(randint(0,size-1))))
    while len(B) < b_size:
        B.add((randint(0,size-1),(randint(0,size-1))))
    return A,B


class Environment():
    def __init__(self):
        self.occupancy={}
        self.initial_position=()
        self.size=3
        self.region_size=10
        for i in range(self.size):
            for j in range(self.size):
                self.occupancy[(i,j)]=randint(0, 1)

    def import_(self,env_ddrp):
        self.size=int(env_ddrp.size/env_ddrp.region_size)
        print self.size
        self.region_size=env_ddrp.region_size
        for i in range(int(env_ddrp.size/env_ddrp.region_size)):
            for j in range(int(env_ddrp.size/env_ddrp.region_size)):
                self.occupancy[(i,j)]=env_ddrp.state[i][j][1]
                print self.occupancy[(i,j)]
        self.initial_position=env_ddrp.region_position

    def getReward(self,last_loc,loc):
        reward=self.occupancy[loc]
        self.occupancy[loc]=0
        return reward,math.sqrt((self.region_size*(last_loc[0]-loc[0]))**2+(self.region_size*(last_loc[1]-loc[1]))**2)

    def getClone(self):
        clone = Environment()
        for i in range(self.size):
            for j in range(self.size):
                clone.occupancy[(i,j)]=self.occupancy[(i,j)]
        clone.initial_position=self.initial_position
        return clone


class Solver():
    def __init__(self):
        self.beta=.01
        self.env=Environment()
        self.K=5
        self.num=0
        self.eta=[]
        self.gamma=1
        self.g_e=[]
        self.n_e=[]
        for i in range(99):
            self.eta.append((99-i)/100.)

    def import_env(self,env):
        self.env.import_(env)

    def test_once(self,env, eta,k,discount):
        self.num=0
        gamma=1
        req_num=2./eta*(math.log(1./self.beta)+1.)
        while self.num < req_num:
            self.num+=1
            A,B=generateRandomLocSet(k,5)
            ratio = getRatio(A,B,env,discount)
            if ratio < gamma:
                self.gamma=ratio
            print "%: ", self.num/req_num*100., " ratio: ", gamma
        return gamma


    def run(self):
        self.num=0
        for e in self.eta:
            self.g_e.append(self.gamma)
            req_num=2./e*(math.log(1./self.beta)+1.)
            while self.num < req_num:
                self.num+=1
                A,B=generateRandomLocSet(self.K,self.env.size)
                ratio = getRatio(A,B,self.env)
                if ratio < self.g_e[-1]:
                    self.g_e[-1]=ratio
                    self.gamma=ratio
            self.n_e.append(self.num)
            print "Completed. Rounds: ", req_num, "e: ", e, "gamma: ", self.gamma

#solver=Solver()
#solver.run()

#plt.plot(solver.n_e,solver.g_e)
#plt.show()
