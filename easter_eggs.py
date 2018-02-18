# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:13:41 2018

@author: rober
"""

import pickle as pkl

import encode as ec
#from code_getter import high
high=1100000

file = open('encoded.txt', 'rb')
code = pkl.load(file)
#file = list(file)
#file = ''.join(file)
code = ec.decode(code, high=high)
#print(code)
#print(type(code))
#print(len(code))
#print('print')
exec(code)