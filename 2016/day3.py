#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:16:10 2017

@author: user
"""

import numpy as np

def istriangle(line):
    assert(len(line) == 3)
    #print(line)
    maxind = np.argmax(line)
    hyp = line[maxind]
    sideinds =np.array([i for i in range(3) if not i == maxind])
    sides = line[sideinds]
    #print(hyp)
    #print(sides)
    isValid = (hyp < sum(sides))
    #print(isValid)
    return isValid

data = np.loadtxt('day3input.txt')
print(data)
data = np.reshape(data.T, [-1, 3])
#print(data)
#data = np.reshape(data, [3,-1])
print(data)
count = 0;
for line in data:
    if istriangle(line):
        count+=1
    
print(count)

