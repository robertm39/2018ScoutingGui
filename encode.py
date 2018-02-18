# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:57:53 2018

@author: rober
"""

import random

def encode(message, seed=0, low=0, high=100, decode=False):
    random.seed(seed)
    encoded = []
    for char in message:
        if not char == '\n':
            change = -1 if decode else 1
            encoded.append(chr(ord(char) + change * random.randint(low, high)))
        else:
            encoded.append('\n')
    return ''.join(encoded)

def decode(message, seed=0, low=0, high=100):
    return encode(message, seed=seed, low=low, high=high, decode=True)

def h_encode(message, seed=0, low=0, high=100):#, decode=False):
    random.seed(seed)
    encoded = []
    for char in message:
        encoded.append(ord(char) + random.randint(low, high))
    return (encoded)

def h_decode(encoded, seed=0, low=0, high=100):
    random.seed(seed)
    decoded = []
    for num in encoded:
        decoded.append(chr(num - random.randint(low, high)))
    return ''.join(decoded)