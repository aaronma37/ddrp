#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import environment_definition
import re

def get_state_string_for_region(complete_environment_msg,region):
    state_string_for_region=''
    for objective_name in environment_definition.objective_names:
        state_string_for_region=state_string_for_region+get_state_string_for_region_objective(complete_environment_msg,objective_name,region)+'o'
    return state_string_for_region + 'r'
        
    
def get_state_string_for_region_objective(complete_environment_msg,objective_name,region):
    for r_o_s in complete_environment_msg.region_objective_states:
        if r_o_s.region.x==region.x and r_o_s.region.y==region.y:
            if r_o_s.objective_name==objective_name:
                return str(r_o_s.state)
    return str(0)
                    

def get_state_region_string(state):
    return state[state.find("s[")+2:state.find("]s")]

def get_sequential_region_string(state):
    return state[state.find("c[")+2:state.find("]c")]

def get_sequential_region_string_k(state,k):
    return get_sequential_region_string(state).split('r')[k]    

def is_repeated_region(state):
    if get_sequential_region_string_k(state,0)==get_sequential_region_string_k(state,1):
        return True
    return False
    
def get_state_length(state):
    return len(get_sequential_region_string(state).split('r'))-1
    
def get_partial_state_to_k_list(state):
    partial_state_to_k_list=[]
    
    region_states=get_state_region_string(state)
    region_state=region_states.split('r')[:-1]
    sequential_regions=get_sequential_region_string(state)
    region_sequence=sequential_regions.split('r')[:-1]
    for i in range(1,len(region_state)):
        temp_region_states=recompile(region_state[0:i],'r')
        temp_sequetial_regions=recompile(region_sequence[0:i],'r')
        partial_state_to_k_list.append('s[' +temp_region_states+ ']sc[' +temp_sequetial_regions+']c')
    return partial_state_to_k_list
    
    
def decrement_region_state(region_state,objective_name):
    region_objective_states=region_state.split('o')[:-1]
    if objective_name != 'none' and int(region_objective_states[environment_definition.objective_map[objective_name]])>=1:
        region_objective_states[environment_definition.objective_map[objective_name]]=str(int(region_objective_states[environment_definition.objective_map[objective_name]])-1)
    return recompile(region_objective_states,'o')
    
def recompile(string_list, delimiter):
    recompiled_string=''
    for s in string_list:
        recompiled_string=recompiled_string+s+delimiter
    return recompiled_string

def state_evolve(state,objective_name):
    region_states=get_state_region_string(state)
    region_state=region_states.split('r')[:-1]
    sequential_regions=get_sequential_region_string(state)
    region_sequence=sequential_regions.split('r')[:-1]
    for i in range(1,len(region_sequence)):
        if region_sequence[i]=='-':
            continue
        if int(region_sequence[i])==0:
            region_state[i]=decrement_region_state(region_state[i],objective_name)   

    region_states=recompile(region_state[1:],'r')
    sequential_regions=recompile(region_sequence[1:],'r')
    return 's[' +region_states+ ']sc[' +sequential_regions+']c'
    
def get_region_objective_at_k(state,objective_name,k):
    if objective_name is 'none':
        return 0
    return int(get_state_region_string(state).split('r')[k].split('o')[environment_definition.objective_map[objective_name]])
    
    

    
