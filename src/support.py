#!/usr/bin/env python


from random import randint
import random
import copy
import numpy as np
import math
from sets import Set
import time
from random import shuffle
import task_classes
import string_operations
Gamma=.98
C=1.

def check_variables_task_init(Q,N,Na,s,t):

	if N.get(s) == None:
		N[s] = 0.

	if Na.get(s)==None:
		Na[s]={}
		Na[s][t]=0.
	elif Na[s].get(t)==None:
		Na[s][t]=0.

	if Q.get(s) == None:
		Q[s]={}
		Q[s][t]=0.
	elif Q[s].get(t)==None:
		Q[s][t]=0.

def increase_var_task(N,Na,s,t):
    N[s]+=1
    Na[s][t]+=1


def check_variables_sub_env_init(Qe,Ne,Var,s):
	if Ne.get(s) == None:
		Ne[s] = 1.
		
	if Var.get(s)==None:
		Var[s]=0
	else:
		Var[s]+=0

	if Qe.get(s) == None:
		Qe[s]=0.

def increase_var_sub(Qe,Ne,Var,s):
    Ne[s]+=1


def arg_max_task(Q,N,Na,e):
	if Q.get(e.state)==None:
		Q[e.state]={}

	v=list(Q[e.state].values())
	key=list(Q[e.state].keys())
	if len(key)==0:
		return 'wait'

	return key[v.index(max(v))]
	
#USE TUPLE BEST EXP VALUE?	
def arg_max_partial_sub_environment(Qe,Ne,Var,partial_sub_env_set):
    max_val=-1
    best_partial_sub_env=None
    
    for e in partial_sub_env_set:
        if Qe.get(e.state)==None:
            Qe[e.state]=0
        if Qe[e.state] > max_val:
            max_val=Qe[e.state]
            best_partial_sub_env=e
    return best_partial_sub_env

def get_candidate_partial_sub_env(Qe,Ne,Var,partial_sub_environment_set):
    max_val=0
    candidate_partial_sub_env = None
    for e in partial_sub_environment_set:
        if candidate_partial_sub_env is None:
            candidate_partial_sub_env = e
        check_variables_sub_env_init(Qe,Ne,Var,e.state)
        val = get_candidate_partial_sub_env_value(Qe,Ne,Var,e)
        if val > max_val:
            max_val = val
            candidate_partial_sub_env = e
    return candidate_partial_sub_env
	
def get_candidate_partial_sub_env_value(Qe,Ne,Var,e):
	return partial_sub_env_ucb(Qe[e.state],Ne[e.state],Var[e.state])

def partial_sub_env_ucb(r,n,var):
	return r+C*var/math.sqrt(1+n)
	
	
def get_candidate_task(Q,N,Na,feasible_task_set,state):
    max_val=-1
    candidate_task = 'none'
    for objective_name in feasible_task_set:
        check_variables_task_init(Q,N,Na,state,objective_name)
        val = get_candidate_task_value(Q,N,Na,objective_name,state)
        if val > max_val:
            max_val = val
            candidate_task = objective_name
    increase_var_task(N,Na,state,candidate_task)
    return candidate_task
	
def get_candidate_task_value(Q,N,Na,objective_name,state):
	return task_ucb(Q[state][objective_name],N[state],Na[state][objective_name])

def task_ucb(r,n,na):	
	return r+C*math.sqrt(math.log(n+1)/(na+1))
	
def task_value_update(Q,Na,state,objective_name,r):
    Q[state][objective_name]+=(r-Q[state][objective_name])/(Na[state][objective_name])
    
def sub_env_value_update(Qe,Ne,Var,full_sub_env_state,r):
    for state in string_operations.get_partial_state_to_k_list(full_sub_env_state):
        _sub_env_value_update_k(Qe,Ne,Var,state,r)
    
def _sub_env_value_update_k(Qe,Ne,Var,state,r):
    check_variables_sub_env_init(Qe,Ne,Var,state)
    Ne[state]+=1
    Qe[state]+=(r-Qe[state])/(Ne[state])
    Var[state]+=0 #NEED TO DO
    
    
def write_q(Q,Na):
    file = open('/home/aaron/Q.txt','w')
    for s,q in Q.items():
        file.write(str(s)+"*\n")
        for a,r in q.items():
            file.write(str(a)+'*'+str(r)+'*'+str(Na[s][a])+"*\n")
    file.close()
    

