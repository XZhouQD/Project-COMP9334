#!/usr/bin/python3

from math import *

mrtList = []

with open("num_tests.txt", "r") as f:
	num_test = int(f.readline().rstrip())

for test in range(num_test):
	with open("mrt_"+str(test+1)+".txt", "r") as f:
		mrtList.append(float(f.readline().rstrip()))

avgMrt = fsum(mrtList) / float(num_test)
sum1 = 0
for item in mrtList:
	sum1 = sum1+pow(avgMrt-item, 2)
std = sqrt(sum1/(num_test-1))
#95% CI, t = 2.045
low = avgMrt - 2.045*std
high = avgMrt + 2.045*std
print("average MRT = %.3f, std = %.3f" % (avgMrt, std))
print(".95 CI (%.3f, %.3f)" % (low, high))
