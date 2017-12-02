from nose.tools import *
import day1

def test1():
	assert day1.captcha('1122') == 3

def test2():
	assert day1.captcha('1111') == 4

def test3():
	assert day1.captcha('1234') == 0

def test4():
	assert day1.captcha('91212129') == 9
    

# PART 2
def test5():
	assert day1.captcha('1212',None) == 6

def test6():
	assert day1.captcha('1221',None) == 0

def test7():
	assert day1.captcha('123425',None) == 4

def test8():
	assert day1.captcha('123123',None) == 12

def test9():
	assert day1.captcha('12131415',None) == 4
    
    
