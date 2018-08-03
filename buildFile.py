#!/usr/bin/python3

#edit these two arguments
delayedoff = 10
num_tests = 30
#below is constant arguments
#m = 5
#setup = 5
#endTime = 5000
#arrivalRate = 0.35
#serviceRate = 1
#mode = random
print(str(num_tests), file=open("num_tests.txt", "w"))
for count in range(num_tests):
	print("0.35", file=open("arrival_"+str(count+1)+".txt", "w"))
	print("1", file=open("service_"+str(count+1)+".txt", "w"))
	print("5\n5\n"+str(delayedoff)+"\n5000\n", file=open("para_"+str(count+1)+".txt", "w"))
	print("random", file=open("mode_"+str(count+1)+".txt", "w"))

#print("buildFile: delayedoff = "+str(delayedoff)+", numtests = "+str(num_tests))
