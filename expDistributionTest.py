#!/usr/bin/python3
from random import *
from math import *

rate = 6
yList = []
count = 0
print("generated numbers", file=open("expDis.csv", "w"))

while count < 20000 :
	rand = random()
	y = -log(1-rand)/rate
	yList.append(y)	
	count = count + 1

for value in yList:
	print(value, file=open("expDis.csv", "a"))
