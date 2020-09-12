#!/usr/bin/env python 

#This file will run over Input.json files, playing out the encoutner in real time. This Input.json is analogous to a stream of sensor messages, and can be adapted to your live systems as such

# You can change between real-time and simulation time with the simulate_delay variable


import ctypes
import json
import time
import sys
import os
import glob
import rospy 
from std_msgs.msg import String
from acasx.msg import position
from acasx.msg import ai_aircraft
from std_msgs.msg import Int64
#from std_msgs.msg import Bool 


#from sensor_msgs.msg import NavSatFix

 
#Configuration
simulate_delay = False

verbosity = 2 #0=none, 1=ReportMsgs only, 2=ReportMsgs and Input Messages
recv_buffer_size = 600000 #A json-writeout string buffer size, this is the max expected return size for json reports from libacas

log_folder = './logs' #where the output logs are saved
if not os.path.exists(log_folder):
	os.makedirs(log_folder)

is_windows = sys.platform.startswith('win')
if is_windows:
	wrapper_name = '../LibsXu.Wrapper/libsxu_wrapper.dll'
else:
	wrapper_name = '../LibsXu.Wrapper/libsxu_wrapper.so' #shared library used in the code
	
paramsfile_path = b'../../data_files/paramsfile_sxu_compressed.txt' #parameter file utilized
runtimefile_path = b'../lib/julia/sxu_v2r0.ji'
	
#static/global handles
initialized = False
libacas = None 
lastTime = None

acas_pub = rospy.Publisher('/acasx/advisory', Int64, queue_size=10)

def callback(data):
	global longitude
	global latitude
	global altitude
	global ownship_v_ns
	global ownship_v_ew
	global heading
	

	longitude = data.longitude
	latitude = data.latitude
	altitude = data.altitude
	heading = (data.heading)*((3.14159)/180)
	ownship_v_ns = data.v_ns*1.94
	ownship_v_ew = data.v_ew *1.94
	#ai_v_ns = -1*ownship_v_ns
	#ai_v_ew = -1*ownship_v_ew
	# print('Longitude', longitude)
	# print('Latitude', latitude)
	# print('Altitude', altitude)

def callback2(data):
	global ai_longitude
	global ai_latitude
	global ai_altitude
	global ai_v_ns
	global ai_v_ew
	ai_longitude = data.longitude
	ai_latitude = data.latitude
	ai_altitude = data.altitude
	ai_v_ns = data.v_ns*1.94
	ai_v_ew = data.v_ew*1.94

	

	# print('Longitude', longitude2)
	# print('Latitude', latitude2)
	# print('Altitude', altitude2)
