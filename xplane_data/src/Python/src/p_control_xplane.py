#!/usr/bin/env python
import sys
from time import sleep
import rospy

import xpc

from xplane_data.msg import position
from xplane_data.msg import ai_aircraft
from std_msgs.msg import Int64
#from std_msgs.msg import Float64

import os
import pygame

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

#ownship at:
#X: 
#Y:
#Z: 

global client
global advisory
advisory = -1





ownship_pub = rospy.Publisher('/ownship/position', position, queue_size=10)
ai_aircraft_pub = rospy.Publisher('/ai_aircraft/position', ai_aircraft, queue_size=10)
#x_error_pub = rospy.Publisher('/xplane/x_error', ai_aircraft, queue_size=10)

pygame.init()

pygame.display.set_mode()

#P controller gain
kp = 0.5
def callback(data):
    #print('in the callback')
    #global advisory
    #advisory = -1

    #print('in here')
    advisory= data.data
    #print(advisory)
    with xpc.XPlaneConnect() as client:

        #advisory= data.data
        #print(advisory)
        
    #     #print('advisory from callback: ', advisory)
        

        if advisory==0:
            #advisory= data.data
            #print(advisory)
            print('Aircraft Climb')
            ctrl_up = [0.6, 0, 0, 1, 0, 0, 0]
            client.sendCTRL(ctrl_up)
            sleep(0.01)
            client.sendTEXT("Aircraft Climb", 50, -1)
            sleep(0.01)
            advisory = -1
            

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

        

    #print(advisory)
  


