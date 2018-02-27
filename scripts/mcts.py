#!/usr/bin/env python
import sets
import mcts_utils

class MCTS:
    def __init__(self,environment):
        self.values={}
        self.values['Q']={}
        self.values['N']={}
        self.values['Na']={}
        self.discount=.98
        self.current_environment=environment.getCopy()
        self.temp_env=None
        self.num_iterations=0.
        self.max_reward=0

    def import_values(self,values):
        if values is None:
            print "Empty import"
            return
        print "Importing data"
        self.values=values

    def set_environment(self,env):
        self.current_environment=env.getCopy()

    def _reset_temp_env(self):
        self.temp_env=self.current_environment.getCopy()

    def _search(self,s_num):
        if s_num>=10:
            return 0,0
        #change to full state
        s=mcts_utils.get_full_env_state(self.temp_env)
        t=mcts_utils.get_candidate_task(self.values,self.temp_env.possible_actions,s)
        o,r,done,info=self.temp_env.step_ddrp((t[0],t[1],1))
        reward = self.discount**self.temp_env.steps*r
        non_discounted_reward = r
        r,ndr=self._search(s_num+1)
        reward+=r
        non_discounted_reward+=ndr
        mcts_utils.value_update(self.values,s,t,reward)
        return reward,non_discounted_reward

    def step(self):
        self._reset_temp_env()
        #change to full state
        s=mcts_utils.get_full_env_state(self.temp_env)
        step_reward,non_discounted_reward = self._search(0)
        if non_discounted_reward > self.max_reward:
            self.max_reward=non_discounted_reward
        self.num_iterations+=1.

    def evaluate(self):
        return self.max_reward
