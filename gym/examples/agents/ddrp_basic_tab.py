from tabular_q_agent import TabularQAgent as Agent

from gym.spaces import discrete
import gym
import numpy as p
import matplotlib.pyplot as plt


env=gym.make("ddrp_basic-v0")
env.seed(0)
agent=Agent(env.observation_space,env.action_space)
reward=[]

for i in range(100000):
    reward.append( agent.learn(env) )

avg_reward=[]
m=50.
for i in range(len(reward)):
    if i < m:
        continue
    avg_reward.append(reward[i-int(m)]/m)
    for j in range(i-int(m)+1,i):
        avg_reward[-1]+=reward[j]/m

plt.plot(avg_reward)
plt.title('Tabular Q on primitive actions and complete state')
plt.ylabel('Average reward per trial')
plt.xlabel('Trials')
plt.show()

