#!/usr/bin/env python
import sets
import utils

class DDRP:
    def __init__(self,environment):
        self.values={}
        self.values['Q']={}
        self.values['N']={}
        self.values['Na']={}
        self.values['Qe']={}
        self.values['Ne']={}
        self.values['M2']={}
        self.discount=.98
        self.max_sub_env_length=10
        self.current_environment=environment.getCopy()
        self.full_sub_envs={}
        self.temp_env=None

    def set_environment(self,env):
        self.current_environment=env.getCopy()

    def _reset_temp_env(self):
        self.temp_env=self.current_environment.getCopy()


    def _task_search(self,sub_env,macro_task):
        if len(sub_env)==0:
            return 0,macro_task
        s=utils.get_sub_env_state(self.temp_env.region_position,self.temp_env,sub_env)
        t=utils.get_candidate_task(self.values,self.temp_env.objectives_size,s)
        macro_task=macro_task+(t,)
        o,r,done,info=self.temp_env.step_ddrp((sub_env[0][0],sub_env[0][1],t))
        reward = self.discount**self.temp_env.steps*r
        r,m=self._task_search(sub_env[1:],macro_task)
        reward+=r
        macro_task=m
        utils.task_value_update(self.values,s,t,reward)
        return reward,macro_task

    def _sub_environment_search(self,partial_sub_env):
        if len(partial_sub_env)>=self.max_sub_env_length:
            return partial_sub_env
        r = utils.get_candidate_region(self.values,self.temp_env,partial_sub_env)
        return self._sub_environment_search(partial_sub_env+(r,))

    def step(self):
        self._reset_temp_env()
        sub_env = self._sub_environment_search(())
        s=utils.get_sub_env_state(self.temp_env.region_position,self.temp_env,sub_env)
        step_reward,macro_task = self._task_search(sub_env,())
        utils.update_full_sub_envs(self.full_sub_envs,sub_env,step_reward,macro_task)
        utils.sub_env_value_update(self.values,s,step_reward)

    def evaluate(self):
        self._reset_temp_env()
        episode_reward=0
        sub_env,val,mt=utils.get_best_full_sub_envs(self.full_sub_envs)
        for r in sub_env:
            obs,r,done,info=self.temp_env.step_ddrp(r)
            episode_reward+=r
        # print episode_reward
        # print info
        # print sub_env,', s: ', utils.get_sub_env_state(self.temp_env.region_position,self.temp_env,sub_env) , ', r: ', episode_reward
        return episode_reward 
