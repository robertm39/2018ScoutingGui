# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 20:11:42 2018

@author: rober
"""

import save_data as sd

save = sd.SaveData('test_save')

def write(): 
    save.one=1
    save.two=2
    
def read():
    print(save.one)
    print(save.two)
    
#write()
read()