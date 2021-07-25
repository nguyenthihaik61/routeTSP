# Python3 program to implement traveling salesman
# problem using naive approach.
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
# caculate distance node to node
def distance(from_node , to_node):
	lon1=float(from_node[0])
	lat1=float(from_node[1])
	lon2=float(to_node[0])
	lat2=float(to_node[1])
	
	R=6378137                               # radius of Earth in meters
	phi_1=math.radians(lat1)
	phi_2=math.radians(lat2)
	delta_phi=math.radians(lat2-lat1)
	delta_lambda=math.radians(lon2-lon1)
	a=math.sin(delta_phi/2.0)**2+\
	math.cos(phi_1)*math.cos(phi_2)*\
	math.sin(delta_lambda/2.0)**2
	c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
	meters=R*c  
	return meters


def pushThingsboard(ACCESS_TOKEN,data_location):
	THINGSBOARD_HOST = 'demo.thingsboard.io'
	
	
	
	sensor_data = {}

	client = mqtt.Client()
	client.username_pw_set(ACCESS_TOKEN)
	
	client.connect(THINGSBOARD_HOST, 1883)
	
	client.loop_start()
	
	try:
		sensor_data['TSP'] = travellingSalesmanProblem(locationToGraph(data_location),0)
		client.publish('v1/devices/me/telemetry',json.dumps(sensor_data))
		time.sleep(10)
	except KeyboardInterrupt:
		pass
	client.loop_stop()
	client.disconnect()

# implementation of traveling Salesman Problem
def travellingSalesmanProblem(graph, s):

	# store all vertex apart from source vertex
	vertex = []
	V = len(graph)
	for i in range(V):
		if i != s:
			vertex.append(i)

	# store minimum weight Hamiltonian Cycle
	min_route=[]
	a=0
	min_path = maxsize
	print(min_path)
	next_permutation=permutations(vertex)
	temp=0
	for i in next_permutation:
		print(i)
		# store current Path weight(cost)
		current_pathweight = 0
		
		# compute current path weight
		k = s
		for j in i:
			current_pathweight += graph[k][j]
			k = j
		# 	if current_pathweight > min_path:
		# 		temp=1
		# 		break
		# if temp==1:
		# 	continue
		current_pathweight += graph[k][s]

		# update minimum
		if min_path > current_pathweight:
			min_path = current_pathweight
			
			min_route=i
		
		print(current_pathweight)
	min_route=(s,)+min_route+(s,)+('T',)
	# push Thingsboard
	print(min_route)
	return min_route


def locationToGraph(data_location):
	graph=[]
	for i in data_location:
		data_row=[]
		for j in data_location:
			if data_location.index(i) == data_location.index(j):
				data_row.append(0)
			else:
				data_row.append(distance(i,j))
		graph.append(data_row)
	return graph


def getDataThingsboard(accessToken):
	try:
		headers = {
			'Content-Type': 'application/json',
			'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsaW5oLm5uMjgwMzk5QGdtYWlsLmNvbSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiYmJhYTFlNTAtZDY1My0xMWViLTkzODEtYWIyYTFhOGRhYWYwIiwiZmlyc3ROYW1lIjoiTmd1eWVuIiwibGFzdE5hbWUiOiJOaGF0IExpbmgiLCJlbmFibGVkIjp0cnVlLCJwcml2YWN5UG9saWN5QWNjZXB0ZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiJiYTgyOGU0MC1kNjUzLTExZWItOTM4MS1hYjJhMWE4ZGFhZjAiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE2MjQ5NjI4MTEsImV4cCI6MTYyNjc2MjgxMX0.Af1hqije-Lbfanr0vSSbdWlcHq_BjTSQ-sA6KLb-0Y8g-0fyArBMKUeXxoGR3liL22me17DXE-1cxCupgRKy-Q',
		}
		response = requests.get(
			'http://demo.thingsboard.io/api/plugins/telemetry/DEVICE/' + accessToken + '/values/timeseries?keys=',
			headers=headers)
		return response.json()
	except Exception as e:
		print(e)
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)			


# Driver Code
if __name__ == "__main__":

	
	# truyen vao device id de goi getDataThingsboard
	accessToken="7a4d7320-e900-11eb-89a9-0d04d3fed54d"
	dataJson=getDataThingsboard(accessToken)
	# 
	data1node=(dataJson['Lat_UAV'][0]['value'],dataJson['Lon_UAV'][0]['value'])
	
	data_location=[]
	data_location.append(data1node)
	data_location.append((dataJson['Lat_sensor0'][0]['value'],dataJson['Lon_sensor0'][0]['value']))
	data_location.append((dataJson['Lat_sensor1'][0]['value'],dataJson['Lon_sensor1'][0]['value']))
	data_location.append((dataJson['Lat_sensor2'][0]['value'],dataJson['Lon_sensor2'][0]['value']))
	data_location.append((dataJson['Lat_sensor3'][0]['value'],dataJson['Lon_sensor3'][0]['value']))
	data_location.append((dataJson['Lat_sensor4'][0]['value'],dataJson['Lon_sensor4'][0]['value']))
	data_location.append((dataJson['Lat_sensor5'][0]['value'],dataJson['Lon_sensor5'][0]['value']))
	data_location.append((dataJson['Lat_sensor6'][0]['value'],dataJson['Lon_sensor6'][0]['value']))
	# data_location=[('21.006553', '105.842921'), ('21.0066095', '105.8431323'), ('21.0065419', '105.8432735'), ('21.0064809', '105.8431522'), ('21.0065144', '105.8429997')]
	# data_location=[('21.006553', '105.842921'), ('21.0066095', '105.8431323'), ('21.0065144', '105.8429997'), ('21.0065419', '105.8432735'), ('21.0064809', '105.8431522')]
	print(data_location)
	# print(type(float(data_location[0][0])))
	
	# truyen vao accestoken de goi pushThingsboard
	pushThingsboard('SsphMB7IqFfizf7IExbT',data_location)
	
	
 
	
	