#This function processes each message and generates a corresponding ACAS Update call
def ProcessMessage(sXu_idx, msg, message_time, message_type, libacas):
	
	#if verbosity == 2: 
		#print("Processing message type ", message_type, ", at t=", message_time)
	
	report_time = message_time # in live applications this would be a reading of the current wall clock time (i.e. time of processing)
	toa = message_time # "Time of Applicability". this value represents the time of reception, or time of measurment (if available)
	sub = msg['acas_sxu_v2r0'][message_type] #nested submessage


	if message_type == 'heading_obs':
		#libacas.ReceiveOwnshipHeading(sXu_idx, sub['heading_true_rad'], sub['heading_degraded'], toa, report_time)
		libacas.ReceiveOwnshipHeading(sXu_idx, heading , sub['heading_degraded'], toa, report_time)
	elif message_type == 'baro_alt_obs':
		#libacas.ReceiveOwnshipBaroAlt(sXu_idx, sub['baro_alt_ft'], toa, report_time)
		libacas.ReceiveOwnshipBaroAlt(sXu_idx, altitude, toa, report_time)
	elif message_type == 'wgs84_obs':
		clean_geo_alt_ft = float('nan') if isinstance(sub['geo_alt_ft'], str) else sub['geo_alt_ft']
		clean_geo_alt_rate_fps = float('nan') if isinstance(sub['geo_alt_rate_fps'], str) else sub['geo_alt_rate_fps']
		#libacas.ReceiveOwnWGS84(sXu_idx, sub['lat_deg'], sub['lon_deg'], sub['vel_ew_kts'], sub['vel_ns_kts'], sub['nacp'], sub['nacv'], toa, clean_geo_alt_ft, clean_geo_alt_rate_fps, report_time)
		libacas.ReceiveOwnWGS84(sXu_idx, latitude, longitude, ownship_v_ew , ownship_v_ns , sub['nacp'], sub['nacv'], toa, altitude, clean_geo_alt_rate_fps, report_time)
		#libacas.ReceiveOwnWGS84(sXu_idx,latitude, longitude, sub['vel_ew_kts'], sub['vel_ns_kts'], sub['nacp'], sub['nacv'], toa, altitude, clean_geo_alt_rate_fps, report_time)
	elif message_type == 'airspeed_obs':
		clean_airspeed_kts = float('nan') if isinstance(sub['airspeed_kts'], str) else sub['airspeed_kts']
		libacas.ReceiveAirspeedObservation(sXu_idx, toa, clean_airspeed_kts, report_time)
	elif message_type == 'ownship_discretes':
		libacas.ReceiveDiscretes(sXu_idx , toa, sub['address'], sub['opflg'], sub['manual_SL'], sub['own_ground_display_mode_on'], sub['on_surface'], sub['is_coarsely_quant'], sub['turn_rate_limit_rad'], sub['vert_rate_limit_fps'], sub['turn_inhibited'], sub['climb_inhibited'], report_time)
	elif message_type == 'airborne_position_report':
		libacas.ReceiveAirbornePosition(sXu_idx, toa, sub['address'], sub['rebroadcast'], sub['non_icao'], sub['lat_deg'], sub['lon_deg'], sub['baro_alt_ft'], sub['quant_ft'], sub['nic'], sub['is_alt_geo_hae'], report_time)
		#libacas.ReceiveAirbornePosition(sXu_idx, toa, sub['address'], sub['rebroadcast'], sub['non_icao'], latitude2, longitude2, altitude2, sub['quant_ft'], sub['nic'], sub['is_alt_geo_hae'], report_time)
	elif message_type == 'airborne_velocity_report':
		libacas.ReceiveAirborneVelocity(sXu_idx, toa, sub['address'], sub['rebroadcast'], sub['non_icao'], sub['vel_ns_kts'], sub['vel_ew_kts'], sub['nic'], report_time)
	elif message_type == 'mode_status_report':
		libacas.ReceiveModeStatus(sXu_idx, toa, sub['address'], sub['rebroadcast'], sub['non_icao'], sub['adsb_version'], sub['nacp'], sub['nacv'], sub['sil'], sub['sda'], report_time)
	elif message_type == 'capability_report':
		libacas.ReceiveCapabilityReport(sXu_idx, toa, sub['address'], sub['adsb_version'], sub['ca_operational'], sub['daa'], sub['priority'], sub['sense'], sub['type_capability'], report_time)
	elif message_type == 'airborne_uat_report':
		libacas.ReceiveUAT (sXu_idx, toa, sub['address'], sub['non_icao'], sub['lat_deg'], sub['lon_deg'], sub['vel_ns_kts'], sub['vel_ew_kts'], sub['baro_alt_ft'], sub['is_alt_geo_hae'], sub['quant_ft'], sub['nic'], report_time)
	elif message_type == 'xu_atar_report':
		clean_covariance_horiz_ft_fps = [float('nan') if isinstance(x, str) else x for x in sub['covariance_horiz_ft_fps']]
		clean_covariance_vert_ft_fps = [float('nan') if isinstance(x, str) else x for x in sub['covariance_vert_ft_fps']]
		covariance_horiz_ft_fps = (ctypes.c_double * 16)(*clean_covariance_horiz_ft_fps)
		covariance_vert_ft_fps = (ctypes.c_double * 4)(*clean_covariance_vert_ft_fps)
		libacas.ReceiveXuAtar(sXu_idx, sub['external_id'], sub['track_status'], toa, sub['ground_range_ft'], sub['azimuth_rad'], sub['ground_range_rate_fps'], sub['cross_range_rate_fps'], covariance_horiz_ft_fps, sub['rel_altitude_ft'], sub['rel_altitude_rate_fps'], covariance_vert_ft_fps, report_time)
	elif message_type == 'ground_surveillance_report':
		clean_covariance_horiz_ft_fps = [float('nan') if isinstance(x, str) else x for x in sub['covariance_horiz_ft_fps']]
		clean_covariance_baro_alt_ft_fps = [float('nan') if isinstance(x, str) else x for x in sub['covariance_baro_alt_ft_fps']]
		clean_covariance_geo_hae_ft_fps = [float('nan') if isinstance(x, str) else x for x in sub['covariance_geo_hae_ft_fps']]
		covariance_horiz_ft_fps = (ctypes.c_double * 16)(*clean_covariance_horiz_ft_fps)
		covariance_baro_alt_ft_fps = (ctypes.c_double * 4)(*clean_covariance_baro_alt_ft_fps)
		covariance_geo_hae_ft_fps = (ctypes.c_double * 4)(*clean_covariance_geo_hae_ft_fps)
		clean_baro_alt_ft = float('nan') if isinstance(sub['baro_alt_ft'], str) else sub['baro_alt_ft']
		clean_baro_alt_rate_fps = float('nan') if isinstance(sub['baro_alt_rate_fps'], str) else sub['baro_alt_rate_fps']
		clean_geo_hae_ft = float('nan') if isinstance(sub['geo_hae_ft'], str) else sub['geo_hae_ft']
		clean_geo_hae_rate_fps = float('nan') if isinstance(sub['geo_hae_rate_fps'], str) else sub['geo_hae_rate_fps']
		libacas.ReceiveGroundSurveillance(sXu_idx, toa, sub['address'], sub['non_icao'], sub['external_id'], sub['track_status'], sub['lat_deg'], sub['lon_deg'], sub['vel_ew_kts'], sub['vel_ns_kts'], covariance_horiz_ft_fps, clean_baro_alt_ft, clean_baro_alt_rate_fps, covariance_baro_alt_ft_fps, clean_geo_hae_ft, clean_geo_hae_rate_fps, covariance_geo_hae_ft_fps, report_time)
	elif message_type == 'broadcast_remote_id_report':
		libacas.ReceiveBroadcastRemoteID(sXu_idx, toa, ai_latitude, ai_longitude, ai_altitude, ai_altitude, ai_v_ew, ai_v_ns , sub['nacp'], sub['nacv'], sub['gva'], sub['external_id'], report_time)
		#libacas.ReceiveBroadcastRemoteID(sXu_idx, toa, latitude, longitude, ai_altitude, ai_altitude, ownship_v_ew, ownship_v_ns , sub['nacp'], sub['nacv'], sub['gva'], sub['external_id'], report_time)
		#libacas.ReceiveBroadcastRemoteID(sXu_idx, toa, ai_latitude, ai_longitude, altitude, sub['geo_alt_hae_ft'], sub['vel_ew_kts'], sub['vel_ns_kts'], sub['nacp'], sub['nacv'], sub['gva'], sub['external_id'], report_time)
	elif message_type == 'df0':
		libacas.ReceiveDF0(sXu_idx, toa, sub['mode_s'], sub['r_slant_ft'], sub['Chi_rel_rad'], sub['baro_alt_ft'], sub['quant_ft'], sub['ri'], sub['surv_mode'], report_time)
	elif message_type == 'uf16uds30':
		libacas.ReceiveUF16UDS30(sXu_idx, toa, sub['mode_s'], sub['cvc'], sub['vrc'], sub['vsb'], sub['chc'], sub['hrc'], sub['hsb'], report_time)
	elif message_type == 'point_obstacle_report':
		libacas.ReceivePointObstacleReport(sXu_idx, toa, sub['external_id'], sub['lat_deg'], sub['lon_deg'], sub['geo_alt_hae_ft'], sub['to_be_deleted'], report_time)
	elif message_type == 'height_agl_obs':
		clean_h_ft = float('nan') if isinstance(sub['h_ft'], str) else sub['h_ft']
		libacas.ReceiveHeightAglObs(sXu_idx, toa, clean_h_ft, report_time)
	else:
		print("error, unrecognized message type: ", message_type)


