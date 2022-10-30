#!/usr/bin/env python3  
import roslib
roslib.load_manifest('learning_tf')

import rospy
import roslaunch
import os

from std_srvs.srv import Empty

def handle_turtlesim_snake(Empty):
    rospy.loginfo("handler")
    #package = 'learning_tf'
    #executable = 'turtle_tf_listener'
    #node = roslaunch.core.Node(package, executable)

    #launch = roslaunch.scriptapi.ROSLaunch()
    #launch.start()
    os.system('rosrun learning_tf turtle_tf_listener.py _turtlename:="turtle2"')
    
if __name__ == '__main__':
    rospy.init_node("start_turtlesim_snake_server")
    rospy.loginfo("Turtlesim Snake server node created")
    service = rospy.Service("/start_turtlesim_snake", Empty, handle_turtlesim_snake)
    rospy.loginfo("Service server has been started")
    rospy.spin()
