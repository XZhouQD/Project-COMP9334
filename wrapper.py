#!/usr/bin/python3

#IMPORTANT: Please read readme.txt and use run.sh for great amount of tests
#or directly use wrapper.py for small amount of tests
#to directly use wrapper.py, simply get ready all configuration files
#and run ./wrapperpy
#The simulation process has no on screen output, all output is printed to files

import sim
import math

def simulation(modeF,paraF,arrivalF,serviceF,seedAddon):
	with open (modeF) as f:
		mode = f.read().rstrip()
#	print(mode)
	with open (paraF) as f:
		m = int(f.readline().rstrip())
		setup = float(f.readline().rstrip())
		delayedoff = float(f.readline().rstrip())
		if mode == "random" :
			endTime = float(f.readline().rstrip())
	with open (arrivalF) as f:
		if mode == "random":
			arrivalRate = float(f.read().rstrip())
		if mode == "trace":
			arrivalList = f.readlines()
	with open (serviceF) as f:
		if mode == "random":
			serviceRate = float(f.read().rstrip())
		if mode == "trace":
			serviceList = f.readlines()
	if mode == "random":
		arrivalList, serviceList = sim.buildTrace(arrivalRate, serviceRate, endTime, seedAddon)
		avgRes,eventList = sim.traceSimulation(m,setup,delayedoff,arrivalList,serviceList,endTime)
	if mode == "trace":
		avgRes,eventList = sim.traceSimulation(m,setup,delayedoff,arrivalList,serviceList,'trace')

	#print(mode, m, setup, delayedoff, endTime, arrivalRate, serviceRate)
	#print(mode, m, setup, delayedoff, arrivalList, serviceList)
	return avgRes, eventList

with open ('num_tests.txt') as f:
	num_test = f.read()

for test in range(int(num_test)):
	avgRes, eventList = simulation("mode_"+str(test+1)+".txt", "para_"+str(test+1)+".txt", "arrival_"+str(test+1)+".txt", "service_"+str(test+1)+".txt", test)
	print('%.3f' % avgRes, end='', file=open("mrt_"+str(test+1)+".txt", "w"))
	open("departure_"+str(test+1)+".txt", "w")
	for event in eventList:
		print('%.3f\t%.3f' % (event[0],event[1]), file=open("departure_"+str(test+1)+".txt", "a"))
#	print("Simulation "+ str(test+1)+" Complete, Mean Response Time = "+ str(avgRes))
#print("Simulation Program Complete")