def InitializeEntrypoints(): #Initalizes ACAS and the entrypoints into the DLL
	libacas = ctypes.cdll.LoadLibrary(wrapper_name)

	#define input argument types/ordering
	libacas.Initialize.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p ]
	libacas.InitializeReportingAutoName.argtypes = [ctypes.c_int, ctypes.c_char_p ]
	libacas.ReceiveOwnshipBaroAlt.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double]
	libacas.ReceiveOwnshipHeading.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_bool, ctypes.c_double, ctypes.c_double]
	libacas.ReceiveDiscretes.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint, ctypes.c_bool, ctypes.c_uint, ctypes.c_bool, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
	libacas.ReceiveGroundSurveillance.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint, ctypes.c_bool, ctypes.c_uint,ctypes.c_ubyte, ctypes.c_double, ctypes.c_double, ctypes.c_double,ctypes.c_double, ctypes.c_double * 16, ctypes.c_double, ctypes.c_double,ctypes.c_double * 4, ctypes.c_double, ctypes.c_double, ctypes.c_double * 4,ctypes.c_double]
	libacas.ReceiveXuAtar.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_double, ctypes.c_double,ctypes.c_double, ctypes.c_double, ctypes.c_double,ctypes.c_double * 16, ctypes.c_double, ctypes.c_double,ctypes.c_double * 4, ctypes.c_double]
	libacas.ReceiveOwnWGS84.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,ctypes.c_uint, ctypes.c_uint, ctypes.c_double, ctypes.c_double,ctypes.c_double, ctypes.c_double]
	libacas.ReceiveBroadcastRemoteID.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double,ctypes.c_double, ctypes.c_double, ctypes.c_double,ctypes.c_double, ctypes.c_double, ctypes.c_uint,ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double]
	libacas.ReceiveUAT.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint, ctypes.c_bool, ctypes.c_double,  ctypes.c_double,  ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_uint, ctypes.c_uint, ctypes.c_double]
	libacas.ReceiveModeStatus.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint, ctypes.c_bool, ctypes.c_bool, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double]
	libacas.ReceiveAirborneVelocity.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint,ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_double]
	libacas.ReceiveAirbornePosition.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint,ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_double]
	libacas.ReceiveHeightAglObs.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double]
	libacas.ReceivePointObstacleReport.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_double]
	libacas.ReceiveUF16UDS30.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double]
	libacas.ReceiveDF0.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_double]
	
	#not recommended for use
	libacas.ReceiveCapabilityReport.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_double]
	libacas.ReceiveAirspeedObservation.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double]

	libacas.ReportAsJSON.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p]
	
	if verbosity:
		print("Done loading entrypoints")

	return libacas


