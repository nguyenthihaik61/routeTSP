import math
from sys import maxsize
from itertools import permutations
from datetime import datetime
import time
import json
import math
import paho.mqtt.client as mqtt
import os,sys
import requests
import random
def pushThingsboard(ACCESS_TOKEN,pof,risk,inspection_plan):
	THINGSBOARD_HOST = 'demo.thingsboard.io'
	
	
	
	sensor_data = {}

	client = mqtt.Client()
	client.username_pw_set(ACCESS_TOKEN)
	
	client.connect(THINGSBOARD_HOST, 1883)
	
	client.loop_start()
	
	try:
		sensor_data['pof'] = pof
		sensor_data['risk'] = risk
		sensor_data['inspection_plan'] = inspection_plan
		client.publish('v1/devices/me/telemetry',json.dumps(sensor_data))
		time.sleep(10)
	except KeyboardInterrupt:
		pass
	client.loop_stop()
	client.disconnect()
if __name__ == "__main__":
    # node 2
    pushThingsboard('GGBI5lF7USKIybPpoicE',"","","")
    # node 3
    pushThingsboard('hr2beEaH0ziVOa1B1Q7P',"","","")
    # node 4
    pushThingsboard('3yMaFLA8FHAElsZNUHcd',"","","")
    # node 5
    pushThingsboard('rxCRysycsdZtX3qZp1bH',"","","")