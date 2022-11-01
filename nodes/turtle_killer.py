#!/usr/bin/env python3
import rospy
import rosnode
import rosservice
import turtlesim.srv
import geometry_msgs.msg
from std_srvs.srv import Empty
from std_msgs.msg import String, Bool

def stopMainTurtle():
    cmd = geometry_msgs.msg.Twist()

    cmd.linear.x = 0
    cmd.angular.z = 0

    pubVel.publish(cmd)

def clearSim():
    rospy.wait_for_service('/clear')
    rospy.set_param('/sim/background_r', 0)
    rospy.set_param('/sim/background_g', 0)
    rospy.set_param('/sim/background_b', 0)
    clearSrv = rospy.ServiceProxy('/clear', Empty)
    resp = clearSrv()

def stopSrvNodes():
    # Killing all the extra turtle services
    for service in rosservice.get_service_list():
        if "/set_pen" in service:                # looking for a service of a turtle, to only get 1 line per turtle in the sim
            if service[1:-8] != 'turtle1':
                rospy.wait_for_service('/kill')
                killSrv = rospy.ServiceProxy('/kill', turtlesim.srv.Kill)
                killSrv(service[1:-8])

    # Killing all the extra listener and broadcaster nodes
    killnodes=[]
    for node in rosnode.get_node_names():
        if "turtle_tf_" in node:
            killnodes.append(node)
    rosnode.kill_nodes(killnodes)

def callback(data):
    pubLvl.publish("GAME OVER")

    stopMainTurtle()
    clearSim()
    stopSrvNodes()

    pubLvl.publish("PRESS START")


if __name__ == '__main__':
    rospy.init_node('turtleKiller')
    pubVel = rospy.Publisher('/turtle1/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
    pubLvl = rospy.Publisher('/currentGameLevel', String, queue_size=10)
    rospy.Subscriber("killTurtles", Bool, callback)
    rospy.spin()