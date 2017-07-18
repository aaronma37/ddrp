#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from ddrp.msg import Waypoint
from ddrp.msg import Objective
import string_operations

objective_names=['obj_1','obj_2']
feasible_task_set=['obj_1','obj_2','none']
objective_generation=['none','random','random']
NUM_OBJECTIVES=2
RAND_LOW_BOUND=5
RAND_HIGH_BOUND=15
RAND_LOW_BOUND_X=5
RAND_HIGH_BOUND_X=15
RAND_LOW_BOUND_Y=5
RAND_HIGH_BOUND_Y=15


            
objective_map={}

for i in range(len(objective_names)):
    objective_map[objective_names[i]]=i
    objective_map[i]=objective_names[i]

region_size_x=10.
region_size_y=10.

def get_reward(state,objective_name):
    if objective_name == 'none':
        return 0
    if int(string_operations.get_region_objective_at_k(state,objective_name,0)) <= 0:
        return 0

    return 1

def get_region_mean(region):
    return ((region[0]+.5)*region_size_x,(region[1]+.5)*region_size_y)
    
def is_in_region(region,i,j):
    if i >= region[0]*region_size_x and i < (region[0]+1)*region_size_x:
        if j >= region[1]*region_size_y and j < (region[1]+1)*region_size_y:
            return True
    return False
    
def get_region(i,j):
    return (int(math.floor(i/region_size_x)),int(math.floor(j/region_size_y)))
    
    
def generate_objective_set():
    objective_msg_list=[]
    for i in range(NUM_OBJECTIVES):
        objective_msg=Objective()
        objective_msg.objective_name=objective_map[i]
        objective_msg.waypoints=generate_waypoints(i)
        objective_msg_list.append(objective_msg_list)
    return objective_msg_list
    
def generate_waypoints(i):
    waypoint_list=[]
    if objective_generation[i]=='random':
        for i in range(randint(RAND_LOW_BOUND,RAND_HIGH_BOUND)):
            waypoint_msg=Waypoint()
            waypoint_msg.x=randint(RAND_LOW_BOUND_X,RAND_HIGH_BOUND_X)
            waypoint_msg.y=randint(RAND_LOW_BOUND_Y,RAND_HIGH_BOUND_Y)
            waypoint_list.append(waypoint_msg)
        return waypoint_list
          

