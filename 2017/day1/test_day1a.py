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
