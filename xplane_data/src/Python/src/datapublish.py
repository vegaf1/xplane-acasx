#!/usr/bin/env python
import sys
from time import sleep
import rospy

import xpc

from xplane_data.msg import position
from xplane_data.msg import ai_aircraft
from std_msgs.msg import Int64

import os
import pygame

#pygame code to get the user input from the window
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

global client

#used for the advisory acas generates
global advisory

#initialize advisory
advisory = -1

ownship_pub = rospy.Publisher('/ownship/position', position, queue_size=10) # publisher for the ownship position to acasx
ai_aircraft_pub = rospy.Publisher('/ai_aircraft/position', ai_aircraft, queue_size=10) #publisher for the ai aircraft position to acasx 

pygame.init() # initialize pygame

pygame.display.set_mode() #initialize pygame window



def callback(data):

    advisory= data.data
    print(advisory)
    with xpc.XPlaneConnect() as client:
	
	#if advisory is 0, have the vehicle climb
        if advisory==0:
            print('Aircraft Climb')
            ctrl_up = [0.6, 0, 0, 1, 0, 0, 0]
            client.sendCTRL(ctrl_up)
            sleep(0.01)
            client.sendTEXT("Aircraft Climb", 50, -1)
            sleep(0.01)
            advisory = -1

def monitor():
    #initialize ros node
    rospy.init_node('data_publisher', anonymous=True)
    rate = rospy.Rate(40)
    
    #subscriber for acasx advisory
    acas_sub = rospy.Subscriber('/acasx/advisory', Int64, callback)

    print "X-Plane Connect example script"
    print "Setting up simulation"
    with xpc.XPlaneConnect() as client:
        # Verify connection
        try:
            # If X-Plane does not respond to the request, a timeout error
            # will be raised.
            client.getDREF("sim/test/test_float")
        except:
            print "Error establishing connection to X-Plane."
            print "Exiting..."
            return
        print("Starting encounter")
        #ctrl = [latitudinal, longitudinal, rudder, throttle, gear, flaps]

	#set throttle to 1
        ctrl = [0, 0, 0, 1, 0, 0, 0]
        print("sending throttle control")

        client.sendCTRL(ctrl)
        
        sleep(30)
	#longitudinal control
        ctrl2 = [0.2, 0, 0, 1, 0, 0, 0]
	#latitudinal control
        print("sending latitudinal control")
        client.sendCTRL(ctrl2)
        sleep(10)
        ctrl3 = [0.4, 0, 0, 1, 0, 0, 1]
        print("leveling out")
        client.sendCTRL(ctrl3)
        sleep(10)
        print("speed forward")
        ctrl4 = [0.4, 0, 0, 1, 0, 0, 0]
        client.sendCTRL(ctrl4)
        sleep(20)
        print("Altitude HOLD")
        print("levelout")
        ctrl6 = [0.4 ,0, 0, 1, 0, 0, 0]
        client.sendCTRL(ctrl6)
        sleep(30)

	#position datarefs
        pos_drefs = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z"]
	#obtain the datarefs from xplane
        pos_values = client.getDREFs(pos_drefs)

	#Datarefs to enable if you want to turn on the autopilot
	#Aircraft does not react much to change but is more stable in the air

        #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 1048576)
        #sleep(0.01)
        #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 16)
        #sleep(0.01)
        #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 1)
        #sleep(0.01)

        #client.sendDREF("sim/cockpit/autopilot/autopilot_mode", 2)

        ownship_x = pos_values[0][0]
        ownship_y = pos_values[1][0]
        ownship_z = pos_values[2][0]

        print('ownship x: ', ownship_x)
        print('ownship y ', ownship_y)
        print('ownship z: ', ownship_z)

        print('AI aircraft Spawned 3 2 1, check position data')

        #spawn ai aircraft1
        client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z-200)
        sleep(0.01)
        client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+10)
        sleep(0.01)
        client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y+10)
 
	# ai aicraft position/velocity datarefs 
        drefs = ["sim/multiplayer/position/plane1_lat", "sim/multiplayer/position/plane1_lon", "sim/multiplayer/position/plane1_v_x", "sim/multiplayer/position/plane1_v_z"]
	# ownship velocity and heading datarefs
        heading_drefs = ["sim/flightmodel/position/psi", "sim/flightmodel/position/local_vx", "sim/flightmodel/position/local_vz", "sim/flightmodel/position/local_vy"]
	# ownship position datarefs
        pos_drefs = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z"]
	# ai aircraft xyz position
        ai_plane_drefs = ["sim/multiplayer/position/plane1_x","sim/multiplayer/position/plane1_y", "sim/multiplayer/position/plane1_z"]
	# time dataref
        time_dref = ["sim/network/misc/network_time_sec"]
        
        while not rospy.is_shutdown():
            event = pygame.key.get_pressed()

            for event in pygame.event.get():
		# whenever right arrow pressed, spawn ai aircraft 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        print('vehicle spawnned in front of aircraft!!!!')

                        
                        pos_values = client.getDREFs(pos_drefs)

                        vel_values = client.getDREFs(heading_drefs)

                        ownship_x = pos_values[0][0]
                        ownship_y = pos_values[1][0]
                        ownship_z = pos_values[2][0]

                        ownship_vel_x = vel_values[1][0]
                        ownship_vel_y = vel_values[3][0]
                        ownship_vel_z = vel_values[2][0]

                        ctrl_ai = client.getCTRL(1)
                        print(ctrl_ai)
			
			# spawn ai aicraft at a certain position from ownship
                        client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z+10)
                       
                        client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+100)
                    
                        client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y-10)

                        client.sendDREF("sim/multiplayer/position/plane1_v_x", ownship_vel_x)

                        client.sendDREF("sim/multiplayer/position/plane1_v_y", ownship_vel_y)

                        client.sendDREF("sim/multiplayer/position/plane1_v_z", ownship_vel_z)

 	    
            #save ownship and ai aircraft positions
            posi = client.getPOSI()
            sleep(0.01)
            ctrl = client.getCTRL()
            sleep(0.01)      
            ownship_msg = position()
            ai_msg = ai_aircraft()
            heading_values = client.getDREFs(heading_drefs)
            ownship_msg.latitude = posi[0]
            ownship_msg.longitude = posi[1]
            ownship_msg.altitude = posi[2]
            ownship_msg.aileron = ctrl[1]
            ownship_msg.elevator = ctrl[0]
            ownship_msg.rudder = ctrl[2]

            ownship_msg.heading = heading_values[0][0]
            ownship_msg.v_ew = heading_values[2][0]
            ownship_msg.v_ns = heading_values[1][0]


            values = client.getDREFs(drefs)
            sleep(0.01)
            
            ai_msg.latitude = values[0][0]
            ai_msg.longitude = values[1][0]
            ai_msg.v_ew = values[3][0]
            ai_msg.v_ns = values[2][0]
            
            ai_msg.altitude = posi[2]
	    #publish the ownship and ai aircraft positions to acasx
            ownship_pub.publish(ownship_msg)
            ai_aircraft_pub.publish(ai_msg)

            rate.sleep()

if __name__ == "__main__":
    try: 
        monitor()
    except rospy.ROSInterruptException: pass
