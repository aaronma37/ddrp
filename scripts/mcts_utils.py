#!/usr/bin/env python
import math
import pickle
from random import sample
from random import randint
MAX_SEARCH_LEN=2
C1=1.95

def _check_init(values,s,t):
    if values['N'].get(s) == None:
        values['N'][s]=0.
    if values['Q'].get(s) == None:
        values['Q'][s]={}
        values['Q'][s][t]=0.
    elif values['Q'][s].get(t)==None:
        values['Q'][s][t]=0.
    if values['Na'].get(s) == None:
        values['Na'][s]={}
        values['Na'][s][t]=0.
    elif values['Na'][s].get(t)==None:
        values['Na'][s][t]=0.

def _step_v(v,s,t):
    v['N'][s]+=1
    v['Na'][s][t]+=1

def _ucb(r,n,na):
    return r+C1*math.sqrt(math.log(n+1)/(na+1))

def get_candidate_task(v,action_space,s,explore=True):
    _max_val=None
    _task=None
    for t in sample(action_space,len(action_space)):
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

def value_update(v,s,t,r):
    v['Q'][s][t]+=(r-v['Q'][s][t])/(v['Na'][s][t])

def _dist(r1,r2):
    return abs(r1[0]-r2[0])+abs(r1[1]-r2[1])

def get_full_env_state(env):
    return (pickle.dumps(env.getObs()),pickle.dumps(env.region_position))
