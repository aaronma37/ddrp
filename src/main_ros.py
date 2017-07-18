#!/usr/bin/env python


from random import randint
import random
import time
import math
from sets import Set
import rospy
import sys

from ddrp.msg import Task
from ddrp.msg import Environment
from ddrp.msg import Agent

from ddrp_main import DDRPMain

rospy.init_node('main', anonymous=True)
task_publisher = rospy.Publisher('/task',Task,queue_size=100)

class DDRP_ROS:
    def __init__(self):
        self.ddrp=DDRPMain()

    def environment_cb(self,environment_msg):
        self.ddrp.update_environment(environment_msg)

    def agent_cb(self,agent_msg):
        self.ddrp.update_agent(agent_msg)

    def send_messages(self):
        task_publisher.publish(self.ddrp.task.task)
	
    def run(self):
        while not rospy.is_shutdown():
            self.ddrp.step()
            self.send_messages()
            time.sleep(.1)


###MAIN
def main(args):
    print "Main start"
    ddrp_ros=DDRP_ROS()
    environment_sub =rospy.Subscriber('/environment', Environment , ddrp_ros.environment_cb)
    agent_sub =rospy.Subscriber('/agent', Agent , ddrp_ros.agent_cb)
	
    try:
        ddrp_ros.run()
        rospy.spin()

    except KeyboardInterrupt:
        print("Main: Shutting down")



if __name__ == '__main__':
    main(sys.argv)