def ACASReport(sXu_idx, report_time, libacas): #AKA "Report Generation"
	json_reports = ctypes.create_string_buffer(recv_buffer_size)
	if verbosity:
		print('Generating report at time: ', report_time)
	libacas.ReportAsJSON(sXu_idx, report_time, json_reports)
	clean_json = json_reports.value.decode("utf-8").replace(" ", "").replace("\n", "").replace('-nan(ind)', '"NaN"').replace('nan(ind)', '"NaN"').replace('-nan', '"NaN"').replace('nan', '"NaN"') + '\n'
	if verbosity:
		print("Report output:", clean_json[:40],'...') 
		with open('/home/fausto/catkin_ws/src/acasx/src/Software/Integration.Resources/Simple.sXu.Runner/logs/Encounter1Aircraft1TrmReport.json') as f:
			data = json.load(f)   

		count = 0
		for report in data['acasx_reports']:
			#vertical advisories
			vert1 = data['acasx_reports'][count]['acas_sxu_v2r0']['trm_report']['display_vert']['cc']
			vert2 = data['acasx_reports'][count]['acas_sxu_v2r0']['trm_report']['display_vert']['vc']
			vert3 = data['acasx_reports'][count]['acas_sxu_v2r0']['trm_report']['display_vert']['ua']
			vert4 = data['acasx_reports'][count]['acas_sxu_v2r0']['trm_report']['display_vert']['da']

			horiz = data['acasx_reports'][count]['acas_sxu_v2r0']['trm_report']['display_horiz']['cc']

			if vert1==4 and vert2==0 and vert3==1 and vert4==0:
				print("CLIMB")
				code = 0
				acas_pub.publish(code)


			elif vert1==4 and vert2==0 and vert3==2 and vert4==0:
				print("REDUCE DESCENT")
				code = 1
				acas_pub.publish(code)

			elif vert1==4 and vert2==0 and vert3==2 and vert4==2:
				print("LEVEL OFF")
				code = 2
				acas_pub.publish(code)


			elif vert1==4 and vert2==1 and vert3==1 and vert4==0:
				print("Altitude Crossing Climb")
				code = 3
				acas_pub.publish(code)


			elif vert1==4 and vert2==2 and vert3==1 and vert4==0:
				print("DESCEND TO CLIMB")
				code = 4
				acas_pub.publish(code)


			elif vert1==5 and vert2==0 and vert3==0 and vert4==1:
				print("DESCEND")
				code = 5
				acas_pub.publish(code)


			elif vert1==5 and vert2==0 and vert3==0 and vert4==2:
				print("REDUCE CLIMB")
				code = 6
				acas_pub.publish(code)


			elif vert1==5 and vert2==0 and vert3==2 and vert4==2:
				print("LEVEL OFF")
				code = 7
				acas_pub.publish(code)


			elif vert1==5 and vert2==1 and vert3==0 and vert4==1:
				print("ALTITUDE CROSSING DESCEND")
				code = 8
				acas_pub.publish(code)


			elif vert1==5 and vert2==2 and vert3==0 and vert4==1:
				print("CLIMB TO DESCEND")
				code = 9
				acas_pub.publish(code)


			elif vert1==6 and vert2==0 and vert3==0 and vert4==2:
				print("LIMIT CLIMB")
				code = 10
				acas_pub.publish(code)


			elif vert1==6 and vert2==0 and vert3==2 and vert4==0:
				print("LIMIT DESCENT")
				code = 11
				acas_pub.publish(code)


			elif vert1==6 and vert2==4 and vert3==2 and vert4==2:
				print("LEVEL OFF")
				code = 12
				acas_pub.publish(code)


			elif vert1==1 and vert2==0 and vert3==0 and vert4==0:
				print("CLEAR OF CONFLICT")
				code = 13
				acas_pub.publish(code)


			elif vert1==0 and vert2==0 and vert3==0 and vert4==0:
				print("NONE")
				code = 15
				acas_pub.publish(code)

			elif horiz==2:
				print("TURN RIGHT")
				code = 16
				acas_pub.publish(code)

			elif horiz==1:
				print("TURN LEFT")
				code = 17
				acas_pub.publish(code)

			count+=1


