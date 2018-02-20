# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:13:41 2018

@author: rober
"""

import pickle as pkl

import encode as ec
high = 99999999 #99,999,999

file = open('encoded.txt', 'rb')
code = pkl.load(file)
code = ec.h_decode(code, high=high)
exec(code)