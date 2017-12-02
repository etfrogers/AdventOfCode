#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 12:06:48 2017

@author: user
"""
import numpy as np

def checksum(data):
    lineCheck = []
    for row in data:
        lineCheck.append(max(row)-min(row))
    return sum(lineCheck)

def main():
    data = np.loadtxt('input.txt')
    out = checksum(data)
    print(out)

if __name__ == '__main__':
    main()