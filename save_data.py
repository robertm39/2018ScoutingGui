# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 19:58:56 2018

@author: rober
"""

import os
import pickle as pkl

class SaveData(object):
    """Saves and loads attributes."""
    def __init__(self, name):
        directory = os.path.dirname(os.path.realpath(__file__)) + '\\save\\'
        self.path = directory + name + '.save'
        if not os.path.exists(self.path):
#            print('making folder')
            os.makedirs(directory)
#            print('opening file')
            file = open(self.path, 'w')
            file.close()
            self.save()
        self.load()
    
    def w(self, name, val):
        result = self.__setattr__(name, val)
        self.save()
        return result
        
    def r(self, name):
        self.load()
        return self.__getattribute__(name)
    
    def non_override_write(self, name, val):
        if not name in self.__dict__:
            self.__setattr__(name, val)
            
    def read_with_default(self, name, val, write=False):
        self.load()
        if not name in self.__dict__:
            if write:
                self.__setattr__(name, val)
            return val
        return self.__getattribute__(name)
    
    def save(self):
        #Bypass the __getattribute__ method loading
        pkl_out = open(self.path, 'wb+') #Write bytes
        pkl.dump(self, pkl_out)
        pkl_out.close()
        
    def load(self):
        #Bypass the __getattribute__ method loading
        path = self.path
        pkl_in  = open(path, 'rb')
        new_self = pkl.load(pkl_in)
        for name in vars(new_self):
#            print('loading', name)
            vars(self)[name] = vars(new_self)[name]