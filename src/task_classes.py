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
import sub_environment_classes
import string_operations
import environment_definition
from ddrp.msg import Task as Task_msg

def get_waypoint(task,complete_environment_msg,agent_msg):
    if task.is_complete(complete_environment_msg,agent_msg):
        print "task is completed"
        return None
    if task.is_objective_requirements_satisfied(complete_environment_msg):
        return closest_objective_location_in_region(task,complete_environment_msg)
    return next_region_waypoint(task)
    
def next_region_waypoint(task):
    return environment_definition.get_region_mean((task.task.target_region.x,task.task.target_region.y))
    
def closest_objective_location_in_region(task,complete_environment_msg,agent_msg):
    min_distance = 1000000
    best_waypoint= None

    for o in complete_environment_msg.objectives:
        if o.objective_name==task.task.objective_name:
            for wp in o.waypoints:
                if environment_definition.is_in_region((task.task.initial_region.x,task.task.initial_region.y),wp.x,wp.y):
                    distance = distance((agent_msg.x,agent_msg.y),(wp.x,wp.y))
                    if distance < min_distance:
                        min_distance = distance
                        best_waypoint=(wp.x,wp.y)
    return best_waypoint
    
def sample_time_from_state(state,objective_name):
    
    if objective_name=='none':
        action_time=0
    else:
        action_time=5
    
    if string_operations.is_repeated_region(state):
        travel_time=0
    else:
        travel_time=7
    
    return travel_time+action_time

class Task:
    def __init__(self, requirements):
        self.task=Task_msg()
        self.task.objective_name=requirements[0]
        self.task.objective_state=requirements[1]
        self.task.initial_region=requirements[2]
        self.task.target_region=requirements[3]
        self.requirements=requirements      #(objective_name,objective_state,(i,j),(p,q))
        
    def is_complete(self,complete_environment_msg,agent_msg):
        if self.is_objective_requirements_satisfied(complete_environment_msg) and self.is_region_requirements_satisfied(agent_msg):
            return True
        return False
        
    def is_objective_requirements_satisfied(self,complete_environment_msg):
        for region_objective_state in complete_environment_msg.region_objective_states:
            if (region_objective_state.region.x,region_objective_state.region.y)==(self.task.initial_region.x,self.task.initial_region.y):
                if self.task.objective_state==region_objective_state.state:
                    return False
        return True
        
    def is_region_requirements_satisfied(self,agent_msg):
        return environment_definition.is_in_region((self.task.target_region.x,self.task.target_region.y),agent_msg.x,agent_msg.y)
        
        
        
