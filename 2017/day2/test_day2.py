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

#def test2():
#	assert day1.captcha('1111') == 4
#
#def test3():
#	assert day1.captcha('1234') == 0
#
#def test4():
#	assert day1.captcha('91212129') == 9
#    
#
## PART 2
#def test5():
#	assert day1.captcha('1212',None) == 6
#
#def test6():
#	assert day1.captcha('1221',None) == 0
#
#def test7():
#	assert day1.captcha('123425',None) == 4
#
#def test8():
#	assert day1.captcha('123123',None) == 12
#
#def test9():
#	assert day1.captcha('12131415',None) == 4
    
    
