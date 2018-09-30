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
        """
        Make a SaveData.
        
        Parameters:
            name: The file name for the save data.
        """
        
        directory = os.path.dirname(os.path.realpath(__file__)) + '\\save\\'
        self.path = directory + name + '.save'
        if not os.path.exists(self.path):
            os.makedirs(directory)
            file = open(self.path, 'w')
            file.close()
            self.save()
        self.load()
    
    def w(self, name, val):
        """
        Write the given val to the given name.
        
        Parameters:
            name: The name of the variable to write
            val: The value to write to the variable
        """
        
        result = self.__setattr__(name, val) #Write the value to the variable
        self.save()
        return result
        
    def r(self, name):
        """
        Return the value of the named variable.
        
        Parameters:
            name: The name of the variable to return the value for.
        """
        
        self.load()
        return self.__getattribute__(name)
    
    def non_override_write(self, name, val):
        """
        Write the value into the name if there is not already a value.
        
        Parameters:
            name: The name of the variable to write to.
            val: The value to write to the variable.
        """
        
        if not name in self.__dict__: #Only write if there is no value for this name
            self.__setattr__(name, val) #Write the value to the variable
            
    def read_with_default(self, name, val, write=False):
        """
        Return the value for the variable or the given default if there is none. Conditionally write the default.
        
        Parameters:
            name: The name of the variable read.
            val: The default value to return if there is no value.
            write: Whether to write the default value if there is no value.
        """
        
        self.load()
        if not name in self.__dict__: #If there is no value
            if write:
                self.__setattr__(name, val) #Write the default
            return val #Return the default
        return self.__getattribute__(name) #Return the current value
    
    def save(self):
        """Save all data to the save file."""
        
        pkl_out = open(self.path, 'wb+') #Open a file to write bytes to
        pkl.dump(self, pkl_out) #Write the bytes
        pkl_out.close() #Close (this is important)
        
    def load(self):
        """Load all data from the save file."""
        
        path = self.path
        pkl_in  = open(path, 'rb') #Open a file to read bytes from
        new_self = pkl.load(pkl_in) #Read bytes
        for name in vars(new_self): #Update all the vars
            vars(self)[name] = vars(new_self)[name] #Manually set the vars