def getMessageTimeAndType(json_msg):
	messageType = None 

	#Collect message type by process of elimination (to avoid using data_type enumeration)
	for sub_msg in json_msg['acas_sxu_v2r0']:
		if sub_msg != 'data_type':
			messageType = sub_msg

	sub_msg = json_msg['acas_sxu_v2r0'][messageType]

	messageTime = json_msg['report_time']
	if 'toa' in sub_msg: #use toa is available, otherwise use report_time
		messageTime = sub_msg['toa']

	return messageTime, messageType

def sXuControlLoop(encounterMessages, file_path, start_time) : # The main update loop for ACAS
	global initialized, libacas, lastTime 
	filename = os.path.basename(file_path)
	encounter_name = filename.split('Encounter')[1].split('Aircraft')[0]
	aircraft_num = filename.split('Aircraft')[1].split('Input.json')[0]
	encounter_name_bytes = bytes(encounter_name, 'utf8')
	log_folder_bytes = bytes(log_folder, 'utf8')

	sXu_idx = 0 # this represents the first sXu instance slot, the only one maintained in the example
	if not initialized:
		if verbosity:
			print("Initializing sXu #" ,sXu_idx)
		libacas = InitializeEntrypoints()
		libacas.Initialize(sXu_idx, paramsfile_path, runtimefile_path)
		
		if verbosity:
			print("Init done ")
		initialized = True


	if verbosity:
		print("Resetting")
	libacas.Reset(sXu_idx)
	
	libacas.InitializeReporting(sXu_idx, encounter_name_bytes, int(aircraft_num), log_folder_bytes)
	report_time = start_time + 1
	
	if verbosity:
		print("Beginning the control loop")
	#Process all queued messages
	for json_msg in encounterMessages:  #Master loop, signifying processing of messages as the come in
		message_time, message_type = getMessageTimeAndType(json_msg)
		
		if simulate_delay:
			if lastTime == None or lastTime > message_time:
				lastTime = message_time
			dt = message_time - lastTime
			print(dt)
			time.sleep(dt)  #sleep to simulate a real-time progresion 
			lastTime = message_time
		current_time = message_time #signifies the passing of time to the moment you receive message

		#process any outstanding reports *before* processing the message
		while current_time >= report_time:
			ACASReport(sXu_idx, report_time, libacas)
			report_time = report_time + 1 #schedule 1 sec in future

		ProcessMessage(sXu_idx, json_msg, message_time, message_type, libacas)


