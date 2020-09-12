#!/usr/bin/env python
from time import sleep
import rospy
import rospy
from std_msgs.msg import Int64
import sys
import xpc

def callback(data):
    print('in the callback')
    with xpc.XPlaneConnect() as client:
            client.sendTEXT("Flight in Progress", 50, -1)
    client.sendTEXT("Flight in Progress", 50, -1)
    global advisory
    advisory= data.data
    #print(advisory)
    if advisory==15:
        print('aircraft chillen')
        with xpc.XPlaneConnect() as client:
            client.sendTEXT("Aircraft SAFE", 50, -1)
    if advisory != 15: 
        print('MOOOOOVE')
        with xpc.XPlaneConnect() as client:
            client.sendTEXT("DESCEND", 50, -1)
    
def acas_listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    acas_sub = rospy.Subscriber('/acasx/advisory', Int64, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    acas_listener()
