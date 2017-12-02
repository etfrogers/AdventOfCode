#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:36:23 2017

@author: user
"""

def captcha(digits):
    if isinstance(digits, str):
        digits = [int(c) for c in digits if c.isdigit()]
        # ignore non-digit characters
    print(digits)
    shifted = digits[1:]
    shifted.append(digits[0])
    print(shifted)
    matches = [t[0] for t in zip(digits, shifted) if t[0]==t[1]]
    return sum(matches)
    
def main():
    #read file
    with open('input.txt', 'r') as file:
        digits = file.read()
    out = captcha(digits)
    print(out)
    
if __name__ == '__main__':
    main()

    