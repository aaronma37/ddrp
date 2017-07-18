#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from complete_environment_classes import CompleteEnvironment
import complete_environment_classes
import sub_environment_classes
import sets
import time
import support
import task_classes
import string_operations
import environment_definition
from ddrp.msg import Environment
from ddrp.msg import Agent
from ddrp.msg import Task

class DDRPMain:
    def __init__(self):
        self.complete_environment_msg=Environment()
        self.expected_complete_environment_msg=Environment()
        self.agent_msg=Agent()
        self.partial_sub_environment_set=set()
        self.partial_sub_environment_set.add(sub_environment_classes.Sub_Environment(None,self.complete_environment_msg,(int(self.agent_msg.x),int(self.agent_msg.y))))
        self.full_sub_environment_set=set()
        self.task=None
        self.step_time=1
        self.Q={}
        self.N={}
        self.Na={}
        self.Qe={}
        self.Ne={}
        self.Var={}
        self.discount=.98
        self.max_sub_env_length=3

    def update_environment(self,complete_environment_msg):
        complete_environment_classes.copy(self.complete_environment_msg,complete_environment_msg)

    def update_agent(self,agent_msg):
        self.agent_msg=agent_msg
		
    def step(self):
        start=time.time()
        while time.time() < start+self.step_time:
			self.estimate_environment()
			self.imagine()
        support.write_q(self.Q,self.Na)
        if self.task is None:
            self.task_selection()
            return
        if self.task.is_complete(self.complete_environment_msg,self.agent_msg):
            self.task_selection()
            return
            
    def task_selection(self):
        best_sub_environment = support.arg_max_partial_sub_environment(self.Qe,self.Ne,self.Var,self.full_sub_environment_set)
        objective_name=support.arg_max_task(self.Q,self.N,self.Na,best_sub_environment)
        self.task = task_classes.Task((objective_name,
			    string_operations.get_region_objective_at_k(best_sub_environment.state,objective_name,0),
			    best_sub_environment.region_list[0],
			    best_sub_environment.region_list[1]))
        self.full_sub_environment_set.clear()
        self.partial_sub_environment_set.clear()
        self.partial_sub_environment_set.add(sub_environment_classes.Sub_Environment(None,self.expected_complete_environment_msg,(self.agent_msg.x,self.agent_msg.y)))
			
    def imagine(self):
        partial_sub_environment = support.get_candidate_partial_sub_env(self.Qe,self.Ne,self.Var,self.partial_sub_environment_set)
        sub_environment = self.sub_env_search(partial_sub_environment)
        expected_reward = self.task_search(sub_environment.state,0)
        self.full_sub_environment_set.add(sub_environment)
        support.sub_env_value_update(self.Qe,self.Ne,self.Var,sub_environment.state,expected_reward)
	
    def task_search(self,state,d):
        if string_operations.get_state_length(state)==0:
            return 0
        feasible_task_set=environment_definition.feasible_task_set
        objective_name=support.get_candidate_task(self.Q,self.N,self.Na,feasible_task_set,state)
        t=task_classes.sample_time_from_state(state,objective_name)
        state_ = string_operations.state_evolve(state,objective_name)
        r = math.pow(self.discount,t+d)*(environment_definition.get_reward(state,objective_name)+self.task_search(state_,t+d))
        support.task_value_update(self.Q,self.Na,state,objective_name,r)
        return r
		
    def sub_env_search(self,partial_sub_environment):
        if len(partial_sub_environment.region_list) >= self.max_sub_env_length:
            self.partial_sub_environment_set.remove(partial_sub_environment)
            return partial_sub_environment
        new_partial_sub_environments = sub_environment_classes.get_feasible_partial_sub_environment(partial_sub_environment,self.expected_complete_environment_msg)
        for new_partial_sub_environment in new_partial_sub_environments:
            self.partial_sub_environment_set.add(new_partial_sub_environment)
        if len(partial_sub_environment.region_list)>1:
            self.partial_sub_environment_set.remove(partial_sub_environment)
        partial_sub_environment = support.arg_max_partial_sub_environment(self.Qe,self.Ne,self.Var,new_partial_sub_environments)
        return self.sub_env_search(partial_sub_environment)
		
    def estimate_environment(self):
        if self.task is None:
            return
        self.expected_complete_environment_msg=complete_environment_classes.evolve_environment_msg(self.complete_environment_msg, self.task)
