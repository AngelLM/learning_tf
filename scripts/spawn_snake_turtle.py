#!/usr/bin/env python3  
import roslib
roslib.load_manifest('learning_tf')

import rospy
import roslaunch
import os
import _thread

from learning_tf.srv import turtle_snake

def handle_spawn_snake_turtle(req):
    #package = 'learning_tf'
    #executable = 'turtle_tf_listener'
    #node = roslaunch.core.Node(package, executable)

    #launch = roslaunch.scriptapi.ROSLaunch()
    #launch.start()

    _thread.start_new_thread(os.system,('rosrun learning_tf turtle_tf_listener.py _posx:=%s _posy:=%s _theta:=%s _turtlename:=%s _turtletarget:=%s' % (req.x, req.y, req.theta, req.turtlename, req.turtletarget),))
    _thread.start_new_thread(os.system,('rosrun learning_tf turtle_tf_broadcaster.py _turtle:=%s' % req.turtlename,))

    return True

if __name__ == '__main__':
    rospy.init_node("spawn_snake_turtle_server")
    rospy.loginfo("Snake Turtle Spawner server node created")
    service = rospy.Service("/spawn_snake_turtle", turtle_snake, handle_spawn_snake_turtle)
    rospy.loginfo("Service server has been started")
    rospy.spin()
