#!/usr/bin/env python
import math
import pickle
from random import randint
MAX_SEARCH_LEN=2
C1=1.95
C2=1.95



class node():
    def __init__(self,parent,val):
        self.val=val
        self.parent=parent
        self.nextDict=None
        self.completed=False
        self.explored=False

    def explore(self,e):
        self.explored=True
        self.nextDict={}
        for sr in get_available_regions(self.val,e):
            newNode=node(self,sr)
            self.nextDict[sr]=newNode

    def get_next_and_explore(self,r,e):
        if self.nextDict.get(r) is None:
            print "ERROR",r
        if self.nextDict[r].explored is True:
            return self.nextDict[r]
        self.nextDict[r].explore(e)
        return self.nextDict[r]

    def check_parent_node_completion(self):
        for k,v in self.nextDict.items():
            if v.completed is False:
                return
        self.completed=True
        if self.parent is None:
            return
        self.parent.check_parent_node_completion()


    def check_and_complete_node(self):
        self.completed=True
        self.nextDict={}
        if self.parent is None:
            return
        self.parent.check_parent_node_completion()

    def printValues(self):
        print self.val,self.completed
        if self.nextDict is None:
            return
        for k,v in self.nextDict.items():
            v.printValues()

    def getSize(self):
        val=1
        if self.nextDict is None:
            return 0
        for k,v in self.nextDict.items():
            val+=v.getSize()
        return val

def get_available_regions(init_r,e):
    r_list=[]
    for r in e.region:
        if _dist(init_r,r) <= MAX_SEARCH_LEN:
            r_list.append(r)
    return r_list

def _check_init(values,s,t):
    if values['N'].get(s) == None:
        values['N'][s]=0.
    if values['Na'].get(s) == None:
        values['Na'][s]={}
        values['Na'][s][t]=0.
    elif values['Na'][s].get(t)==None:
        values['Na'][s][t]=0.
    if values['Q'].get(s) == None:
        values['Q'][s]={}
        values['Q'][s][t]=0.
    elif values['Q'][s].get(t)==None:
        values['Q'][s][t]=0.

def _step_v(v,s,t):
    v['N'][s]+=1
    v['Na'][s][t]+=1

def _ucb(r,n,na):
    return r+C1*math.sqrt(math.log(n+1)/(na+1))

def get_candidate_task(v,objectives,s,explore=True):
    _max_val=None
    _task=None
    for t,objective_wp in objectives.items():
        _check_init(v,s,t)
        if explore==True:
            val=_ucb(v['Q'][s][t],v['N'][s],v['Na'][s][t])
        else:
            val=v['Q'][s][t]
            if v['Na'][s][t]==0:
                _step_v(v,s,t)
                return t
        if _max_val is None:
            _max_val=val
            _task=t
        elif val > _max_val:
            _max_val=val
            _task=t
    _step_v(v,s,_task)
    return _task

def task_value_update(v,s,t,r):
    v['Q'][s][t]+=(r-v['Q'][s][t])/(v['Na'][s][t])

def _dist(r1,r2):
    return abs(r1[0]-r2[0])+abs(r1[1]-r2[1])

def get_sub_env_state(init_loc,env,sub_env):
    environment_state=env.getObs()#[x][y][obj]
    num_obj=len(env.objectives)
    sub_env_state=()
    temp_r_list=[]
    for r in sub_env:
        r_state=()
        for k,v in env.objectives.items():
            r_state=r_state+(environment_state[r[0]][r[1]][k],)
        regional_state=(r_state,_dist(init_loc,r))
        repeated=0
        for i in range(len(temp_r_list)):
            if r==temp_r_list[i]:
                repeated=i
                break
        #sub_env_state=sub_env_state + (regional_state,)
        sub_env_state=sub_env_state + (regional_state,)+(repeated,)
        init_loc=r
        temp_r_list.append(r)
    return sub_env_state

def printV(v):
    if v['Qe'] is not None:
        for k,a in v['Qe'].items():
            print 'Qe',k,a

def update_full_sub_envs(env_dict,sub_env,r,mt):
    if env_dict.get(sub_env) is None:
        env_dict[sub_env]=(r,mt)
        return
    if env_dict[sub_env][0] < r:#BIG TYPO?
        env_dict[sub_env]=(r,mt)

def _init_env_values(v,s):
    if v['Ne'].get(s) is None:
        v['Ne'][s]=0
    if v['M2'].get(s) is None:
        v['M2'][s]=0
    if v['Qe'].get(s) is None:
        v['Qe'][s]=0

def sub_env_value_update(v,s,r):
    if len(s)<1:
        return
    _init_env_values(v,s)
    v['Ne'][s]+=1
    d=r-v['Qe'][s]
    v['Qe'][s]+=d/(v['Ne'][s])
    d2=r-v['Qe'][s]
    v['M2'][s]+=d*d2
    sub_env_value_update(v,s[:-1],r)

def get_var(v,s):
    _init_env_values(v,s)
    if v['Ne'][s]==1:
        return 0
    return v['M2'][s]/(v['Ne'][s]-1)

def get_candidate_region(v,env,sub_env,explore,completion_node,num_step):
    _max_val=None
    _region=None
    # print completion_node
    for r,node in completion_node.nextDict.items():
        if node.completed is True:
            continue
        if len(sub_env)>0:
            if _dist(sub_env[-1],r)>MAX_SEARCH_LEN:
                print sub_env[-1],r
                print "THIS SHOULD NEVER HAPPEN"
                continue
        elif _dist(env.region_position,r)>MAX_SEARCH_LEN:
            print "THIS ALSO SHOULDNT HAPPEN"
            continue
        s=get_sub_env_state(env.region_position,env,sub_env+(r,))
        _init_env_values(v,s)
        if explore is True:
            # print sub_env,s,v['Ne'][s],"HERE"
            if v['Ne'][s]==0:
                return r
            if randint(0,100)>5*(1-1/math.exp(num_step/100.)):
                val=v['Qe'][s]+C2*get_var(v,s)/math.sqrt(1+v['Ne'][s])
            else:
                val=randint(0,100)
            #print get_var(v,s),'2'
        else:
            val=v['Qe'][s]
        if _max_val is None:
            _max_val=val
            _region=r
        elif _max_val < val:
            _max_val=val
            _region=r
    return _region

def get_best_full_sub_envs(sub_env_dict):
    _max_val=None
    _max_key=None
    _max_a=None
    for k,a in sub_env_dict.items():
        if _max_val is None:
            _max_val=a[0]
            _max_key=k
            _max_a=a[1]
        elif a[0] > _max_val:
            _max_val=a[0]
            _max_key=k
            _max_a=a[1]
    return _max_key,_max_val,_max_a

def save_data(filename,v):
    with open(filename,'wb') as fp:
        pickle.dump(v,fp)
