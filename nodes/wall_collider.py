#!/usr/bin/env python3
import rospy
import random
import turtlesim.srv
import turtlesim.msg
from std_msgs.msg import Bool

def telep_main_turtle():
    rospy.wait_for_service('/turtle1/teleport_absolute')
    telep = rospy.ServiceProxy('/turtle1/teleport_absolute', turtlesim.srv.TeleportAbsolute)
    telep(5.5,5.5,round(random.uniform(-3.1,3.1),1))

def callback(data):
    if data.x < 0.5 or data.x > 11.0 or data.y <0.5 or data.y > 11.0:
        telep_main_turtle()
        pubKill.publish(True)


if __name__ == '__main__':
    rospy.init_node('wallCollider')
    rospy.Subscriber("/turtle1/pose", turtlesim.msg.Pose, callback)
    pubKill = rospy.Publisher('/killTurtles', Bool, queue_size=10)
    rospy.spin()