#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:16:10 2017

@author: user
"""

import numpy as np


def is_triangle(line):
    assert(len(line) == 3)
    # print(line)
    max_ind = np.argmax(line)
    hyp = line[max_ind]
    side_inds = np.array([i for i in range(3) if not i == max_ind])
    sides = line[side_inds]
    # print(hyp)
    # print(sides)
    is_valid = (hyp < sum(sides))
    # print(is_valid)
    return is_valid


def main():
    data = np.loadtxt('day3input.txt')
    print(data)
    data = np.reshape(data.T, [-1, 3])
    # print(data)
    # data = np.reshape(data, [3,-1])
    print(data)
    count = 0
    for line in data:
        if is_triangle(line):
            count += 1

    print(count)


if __name__ == '__main__':
    main()
