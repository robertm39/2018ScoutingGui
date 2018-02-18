# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:13:41 2018

@author: rober
"""

import encode as ec
#from code_getter import high
high=5
file = open('encoded.txt', 'r')
file = list(file)
file = ''.join(file)
code = ec.decode(file, high=high)
exec(code)