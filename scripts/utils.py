#!/usr/bin/env python
import math
C=1.95
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
    return r+C*math.sqrt(math.log(n+1)/(na+1))

def get_candidate_task(v,objective_size,s,explore=True):
    _max_val=None
    _task=None
    for t in range(objective_size):
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
    num_obj=env.objectives_size
    sub_env_state=()
    for r in sub_env:
        r_state=()
        for o in range(num_obj):
            r_state=r_state+(environment_state[r[0]][r[1]][o],)
        regional_state=(r_state,_dist(init_loc,r))
        sub_env_state=sub_env_state + (regional_state,)
        init_loc=r
    return sub_env_state

def printV(v):
    if v['Qe'] is not None:
        for k,a in v['Qe'].items():
            print 'Qe',k,a

def update_full_sub_envs(env_dict,sub_env,r,mt):
    if env_dict.get(sub_env) is None:
        env_dict[sub_env]=(r,mt)
        return
    if env_dict[sub_env][0] > r:
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

def get_candidate_region(v,env,sub_env,explore=True):
    _max_val=None
    _region=None
    for r in env.region:
        s=get_sub_env_state(env.region_position,env,sub_env+(r,))
        _init_env_values(v,s)
        if explore is True:
            # print sub_env,s,v['Ne'][s],"HERE"
            if v['Ne'][s]==0:
                return r
            val=v['Qe'][s]+C*get_var(v,s)/math.sqrt(1+v['Ne'][s])
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

            

