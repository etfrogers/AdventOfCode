from AOC2017.day1.day1 import captcha


def test1():
	assert captcha('1122') == 3


def test2():
	assert captcha('1111') == 4


def test3():
	assert captcha('1234') == 0


def test4():
	assert captcha('91212129') == 9

# PART 2


def test5():
	assert captcha('1212', None) == 6


def test6():
	assert captcha('1221', None) == 0


def test7():
	assert captcha('123425', None) == 4


def test8():
	assert captcha('123123', None) == 12


def test9():
	assert captcha('12131415', None) == 4
    
