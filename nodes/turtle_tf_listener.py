#!/usr/bin/env python3  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import rosnode
import rosservice
import math
import tf
import random
import os
import geometry_msgs.msg
import turtlesim.srv
import learning_tf.srv
from std_srvs.srv import Empty
from std_msgs.msg import String, Bool

def changeBgColor():
    rospy.wait_for_service('/clear')

    rospy.set_param('/sim/background_r', random.randrange(0,255))
    rospy.set_param('/sim/background_g', random.randrange(0,255))
    rospy.set_param('/sim/background_b', random.randrange(0,255))

    clearSrv = rospy.ServiceProxy('/clear', Empty)
    resp = clearSrv()

def publishLevel(i):
    pub.publish("Level: %s" % str(i))

def spawnNewTurtle(i):

    x = round(random.uniform(0.5,10.5),1)
    y = round(random.uniform(0.5,10.5),1)
    theta = 0
    turtlename = "turtle%s" % str(i+1)
    turtletarget = "turtle%s" % str(i)


    rospy.wait_for_service('spawn_snake_turtle')
    spawnSnakeTurtle = rospy.ServiceProxy('spawn_snake_turtle', learning_tf.srv.turtle_snake)
    spawnSnakeTurtle(x, y, theta, turtlename, turtletarget)

    rospy.wait_for_service('/%s/set_pen' % turtlename)
    setpen = rospy.ServiceProxy('/%s/set_pen' % turtlename, turtlesim.srv.SetPen)
    r=0
    g=0
    b=0
    width=0
    off=1
    setpen(r,g,b,width,off)

if __name__ == '__main__':
    pub = rospy.Publisher('/currentGameLevel', String, queue_size=10)
    pubKill = rospy.Publisher('/killTurtles', Bool, queue_size=10)
    rospy.init_node('turtle_tf_listener', anonymous=True)

    posx = rospy.get_param('~posx')
    posy = rospy.get_param('~posy')
    theta = rospy.get_param('~theta')
    turtlename = rospy.get_param('~turtlename')
    turtletarget = rospy.get_param('~turtletarget')

    listener = tf.TransformListener()

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(posx, posy, theta, turtlename)

    turtle_vel = rospy.Publisher('%s/cmd_vel' %turtlename, geometry_msgs.msg.Twist,queue_size=10)
    turtle_collision = rospy.Publisher('/collision', Bool, queue_size=1)

    rate = rospy.Rate(10.0)

    following = False   # Variable to control if the turtle has been already caught or not
    cancollide = False  # Variable that prevents the collision when the turtle is just caught.

    publishLevel(int(turtletarget[6:]))

    while not rospy.is_shutdown():
        
        try:
            now = rospy.Time.now() 
            past = now #- rospy.Duration(0)
            listener.waitForTransformFull("/%s" %turtlename, now,
                                    "/turtle1", past,
                                    "/world", rospy.Duration(1.0))
            (trans,rot) = listener.lookupTransformFull("/%s" % turtlename, now,
                                                    "/turtle1", past,
                                                    "/world")
        except (tf.Exception, tf.LookupException, tf.ConnectivityException):
            continue

        distance = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        
        # Let's check if the main turtle is near enough to follow
        if not following and distance < 1:
            following = True
            changeBgColor()
            spawnNewTurtle(int(turtlename[6:]))
        if cancollide and distance < 0.5:
            pubKill.publish(True)

        if following:
            try:
                now = rospy.Time.now() 
                past = now #- rospy.Duration(0)
                listener.waitForTransformFull("/%s" %turtlename, now,
                                        "/%s" % turtletarget, past,
                                        "/world", rospy.Duration(1.0))
                (trans,rot) = listener.lookupTransformFull("/%s" % turtlename, now,
                                                        "/%s" % turtletarget, past,
                                                        "/world")
            except (tf.Exception, tf.LookupException, tf.ConnectivityException):
                continue

            angular = 4 * math.atan2(trans[1], trans[0])
            linear = 2 #0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            distance = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            cmd = geometry_msgs.msg.Twist()

            if distance >= 1:
                cmd.linear.x = linear
                cmd.angular.z = angular
            else:
                cmd.linear.x = 0
                cmd.angular.z = 0
                if turtlename != "turtle2": # As turtle2 will be very near to the main turtle it causes unintended collisions, this disables the collision
                    cancollide = True       # When the new turtle reachs its position in the snake the collision is enabled

            turtle_vel.publish(cmd)

        rate.sleep()