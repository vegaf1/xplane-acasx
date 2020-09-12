from time import sleep
import xpc

def ex():

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

        #print "Setting position"
        #       Lat     Lon         Alt   Pitch Roll Yaw Gear
        #posi = [37.524, -122.06899, 2500, 0,    0,   0,  1]
        #client.sendPOSI(posi)

        #while True: 


            #ctrl = client.getCTRL(0)

            #print(ctrl)

            #sleep(.01)
    
        #print client.getDREF("sim/operation/override/override_plane_ai_autopilot")
        #print client.getDREF("sim/operation/override/override_flightcontrol")

        #client.sendDREF("sim/operation/override/override_flightcontrol", 1)
        #client.sendDREF("sim/operation/override/override_plane_ai_autopilot", 1)
        #print client.getDREF("sim/operation/override/override_plane_ai_autopilot")
        #print client.getDREF("sim/operation/override/override_flightcontrol")
        #print "Setting controls"
        #ctrl = [1.3083007388559054e-06, -2.6579946279525757e-05, 5.7890447351383045e-06, 1, 0, 0, 0]

        #posi = client.getPOSI(0)
        #print("physics simulation stopped")
        #client.pauseSim(True) # Pause simulation
    

        #print("sending plane in 3 2 1")

        #sleep(3)

        #client.sendDREF("/sim/operation/override/override_plane_ai_autopilot", 1)

        #client.sendPOSI(posi,1)
        #ctrl0 = [0, 0, 0, 0, 0, 0, 0]
        #client.sendCTRL(ctrl0,1)

        #print("Enemy vehicle spawned")

        #sleep(10)

        #print("physics simulation back")

        #client.pauseSim(False)

        #print("small wait")
        #sleep(5)
        #print("spawning ai aircraft")
        #client.sendDREF("sim/multiplayer/position_plane1_x", 2)
        #sleep(0.01)
        #client.sendDREF("sim/multiplayer/position_plane1_y", 0)
        #sleep(0.01)
        #client.sendDREF("sim/multiplayer/position_plane1_z", 0)
        #sleep(5)

        #client.sendDREF("sim/cockpit/autopilot/autopilot_mode", 2)

        #sleep(20)

        print("Starting encounter")

        ctrl = [0, 0, 0, 1, 0, 0, 0]
        print("sending throttle control")
        #while True: 
            #print("settings commands")

        client.sendCTRL(ctrl)
        #client.sendCTRL(ctrl,1)
        sleep(30)
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
        sleep(5)
        client.sendDREF("sim/cockpit/autopilot/autopilot_state", 1048576)
        #sleep(0.01)
        client.sendDREF("sim/cockpit/autopilot/autopilot_state", 16)
        #sleep(0.01)
        client.sendDREF("sim/cockpit/autopilot/autopilot_state", 1)
        #sleep(0.01)

        client.sendDREF("sim/cockpit/autopilot/autopilot_mode", 2)

        sleep(20)
        print("Altitude HOLD")
        client.sendDREF("sim/cockpit/autopilot/autopilot_state", 32)

        sleep(20)
        print("Turning right")
        ctrl5 = [0.4, 0.4, 0, 1, 0, 0, 0]
        client.sendCTRL(ctrl5)
        sleep(20)
        print("levelout")
        ctrl6 = [0.4 ,0, 0, 1, 0, 0, 0]
        client.sendCTRL(ctrl6)

        drefs = ["sim/multiplayer/position/plane6_lat", "sim/multiplayer/position/plane6_lon"]
        while True: 

    		values = client.getDREFs(drefs)
    		sleep(0.01)
    		#print(values)
    		print("The latitude is " + str(values[0][0]), "The longitude is " + str(values[1][0]))
    		sleep(0.01)


      

if __name__ == "__main__":
    ex()


