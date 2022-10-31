#!/usr/bin/env python3  
import roslib
roslib.load_manifest('learning_tf')

import rospy
import roslaunch
import random

from std_srvs.srv import Empty
from learning_tf.srv import turtle_snake

def handle_turtlesim_snake(req):

    x = round(random.uniform(0.5,10.5),1)
    y = round(random.uniform(0.5,10.5),1)
    theta = 0
    turtlename = "turtle2"
    turtletarget = "turtle1"

    rospy.wait_for_service('spawn_snake_turtle')
    spawnSnakeTurtle = rospy.ServiceProxy('spawn_snake_turtle', turtle_snake)
    spawnSnakeTurtle(x, y, theta, turtlename, turtletarget)

if __name__ == '__main__':
    rospy.init_node("start_turtlesim_snake_server")
    rospy.loginfo("Turtlesim Snake server node created")
    service = rospy.Service("/start_turtlesim_snake", Empty, handle_turtlesim_snake)
    rospy.loginfo("Service server has been started")
    rospy.spin()
