#!/usr/bin/python3

#COMP9334 18s1 Project
#Xiaowei Zhou
#z5108173
#UNSW Sydney

from math import *
from random import *
from sys import maxsize
from collections import deque

def traceSimulation (m,setup,delayedoff,arrivalList,serviceList,endTime):
	responseTime = 0
	arrivalCount = 0
	departureCount = 0
	trueCount = 0
	arrival = []
	service = []
# Read in arrival and service times
	for event in arrivalList:
		arrival.append(float(str(event).rstrip()))
	for event in serviceList:
		service.append(float(str(event).rstrip()))
# Use deque for function popleft
	Queue = deque([])
	transient = len(arrivalList)/5
	statusList = [0] * m #status of servers, 0 OFF 1 SETUP 2 DELAYEDOFF 3 BUSY
	departureList = [maxsize] * m #next departure time of servers, default maxsize
	setupTimeList = [maxsize] * m #finish setup time of servers, default maxsize
	delayedoffTimeList = [maxsize] * m #delayoff time of servers, default maxsize
	arrivalTimeNextDeparture = [0]*m #arrival time of event for servers, used for construct departure list

# nextEvent:arrival or departure or finish setup or turn server off
	nextEventTime = min([arrival[arrivalCount],min(departureList),min(setupTimeList),min(delayedoffTimeList)])
# empty departure list
	eventList = []
	if endTime == 'trace':
		endTime = maxsize
#loop, finsih all jobs or reach endTime (for clear trace simulation, endTime is infinity
	while (len(eventList) < len(arrival) and nextEventTime <= endTime ) :
		if arrivalCount < len(arrival) and nextEventTime == arrival[arrivalCount] : #an arrival
			if statusList.count(0) + statusList.count(2) == 0 :
#				No Server available
				Queue.append([nextEventTime,service[arrivalCount],"unmark"])
			elif statusList.count(2) > 0:
#				Use a delayedoff server
				idleServerValue = 0
				for value in delayedoffTimeList:
					if value > idleServerValue and value < maxsize :
						idleServerValue = value
				idleServer = delayedoffTimeList.index(idleServerValue)
#				found a delayedoff server with maximum delayedoff time but not maxsize
				if len(Queue) > 0 :
					nextJob = Queue.popleft()
					Queue.append([nextEventTime,service[arrivalCount],"unmark"])
				else :
					nextJob = [nextEventTime,service[arrivalCount],"unmark"]
#				nextJob can be either from queue or this job passed in
				departureList[idleServer] = nextEventTime+nextJob[1]
				arrivalTimeNextDeparture[idleServer] = nextJob[0]
				statusList[idleServer] = 3
#				finsih sending job in server, server busy now
				delayedoffTimeList[idleServer] = maxsize
#				reset delayedoff time to maxsize
			elif statusList.count(0) > 0:
#				start an off server
				offServer = statusList.index(0)
				statusList[offServer] = 1
				setupTimeList[offServer] = nextEventTime + setup
#				set server to setup stage
				Queue.append([nextEventTime,service[arrivalCount],"mark"])
#				send job into queue with MARKED
			arrivalCount = arrivalCount+1
		elif nextEventTime == min(departureList) :
#			A Departure
			departureServer = departureList.index(nextEventTime)
			departureCount = departureCount + 1
			if departureCount > transient:
				responseTime = responseTime + nextEventTime - arrivalTimeNextDeparture[departureServer]
				trueCount = trueCount + 1
			eventList.append([arrivalTimeNextDeparture[departureServer],nextEventTime])
#			update total response time and departure list
			if len(Queue)>0 :
				nextJob = Queue.popleft()
				departureList[departureServer] = nextEventTime + nextJob[1]
				arrivalTimeNextDeparture[departureServer] = nextJob[0]
#				if a job in queue, send it into departure server
			else :
				departureList[departureServer] = maxsize
				statusList[departureServer] = 2
				delayedoffTimeList[departureServer] = nextEventTime + delayedoff
#				no job in queue, go delayedoff
		elif nextEventTime == min(setupTimeList):
#			Setup Finish
			setupServer = setupTimeList.index(nextEventTime)
			setupTimeList[setupServer] = maxsize
			if len(Queue) > 0 :
				nextJob = Queue.popleft()
				departureList[setupServer] = nextEventTime + nextJob[1]
				arrivalTimeNextDeparture[setupServer] = nextJob[0]
				statusList[setupServer] = 3
#				if a job in queue, send it to new setuped server
			else :
				statusList[setupServer] = 2
				delayedoffTimeList[setupServer] = nextEventTime + delayedoff
#				no job in queue, go delayedoff
		elif nextEventTime == min(delayedoffTimeList) :
#			Server shut down
			delayedoffServer = delayedoffTimeList.index(nextEventTime)
			statusList[delayedoffServer] = 0
			delayedoffTimeList[delayedoffServer] = maxsize
#			set status to OFF, reset delayedoff time to maxsize
		settingUpServers = statusList.count(1)
#		check the number of servers in setup stage
		for job in Queue:
			if job[2] == "mark" :
				settingUpServers = settingUpServers - 1
			elif settingUpServers > 0 :				
				job[2] = "mark"
				settingUpServers = settingUpServers - 1
#		check if it fit with jobs in queue with MARKED, if not, mark some jobs
		while settingUpServers > 0:
			settingUpLatest = 0
			for value in setupTimeList:
				if value > settingUpLatest and value < maxsize :
					settingUpLatest = value
			statusList[setupTimeList.index(settingUpLatest)] = 0
			setupTimeList[setupTimeList.index(settingUpLatest)] = maxsize
			settingUpServers = settingUpServers - 1