def acasx():
	#pub = rospy.Publisher('chatter', String, queue_size=10)
	
	rospy.init_node('ACASsXU', anonymous=True)
	rate = rospy.Rate(100) 

	ownship_sub = rospy.Subscriber('/ownship/position', position, callback)
	ai_sub = rospy.Subscriber('/ai_aircraft/position', ai_aircraft, callback2)

	#bool_pub = rospy.Publisher('/acas/start', Bool, queue_size = 10)

	

	#rospy.spin()

	#encounter_folder = '../../test_files/TestSuiteV2R0/'
	encounterFile = '/home/fausto/catkin_ws/src/acasx/src/Software/test_files/TestSuiteV2R0/Encounter1/Encounter1Aircraft1Input.json'
	while not rospy.is_shutdown():

		#started_bool = 0
		#hello_str = "hello world %s" % rospy.get_time()
		#rospy.loginfo(hello_str)
		#pub.publish(hello_str)
		#rate.sleep()
		#for encounterFile in glob.iglob(encounter_folder + '**/*Input.json', recursive=True):
		print("Running encoutner:", encounterFile)
	
		with open(encounterFile,'r') as f:
			as_json = json.load(f)
			json_messages = as_json['acasx_reports']
			start_time = as_json['playback_header']['start_time']
			sXuControlLoop(json_messages, encounterFile, start_time)
			#started_bool = 1
			#bool_pub.publish(started_bool)
			#rospy.spin()
			rate.sleep()
		

if __name__ == '__main__':
	try:
		acasx()
	except rospy.ROSInterruptException:
		pass
