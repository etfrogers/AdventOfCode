#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:07:08 2017

@author: user
"""

import turtle
from enum import Enum
import numpy as np

class dirn(Enum):
    N = 0 
    E = 1 
    S = 2
    W = 3
    
    def vector(self):
        if   self.value == 0:
            v = [ 0, +1]
        elif self.value == 1:
            v = [+1,  0]
        elif self.value == 2:
            v = [ 0, -1]
        elif self.value == 3:
            v = [-1,  0]
        else:
            raise ValueError
        
        return np.array(v)
                
   
class turns(Enum):
    L = -1
    R = +1

   
strIn = 'L2, L5, L5, R5, L2, L4, R1, R1, L4, R2, R1, L1, L4, R1, L4, L4, R5, R3, R1, L1, R1, L5, L1, R5, L4, R2, L5, L3, L3, R3, L3, R4, R4, L2, L5, R1, R2, L2, L1, R3, R4, L193, R3, L5, R45, L1, R4, R79, L5, L5, R5, R1, L4, R3, R3, L4, R185, L5, L3, L1, R5, L2, R1, R3, R2, L3, L4, L2, R2, L3, L2, L2, L3, L5, R3, R4, L5, R1, R2, L2, R4, R3, L4, L3, L1, R3, R2, R1, R1, L3, R4, L5, R2, R1, R3, L3, L2, L2, R2, R1, R2, R3, L3, L3, R4, L4, R4, R4, R4, L3, L1, L2, R5, R2, R2, R2, L4, L3, L4, R4, L5, L4, R2, L4, L4, R4, R1, R5, L2, L4, L5, L3, L2, L4, L4, R3, L3, L4, R1, L2, R3, L2, R1, R2, R5, L4, L2, L1, L3, R2, R3, L2, L1, L5, L2, L1, R4'

#strIn = 'R5, L5, R5, R3'
#strIn = 'R8, R4, R4, R8'

listIn = strIn.split(',')

listIn = [entry.strip() for entry in listIn]
          
pos = np.array([0,0])
cDir = dirn.N

posL = [];          
for j, entry in enumerate(listIn):
    turn = turns[entry[0]]
    #assert(turn == 'L' or turn == 'R')
    dist = int(entry[1:])
    
    cDir = dirn((cDir.value + turn.value)%4)
    
    moves = []
    for i in range(1,dist+1):    
        moves.append(pos + i*cDir.vector())
    
    pos = pos + (dist * cDir.vector())
    
    
    print(str(j) + ': ' + turn.name + ':' + str(dist) + '   ' + cDir.name + ' - ' + str(pos.tolist()))

    
    found = False
    if len(posL)>1:
        #print(moves)
        for move in moves:
            #print(move)
            inHist = (move == posL[:-1]).all(1)
            if inHist.any():
                found = True
                break # for second part
        if found:
            foundInds = [i for i,b in enumerate(inHist) if b]
            endPos = posL[foundInds[0]]
            break
    posL+=(moves)
    
totalDist = sum(abs(endPos))
print('End pos: ' + str(endPos))
print('Distance from origin: ' + str(totalDist))