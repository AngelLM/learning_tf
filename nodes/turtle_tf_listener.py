#!/usr/bin/env python3  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')

    listener = tf.TransformListener()

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 2, 0, 'turtle2')

    turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)

    rate = rospy.Rate(10.0)

    following = False

    #listener.waitForTransform("/turtle2", "/turtle1", rospy.Time(), rospy.Duration(4.0))
    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now() 
            past = now #- rospy.Duration(0)
            listener.waitForTransformFull("/turtle2", now,
                                    "/turtle1", past,
                                    "/world", rospy.Duration(1.0))
            (trans,rot) = listener.lookupTransformFull("/turtle2", now,
                                                    "/turtle1", past,
                                                    "/world")
        except (tf.Exception, tf.LookupException, tf.ConnectivityException):
            continue

        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 2 #0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        distance = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        
        # Let's check if the main turtle is near enough to follow
        if not following and distance < 1:
            following = True

        if following and distance >= 1:
            cmd.linear.x = linear
            cmd.angular.z = angular
        else:
            cmd.linear.x = 0
            cmd.angular.z = 0

        turtle_vel.publish(cmd)

        rate.sleep()