#			if number still not match, shut down some setting up servers
		if arrivalCount >= len(arrival):
			nextEventTime = min([min(departureList),min(setupTimeList),min(delayedoffTimeList)])
#			if all arrivals processed, arrival time does not count as next event
		else : 
			nextEventTime = min([arrival[arrivalCount],min(departureList),min(setupTimeList),min(delayedoffTimeList)])
#			else come up next event time
	avgResponse = 0
	if trueCount > 0 :
		avgResponse = responseTime/trueCount
	return avgResponse, eventList
#	return average response time calculated and eventList
#This random simulation function is complete but not used as 
#random simulation is routed to construct a trace and use trace simulation
#it also returns arrival list and service list for trace simulation check
#but buildTrace function can do that
def randomSimulation (m,setup,delayedoff,endTime,arrivalRate,serviceRate,seedAddon):
	seed(5108173+seedAddon)
	responseTime = 0
	eventCount = 0
	arrivalList = []
	serviceList = []
	nextArrival = -log(1-random())/arrivalRate
	serviceTime = -log(1-random())/serviceRate-log(1-random())/serviceRate-log(1-random())/serviceRate
	arrivalList.append(nextArrival)
	serviceList.append(serviceTime)
	departureList = [maxsize] * m
	masterClock = 0
	statusList = [0] * m # 0 for off, 1 for setup, 2 for delayed off, 3 for busy
	delayedoffTimeList = [0] * m
	setupTimeList = [0] * m
	arrivalTimeNextDeparture = [0] * m
	Queue = deque([])
	eventList = []
	prevMasterClock = 0
	while masterClock < endTime:
		nextDepartureTime = min(departureList)
		nextDepartureServer = departureList.index(nextDepartureTime)
		if nextArrival < nextDepartureTime :
			nextEventTime = nextArrival
			nextEvent = "arrival"
		else :
			nextEventTime = nextDepartureTime
			nextEvent = "departure"
		masterClock = nextEventTime
		for server in range(m):
			if delayedoffTimeList[server] > 0:
				delayedoffTimeList[server] = delayedoffTimeList[server] - (masterClock - prevMasterClock)
				if delayedoffTimeList[server] <= 0:
					delayedoffTimeList[server] = 0
					statusList[server] = 0
		for server in range(m):
			if setupTimeList[server] > 0:
				setupTimeList[server] = setupTimeList[server] - (masterClock - prevMasterClock)
				if setupTimeList[server] <= 0:
					setupTimeList[server] = 0
					statusList[server] = 2
					delayedoffTimeList[server] = delayedoff
		prevMasterClock = masterClock
		if nextEvent == "arrival" :
			if statusList.count(0)+statusList.count(2) == 0 :
				Queue.append([nextArrival,serviceTime,"unmark"])
			elif statusList.count(2) > 0 :
				idleServer = delayedoffTimeList.index(max(delayedoffTimeList))
				if len(Queue) > 0 :
					nextJob = Queue.popleft()
					Queue.append([nextArrival,serviceTime,"unmark"])
				else :
					nextJob = [nextArrival,serviceTime,"unmark"]
				departureList[idleServer] = masterClock + nextJob[1]
				arrivalTimeNextDeparture[idleServer] = nextJob[0]
				statusList[idleServer] = 3
				delayedoffTimeList[idleServer] = 0
			elif statusList.count(0) > 0 :
				offServer = statusList.index(0)
				statusList[offServer] = 1
				setupTimeList[offServer] = setup
				Queue.append([nextArrival,serviceTime,"mark"])
			nextArrival = masterClock - log(1-random())/arrivalRate
			serviceTime = -log(1-random())/serviceRate-log(1-random())/serviceRate-log(1-random())/serviceRate
			arrivalList.append(nextArrival)
			serviceList.append(serviceTime)

		else:
			responseTime = responseTime + masterClock - arrivalTimeNextDeparture[nextDepartureServer]
			eventList.append([arrivalTimeNextDeparture[nextDepartureServer], masterClock])
			if len(Queue)>0 :
				nextJob = Queue.popleft()
				departureList[nextDepartureServer] = masterClock+nextJob[1]
				arrivalTimeNextDeparture[nextDepartureServer] = nextJob[0]
			else :
				departureList[nextDepartureServer] = maxsize
				statusList[nextDepartureServer] = 2
				delayedoffTimeList[nextDepartureServer] = delayedoff
		
		settingUpServers = statusList.count(1)
		for job in Queue:
			if job[2] == 'mark' :
				settingUpServers = settingUpServers-1
			elif settingUpServers > 0:
				job[2] == 'mark'
				settingUpServers = settingUpServers-1
		while settingUpServers > 0:
			statusList[setupTimeList.index(max(setupTimeList))] = 0
			setupTimeList[setupTimeList.index(max(setupTimeList))] = 0
			settingUpServers = settingUpServers - 1
	avgResponse = 0
	if len(eventList) > 0:
		avgResponse = responseTime/len(eventList)
	return avgResponse, eventList, arrivalList, serviceList

#This function build a Trace from random simulation arguments
def buildTrace(arrivalRate, serviceRate, endTime, seedAddon):
	seed(5108173+seedAddon)
	arrivalList = []
	serviceList = []
	nextArrival = 0
	while nextArrival < endTime:
		nextArrival = nextArrival - log(1-random())/arrivalRate
		serviceTime = -log(1-random())/serviceRate-log(1-random())/serviceRate-log(1-random())/serviceRate
		arrivalList.append(nextArrival)
		serviceList.append(serviceTime)
#		construct arrivals and service time by poision
	arrivalList.pop()
	serviceList.pop()
	return arrivalList, serviceList
