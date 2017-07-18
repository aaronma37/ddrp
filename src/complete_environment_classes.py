#!/usr/bin/env python

from random import randint
import random
import numpy as np
import math
from ddrp.msg import Environment
from ddrp.msg import Objective
from ddrp.msg import Waypoint
from ddrp.msg import RegionObjectiveState
from ddrp.msg import Region
from ddrp.msg import Objective
from ddrp.msg import Waypoint
#import environment_definition as env_def

def copy(new_env_msg,ref_env_msg):
    new_env_msg.frame_id = ref_env_msg.frame_id
    new_env_msg.objectives=[]
    for Obj in ref_env_msg.objectives:
        new_Obj=Objective()
        new_Obj.objective_name=Obj.objective_name
        for o in Obj.waypoints:
            wp = Waypoint()
            wp.x=o.x
            wp.y=o.y
            new_Obj.waypoints.append(wp)
        new_env_msg.objectives.append(new_Obj)
    for ros in ref_env_msg.region_objective_states: 
        new_ros=RegionObjectiveState()
        new_ros.objective_name=ros.objective_name
        new_ros.region.x=ros.region.x
        new_ros.region.y=ros.region.y
        new_ros.state=ros.state
        new_env_msg.region_objective_states.append(new_ros)

def clone_env_msg_from_complete_environment(complete_environment):
	env_msg=Environment()
	env_msg.frame_id="default"
		
	env_msg.objectives=[]
	for o_msg in complete_environment.complete_environment_msg.objectives:
        	objective_msg=Obective()
        	objective_msg.objective_name=o_msg.objective_name
        	for wp_msg in o_msg.waypoints:
            		waypoint_msg=Waypoint()
            		waypoint_msg.x=wp_msg.x
            		waypoint_msg.y=wp_msg.y
            		objective_msg.waypoints.append(waypoint_msg)
       		env_msg.objectives.append(objective_msg)
    
    	for r_o_s in complete_environment.complete_environment_msg.region_objective_states:
        	region_objective_state_msg=RegionObjectiveState()
        	region_objective_state_msg.objective_name=r_o_s.objective_name
        	region_objective_state_msg.state=r_o_s.state
        	region_msg=Region()
        	region_msg.x=r_o_s.region.x
        	region_msg.y=r_o_s.region.y
        	region_objective_state_msg.region=region_msg
 
	return env_msg

def evolve_environment_msg(complete_environment_msg,task):
    task_msg=task.task
    for r_o_s in complete_environment_msg.region_objective_states:
        if r_o_s.objective_name == task_msg.objective_name:
            if r_o_s.region.x==task_msg.initial_region.x and r_o_s.region.y==task_msg.initial_region.y and int(r_o_s.state)>=1 and int(task_msg.objective_state)>=1:
                r_o_s.state=int(task_msg.objective_state-1)          
    return complete_environment_msg
		
class CompleteEnvironment:
    def __init__(self):
        self.complete_environment_msg=Environment()
        
    def generate_random_environment(self):
        self.complete_environment_msg=Environment()
        self.complete_environment_msg.frame_id="default"
        self.complete_environment_msg.objectives=[]
        self.complete_environment_msg.region_objective_states=[]
        for obj_msg in env_def.generate_objective_set():
            self.complete_environment_msg.objectives.append(obj_msg)
        self.update_region_objective_state()
    
    def update_region_objective_state(self):
        self.complete_environment_msg.region_objective_states=[]
        region_check={}
        
        for o_msg in self.complete_environment_msg.objectives:
            for wp_msg in o_msg.waypoints:
                if region_check.get(env_def.get_region(wp_msg.x,wp_msg.y)) is None:
                    region_check[env_def.get_region(wp_msg.x,wp_msg.y)]
                    region_objective_state_msg=RegionObjectiveState()
                    region_objective_state_msg.objective_name=o_msg.objective_name
                    region_objective_state_msg.state=1
                    region_objective_state_msg.region.x=env_def.get_region(wp_msg.x,wp_msg.y)[0]
                    region_objective_state_msg.region.y=env_def.get_region(wp_msg.x,wp_msg.y)[1]
                    self.complete_environment.region_objective_state.append(region_objective_state_msg)
                    continue
                    

            
            
            





