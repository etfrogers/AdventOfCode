from nose.tools import *
import day2
import numpy as np

def test1():
    data = [[5, 1, 9, 5],
            [7, 5, 3],
            [2, 4, 6, 8]]
    
    assert day2.checksum(data) == 18

def testPart1():
    data = np.loadtxt('input.txt')
    assert day2.checksum(data) == 43074

def test2():
    data = [[5, 9, 2, 8],
            [9, 4, 7, 3],
            [3, 8, 6, 5]]
    assert day2.checksum(data, True) == 9



