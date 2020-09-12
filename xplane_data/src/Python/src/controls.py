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

        print "Switching dataref"
        auto_ai = "sim/operation/override/override_plane_ai_autopilot"
        client.sendDREF(auto_ai, 1)

        # Set position of the player aircraft
        print "Setting position"
        #       Lat     Lon         Alt   Pitch Roll Yaw Gear
        posi = [37.524, -122.06899, 2500, 0,    0,   0,  1]
        client.sendPOSI(posi)
        
        # Set position of a non-player aircraft
        print "Setting NPC position"
        #       Lat       Lon         Alt   Pitch Roll Yaw Gear
        posi = [37.52465, -122.06899, 2500, 0,    20,   0,  1]
        client.sendPOSI(posi, 1)

        sleep(5)

        # Set angle of attack, velocity, and orientation using the DATA command
        print "Setting orientation"
        data = [\
            [18,   0, -998,   0, -998, -998, -998, -998, -998],\
            [ 3, 130,  130, 130,  130, -998, -998, -998, -998],\
            [16,   0,    0,   0, -998, -998, -998, -998, -998]\
            ]
        client.sendDATA(data)

        sleep(5)

        # Set control surfaces and throttle of the player aircraft using sendCTRL

        #while True: 

        print "Setting controls"
        ctrl = [1.3083007388559054e-06, -2.6579946279525757e-05, 5.7890447351383045e-06, 1, 0, 0, 0]
        #values = [0.0F, 0.0F, 0.0F, 0.8F, 0.0F, 0.0F]
        client.sendCTRL(ctrl,0)



        sleep(2)

        print "Setting controls AI Aircraft"
        #ctrl2 = [0.0, 0.0, 0.0, 0.8, 0.0, 0.0]
        client.sendCTRL(ctrl,1)

        sleep(2)





        # # Pause the sim
        # print "Pausing"
        # client.pauseSim(True)
        # sleep(2)

        # # Toggle pause state to resume
        # print "Resuming"
        # client.pauseSim(False)

        # Stow landing gear using a dataref

        # Let the sim run for a bit.
        sleep(10)

        # Make sure gear was stowed successfully
        #gear_status = client.getDREF(gear_dref)
        # if gear_status[0] == 0:
        #     print "Gear stowed"
        # else:
        #     print "Error stowing gear"

        print "End of Python client example"
        raw_input("Press any key to exit...")

if __name__ == "__main__":
    ex()

