#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:36:23 2017

@author: user
"""

def captcha(digits,step=1):
    
        
    if isinstance(digits, str):
        digits = [int(c) for c in digits if c.isdigit()]
        # ignore non-digit characters
    
    #must do after conversion as newline breaks the length
    if step is None:
        step = int(len(digits)/2)
        print(step)
    
    shifted = digits[step:]
    shifted.extend(digits[0:step])
    print(digits)
    print(shifted)
    matches = [t[0] for t in zip(digits, shifted) if t[0]==t[1]]
    return sum(matches)
    
def main():
    #read file
    with open('input.txt', 'r') as file:
        digits = file.read()
    #digits = '1111'
    out = captcha(digits,None)
    print(out)
    
if __name__ == '__main__':
    main()

    