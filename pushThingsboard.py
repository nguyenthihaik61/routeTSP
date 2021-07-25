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
		sensor_data['PoF'] = pof
		sensor_data['CoF'] = risk
		sensor_data['inspection_plan'] = inspection_plan
		client.publish('v1/devices/me/telemetry',json.dumps(sensor_data))
		time.sleep(10)
	except KeyboardInterrupt:
		pass
	client.loop_stop()
	client.disconnect()
if __name__ == "__main__":
    # node 2
    pushThingsboard('GGBI5lF7USKIybPpoicE',"0.00031953","237920","29/12/2024")
    # node 3
    pushThingsboard('hr2beEaH0ziVOa1B1Q7P',"0.00036405","237920","05/12/2024")
    # node 4
    pushThingsboard('3yMaFLA8FHAElsZNUHcd',"0.00016412","237920","11/06/2016")
    # node 5
    pushThingsboard('rxCRysycsdZtX3qZp1bH',"0.000097","177673","22/09/2014")