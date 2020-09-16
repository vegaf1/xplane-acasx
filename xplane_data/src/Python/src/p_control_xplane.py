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

#pygame getch to get user input
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




#publisher for ownship position to acasx
ownship_pub = rospy.Publisher('/ownship/position', position, queue_size=10)
#publisher for the ai aircraft position to acas x
ai_aircraft_pub = rospy.Publisher('/ai_aircraft/position', ai_aircraft, queue_size=10)

#initialize pygame
pygame.init()

#initialize pygame window
pygame.display.set_mode()

#P controller gain
kp = 0.5
def callback(data):
  
    advisory= data.data

    with xpc.XPlaneConnect() as client:
	# if advisory is zero, have the vehicle climb
        if advisory==0:

            print('Aircraft Climb')
            ctrl_up = [0.6, 0, 0, 1, 0, 0, 0]
            client.sendCTRL(ctrl_up)
            sleep(0.01)
            client.sendTEXT("Aircraft Climb", 50, -1)
            sleep(0.01)
            advisory = -1
            

	#other advisories acas may generate

        # while advisory==15: 
        #     print('Aircraft Steady')
        #     sleep(0.01)
        #     client.sendTEXT("Aircraft steady", 50, -1)
        #     sleep(0.01)
        #     advisory = -1
        #     break


            

    #     if advisory==15:
    #         print('Aircraft steady')
    #         ctrl_steady = [0.4, 0, 0, 1, 0, 0, 0]
    #         client.sendCTRL(ctrl_steady)
    #         sleep(0.01)
    #         client.sendTEXT("Aircraft Steady", 50, -1)
    #         sleep(0.01)
    #         advisory = -1

        


  


def monitor():
    # initialize ros node
    rospy.init_node('data_publisher', anonymous=True)

    rate = rospy.Rate(10)
    controller_enabled = 0
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
        print("sending latitudinal control")
        client.sendCTRL(ctrl2)
        sleep(10)
	# latitudinal control 
        ctrl3 = [0.4, 0, 0, 1, 0, 0, 1]
        print("leveling out")
        client.sendCTRL(ctrl3)
        sleep(10)
        print("speed forward")
        ctrl4 = [0.4, 0, 0, 1, 0, 0, 0]
        client.sendCTRL(ctrl4)
        sleep(20)
        print("Altitude HOLD")

	#position datarefs
        pos_drefs = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z"]
	#obtain datarefs from xplane
        pos_values = client.getDREFs(pos_drefs)

        ownship_x = pos_values[0][0]
        ownship_y = pos_values[1][0]
        ownship_z = pos_values[2][0]

        print('ownship x: ', ownship_x)
        print('ownship y ', ownship_y)
        print('ownship z: ', ownship_z)

        print('AI aircraft Spawned 3 2 1, check position data')
	#spawn AI aircraft
        #Plane1
        client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z-1000)
        sleep(0.01)
        client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+600)
        sleep(0.01)
        client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y+30)
	# ai aircraft position/velocity datarefs
        drefs = ["sim/multiplayer/position/plane1_lat", "sim/multiplayer/position/plane1_lon", "sim/multiplayer/position/plane1_v_x", "sim/multiplayer/position/plane1_v_z"]
	# ownship velocity and heading datarefs
        heading_drefs = ["sim/flightmodel/position/psi", "sim/flightmodel/position/local_vx", "sim/flightmodel/position/local_vz", "sim/flightmodel/position/local_vy"]
	# ownship position datarefs
        pos_drefs = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z"]
	# ai aircraft xyz position
        ai_plane_drefs = ["sim/multiplayer/position/plane1_x","sim/multiplayer/position/plane1_y", "sim/multiplayer/position/plane1_z"]
	# time datarefs
        time_dref = ["sim/network/misc/network_time_sec"]
        

        while not rospy.is_shutdown():
            event = pygame.key.get_pressed()

            for event in pygame.event.get():
		#whenever right arrow is pressed, spawn ai aircraft
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        print('vehicle spawnned in front of aircraft!!!!')

                        
                        pos_values = client.getDREFs(pos_drefs)

                        vel_values = client.getDREFs(heading_drefs)
			#save ownship position 
                        ownship_x = pos_values[0][0]
                        ownship_y = pos_values[1][0]
                        ownship_z = pos_values[2][0]
			#save ownship velocity
                        ownship_vel_x = vel_values[1][0]
                        ownship_vel_y = vel_values[3][0]
                        ownship_vel_z = vel_values[2][0]


		
			#spawn aircraft a certain position from ownship
                        client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z-600)
                        sleep(0.01)
                        client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+600)
                        sleep(0.01)
                    
                        client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y+150)
                        sleep(0.01)
			
			#boolean to enable the p controller 
                        controller_enabled = 1

            # P Controller for Xplane to follow AI aicraft 
            sleep(0.01)
            pos_values = client.getDREFs(pos_drefs)
            sleep(0.01)
            ai_values = client.getDREFs(ai_plane_drefs)
            sleep(0.01)


            ownship_x = pos_values[0][0]
            ownship_y = pos_values[1][0]
            ownship_z = pos_values[2][0]

            ai_x = ai_values[0][0]
            ai_y = ai_values[1][0]
            ai_z = ai_values[2][0]
	    
	    #error between both ai aircraft and ownship positions
            x_error= ai_x - ownship_x
            y_error= ai_y - ownship_y
            z_error= ai_z - ownship_z


            print('x_error: ', x_error)
            print('y_error: ', y_error)
            print('z_error: ', z_error)

            u_x = (x_error * kp)/(400*5)
            u_y = (y_error * kp)/(200*5)
            u_z = (z_error * kp)/(600*5)
	    
	    # controller limits
            if u_x>0.5:
                u_x =0.5
            if u_x<-0.5:
                u_x =-0.5
            if u_y>0.5:
                u_y =0.5
            if u_y<-0.5:
                u_y =-0.5

            print('x_error: ', u_x)
            print('y_error: ', u_y)
            print('z_error: ', u_z)

    
            print("Aircraft controller")
                

            #Aircraft Controller

            if controller_enabled==1:
		# ownship input from controller 
                ctrl_right = [0.4, u_x, 0, 0.8, 0, 0, 0]
                client.sendCTRL(ctrl_right)


            sleep(0.01)
            posi = client.getPOSI()
            sleep(0.01)
            ctrl = client.getCTRL()
            sleep(0.01)

            #save current aircraft positions
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
