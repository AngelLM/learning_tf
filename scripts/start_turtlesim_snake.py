#!/usr/bin/env python3  
import roslib
roslib.load_manifest('learning_tf')

import rospy
import roslaunch
import random

import turtlesim.srv
from std_srvs.srv import Empty
from learning_tf.srv import turtle_snake

def disable_pen(turtle):
    r=0
    g=0
    b=0
    width=0
    off=1
    rospy.wait_for_service('/%s/set_pen' % turtle)
    setpen = rospy.ServiceProxy('/%s/set_pen' % turtle, turtlesim.srv.SetPen)
    setpen(r,g,b,width,off)

def changeBgColor():
    rospy.wait_for_service('/clear')
    rospy.set_param('/sim/background_r', random.randrange(0,255))
    rospy.set_param('/sim/background_g', random.randrange(0,255))
    rospy.set_param('/sim/background_b', random.randrange(0,255))
    clearSrv = rospy.ServiceProxy('/clear', Empty)
    resp = clearSrv()

def handle_turtlesim_snake(req):

    x = round(random.uniform(0.5,10.5),1)
    y = round(random.uniform(0.5,10.5),1)
    theta = 0
    turtlename = "turtle2"
    turtletarget = "turtle1"

    rospy.wait_for_service('spawn_snake_turtle')
    spawnSnakeTurtle = rospy.ServiceProxy('spawn_snake_turtle', turtle_snake)
    spawnSnakeTurtle(x, y, theta, turtlename, turtletarget)
    disable_pen(turtletarget)
    disable_pen(turtlename)
    changeBgColor()

if __name__ == '__main__':
    rospy.init_node("start_turtlesim_snake_server")
    rospy.loginfo("Turtlesim Snake server node created")
    service = rospy.Service("/start_turtlesim_snake", Empty, handle_turtlesim_snake)
    rospy.loginfo("Service server has been started")
    rospy.spin()