def monitor():
    

    #ownship_pub = rospy.Publisher('/ownship/position', position, queue_size=10)
    #ai_aircraft_pub = rospy.Publisher('/ai_aircraft/position', ai_aircraft, queue_size=10)
    
    


    rospy.init_node('data_publisher', anonymous=True)
    #rate = rospy.Rate(5)
    rate = rospy.Rate(10)
    controller_enabled = 0

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

        #pos_drefs = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z"]
        #pos_values = client.getDREFs(pos_drefs)

        #ownship_x = pos_values[0][0]
        #ownship_y = pos_values[1][0]
        #ownship_z = pos_values[2][0]

        #print('ownship x: ', ownship_x)
        #print('ownship y ', ownship_y)
        #print('ownship z: ', ownship_z)


        #client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z+40)
        #sleep(3)
        #client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+40)
        #sleep(3)
        #client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y)
        #sleep(3)

        #client.sendDREF("sim/multiplayer/position/plane2_z",  ownship_z)
        #sleep(3)
        #client.sendDREF("sim/multiplayer/position/plane2_x", ownship_x )
        #sleep(3)
        #client.sendDREF("sim/multiplayer/position/plane2_y", ownship_y)
        #sleep(3)
        

        #print("AI vehicle spawned")

        #sleep(5)

        print("Starting encounter")

        #client.sendTEXT("Hello from Python", 50, -1)

        ctrl = [0, 0, 0, 1, 0, 0, 0]
        print("sending throttle control")


        #while True: 
            #print("settings commands")

        client.sendCTRL(ctrl)
        
        sleep(30)

        


        #heading = client.getDREF('/sim/flightmodel/position/psi')
        #v_ew = client.getDREF('/sim/flightmodel/position/local_vx')
        #v_ns = client.getDREF('/sim/flightmodel/position/local_vz')

        #print(heading, v_ew, v_ns)

        ctrl2 = [0.2, 0, 0, 1, 0, 0, 0]
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
        # client.sendDREF("sim/cockpit/autopilot/autopilot_state", 1048576)
        # sleep(0.01)
        # client.sendDREF("sim/cockpit/autopilot/autopilot_state", 16)
        # sleep(0.01)
        # client.sendDREF("sim/cockpit/autopilot/autopilot_state", 1)
        # sleep(0.01)

        # client.sendDREF("sim/cockpit/autopilot/autopilot_mode", 2)

        # sleep(5)
        print("Altitude HOLD")
        #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 32)

        #sleep(5)
        #print("Turning right")
        #ctrl5 = [0.4, 0.2, 0, 1, 0, 0, 0]
        #client.sendCTRL(ctrl5)
        #sleep(5)
        #print("levelout")
        #ctrl6 = [0.4 ,0, 0, 1, 0, 0, 0]
        #client.sendCTRL(ctrl6)
        #sleep(20)

        pos_drefs = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z"]
        pos_values = client.getDREFs(pos_drefs)

        ownship_x = pos_values[0][0]
        ownship_y = pos_values[1][0]
        ownship_z = pos_values[2][0]

        print('ownship x: ', ownship_x)
        print('ownship y ', ownship_y)
        print('ownship z: ', ownship_z)

        print('AI aircraft Spawned 3 2 1, check position data')

        #sleep(3)
        #Plane1
        client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z-1000)
        sleep(0.01)
        client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+600)
        sleep(0.01)
        client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y+30)
        # #Plane2
        # client.sendDREF("sim/multiplayer/position/plane2_z", ownship_z+100)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane2_x", ownship_x+500)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane2_y", ownship_y)
        # #Plane3
        # client.sendDREF("sim/multiplayer/position/plane3_z", ownship_z-10)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane3_x", ownship_x-50)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane3_y", ownship_y)
        # #Plane4
        # client.sendDREF("sim/multiplayer/position/plane4_z", ownship_z+50)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane4_x", ownship_x+300)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane4_y", ownship_y)
        # #Plane5
        # client.sendDREF("sim/multiplayer/position/plane5_z", ownship_z+200)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane5_x", ownship_x+400)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane5_y", ownship_y)
        # #Plane6
        # client.sendDREF("sim/multiplayer/position/plane6_z", ownship_z-200)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane6_x", ownship_x-400)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane6_y", ownship_y)
        # #Plane7
        # client.sendDREF("sim/multiplayer/position/plane7_z", ownship_z+90)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane7_x", ownship_x+400)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane7_y", ownship_y)
        # #Plane8
        # client.sendDREF("sim/multiplayer/position/plane8_z", ownship_z+320)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane8_x", ownship_x+400)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane8_y", ownship_y)
        # #Plane9
        # client.sendDREF("sim/multiplayer/position/plane9_z", ownship_z+200)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane9_x", ownship_x+50)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane9_y", ownship_y)
        # #Plane10
        # client.sendDREF("sim/multiplayer/position/plane10_z", ownship_z+200)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane10_x", ownship_x+50)
        # sleep(0.01)
        # client.sendDREF("sim/multiplayer/position/plane10_y", ownship_y+50)

        drefs = ["sim/multiplayer/position/plane1_lat", "sim/multiplayer/position/plane1_lon", "sim/multiplayer/position/plane1_v_x", "sim/multiplayer/position/plane1_v_z"]

        heading_drefs = ["sim/flightmodel/position/psi", "sim/flightmodel/position/local_vx", "sim/flightmodel/position/local_vz", "sim/flightmodel/position/local_vy"]

        pos_drefs = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z"]

        ai_plane_drefs = ["sim/multiplayer/position/plane1_x","sim/multiplayer/position/plane1_y", "sim/multiplayer/position/plane1_z"]

        time_dref = ["sim/network/misc/network_time_sec"]
        

    #with xpc.XPlaneConnect() as client:
        while not rospy.is_shutdown():
            event = pygame.key.get_pressed()

            for event in pygame.event.get():

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

                        #ctrl_ai = client.getCTRL(1)
                        #print(ctrl_ai)


                        client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z-600)
                        sleep(0.01)
                        client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+600)
                        sleep(0.01)
                        #client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x+600)
                        #sleep(0.01)
                        client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y+150)
                        sleep(0.01)
                        #client.sendDREF("sim/multiplayer/position/plane1_z", ownship_z)
                       
                        #client.sendDREF("sim/multiplayer/position/plane1_x", ownship_x)
                    
                        #client.sendDREF("sim/multiplayer/position/plane1_y", ownship_y)

                        #client.sendDREF("sim/multiplayer/position/plane1_v_x", ownship_vel_x)

                        #client.sendDREF("sim/multiplayer/position/plane1_v_y", ownship_vel_y)

                        #client.sendDREF("sim/multiplayer/position/plane1_v_z", ownship_vel_z)

                        controller_enabled = 1

            # P Controller for Xplane to follow AI aicraft 
            sleep(0.01)
            pos_values = client.getDREFs(pos_drefs)
            sleep(0.01)
            ai_values = client.getDREFs(ai_plane_drefs)
            sleep(0.01)
            # ctrl_ai = client.getCTRL(1)
            # print(ctrl_ai)
            # sleep(0.01)

            ownship_x = pos_values[0][0]
            ownship_y = pos_values[1][0]
            ownship_z = pos_values[2][0]

            ai_x = ai_values[0][0]
            ai_y = ai_values[1][0]
            ai_z = ai_values[2][0]

            x_error= ai_x - ownship_x
            y_error= ai_y - ownship_y
            z_error= ai_z - ownship_z

            #print('ai_x: ', ai_x)
            #print('ai_y: ', ai_y)
            #print('ai_z: ', ai_z)

            print('x_error: ', x_error)
            print('y_error: ', y_error)
            print('z_error: ', z_error)

            u_x = (x_error * kp)/(400*5)
            u_y = (y_error * kp)/(200*5)
            u_z = (z_error * kp)/(600*5)

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




            #print('x error: ', u_x)
            #print('y error: ', u_y)
            #print('z error: ', u_z)

            # if u_y < 0:
            #     #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 0)
            #     print("Turning down")
            #     ctrl_down = [u_y, 0, 0, 0.5, 0, 0, 0]
            #     client.sendCTRL(ctrl_down)

            # if u_y > 0: 
            #     print('Moving up')
            #     #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 0)
            #     #ctrl_up = [0.8, 0, 0, 1, 0, 0, 0]
            #     ctrl_up = [u_y, 0, 0, 1, 0, 0, 1]
            #     client.sendCTRL(ctrl_up)

            # if u_x < 0:
                
            print("Aircraft controller")
                #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 0)

            #Aircraft Controller

            if controller_enabled==1:

                ctrl_right = [0.4, u_x, 0, 0.8, 0, 0, 0]
                client.sendCTRL(ctrl_right)


            # if u_x > 0:
            #     print("Turning left")
            #     #client.sendDREF("sim/cockpit/autopilot/autopilot_state", 0)
            #     ctrl_left = [u_y, u_x, 0, 1, 0, 0, 0]
            #     client.sendCTRL(ctrl_left)

            # #print('x error: ', x_error)
            # print('y_error: ', y_error)
            # print('z_error: ', z_error)

            sleep(0.01)
            posi = client.getPOSI()
            sleep(0.01)
            ctrl = client.getCTRL()
            sleep(0.01)

            # if advisory==0:
            #     print('Aircraft Climb')
            #     ctrl_up = [0.4, 0, 0, 1, 0, 0, 0]
            #     client.sendCTRL(ctrl_up)
            #     sleep(0.01)
            #     client.sendTEXT("Aircraft Climb", 50, -1)
            #     sleep(0.01)
                

            # if advisory==15:
            #     print('Aircraft steady')
            #     ctrl_steady = [0.4, 0, 0, 1, 0, 0, 0]
            #     client.sendCTRL(ctrl_steady)
            #     sleep(0.01)
            #     client.sendTEXT("Aircraft Steady", 50, -1)
            #     sleep(0.01)
            

            # if advisory==5:
            #     print('Aircraft Descend')
            #     ctrl_down = [0.1, 0, 0, 1, 0, 0, 0]
            #     client.sendCTRL(ctrl_down)
            #     sleep(0.01)
            #     client.sendTEXT("Aircraft Descend", 50, -1)
            #     break

            # Velocity Calculation
            # ownship_pos1 = client.getDREFs(ai_plane_drefs)
            # time1 = client.getDREFs(time_dref)

            # ownship_pos1_x = ownship_pos1[0][0]
            # ownship_pos1_y = ownship_pos1[1][0]
            # ownship_pos1_z = ownship_pos1[2][0]
            # ownship_time1 = time1[0][0]

            # sleep(0.05)

            # ownship_pos2 = client.getDREFs(ai_plane_drefs)
            # time2 = client.getDREFs(time_dref)

            # ownship_pos2_x = ownship_pos2[0][0]
            # ownship_pos2_y = ownship_pos2[1][0]
            # ownship_pos2_z = ownship_pos2[2][0]
            # ownship_time2 = time2[0][0]

            # #sleep(0.05)

            # ownship_vel_x = abs(ownship_pos2_x-ownship_pos1_x)/abs(ownship_time2-ownship_time1)
            # ownship_vel_y = abs(ownship_pos2_y-ownship_pos1_y)/abs(ownship_time2-ownship_time1)
            # ownship_vel_z = abs(ownship_pos2_z-ownship_pos1_z)/abs(ownship_time2-ownship_time1)

            # print('Velocity in X Ownship: ', ownship_vel_x)
            # print('Velocity in Y Ownship: ', ownship_vel_y)
            # print('Velocity in Z Ownship: ', ownship_vel_z)




            # heading = client.getDREF('/sim/flightmodel/position/psi')
            # v_ew = client.getDREF('/sim/flightmodel/position/local_vx')
            # v_ns = client.getDREF('/sim/flightmodel/position/local_vz')
       
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
            
            #print(values)
            #print("The latitude is " + str(values[0][0]), "The longitude is " + str(values[1][0]))
            #sleep(0.01)
            ai_msg.latitude = values[0][0]
            ai_msg.longitude = values[1][0]
            ai_msg.v_ew = values[3][0]
            ai_msg.v_ns = values[2][0]
            
            ai_msg.altitude = posi[2]
            #rospy.loginfo(ownship_msg)
            #rospy.loginfo(ai_msg)

            ownship_pub.publish(ownship_msg)
            ai_aircraft_pub.publish(ai_msg)
            

            
            #if(advisory ==15):
                #print('Aircraft is safe')
            rate.sleep()

            #print "Loc: (%4f, %4f, %4f) Aileron:%2f Elevator:%2f Rudder:%2f\n"\
            #   % (posi[0], posi[1], posi[2], ctrl[1], ctrl[0], ctrl[2])
            #time.sleep(0.01)


if __name__ == "__main__":
    try: 
        monitor()
    except rospy.ROSInterruptException: pass
