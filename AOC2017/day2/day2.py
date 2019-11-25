#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 12:06:48 2017

@author: user
"""
import numpy as np


def checksum(data, divisors=False):
    line_check = []
    for row in data:
        print(row)
        if divisors:
            found = False
            res = 0
            for a in row:
                found = False
                matches = [b for b in row if (max(a, b) % min(a, b) == 0) and a != b]
                print(matches)
                assert len(matches) <= 1
                if len(matches) > 0:
                    res = max(a, matches[0]) / min(a, matches[0])
                    found = True
                    break
            assert found
            line_check.append(res)
        else:
            line_check.append(max(row)-min(row))
            
    return sum(line_check)


def main():
    data = np.loadtxt('input.txt')
#    data = [[5, 9, 2, 8],
#            [9, 4, 7, 3],
#            [3, 8, 6, 5]]
    out = checksum(data, True)
    print(out)


if __name__ == '__main__':
    main()