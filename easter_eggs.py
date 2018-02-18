# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:13:41 2018

@author: rober
"""

import tkinter as tk

def jr(get_weight, default_weights, numeric_cats):
    negative = False
    for cat in numeric_cats:
        if not 'foul' in cat:
            if get_weight(cat)*default_weights[cat] < 0: #If one is positive and the other is negative
               negative = True
    if negative:
        top = tk.Toplevel()
        top.title('Jerry Rig')
        top.geometry('250x30+400+400')
        label = tk.Label(top, text='Have a negative weight')
        label.pack(side=tk.TOP)
        
def clav(get_weight, default_weights, numeric_cats):
    positive = False
    for cat in numeric_cats:
        if 'foul' in cat:
            if get_weight(cat) > 0:
               positive = True
    if positive:
        top = tk.Toplevel()
        top.title('Chillin\' like a Villian')
        top.geometry('350x30+400+400')
        label = tk.Label(top, text='Have a positive weight for fouls')
        label.pack(side=tk.TOP)

def nmaw(get_weight, default_weights, numeric_cats):
    zero = True
    for cat in numeric_cats:
        if get_weight(cat) != 0:
              zero = False
    if zero:
        top = tk.Toplevel()
        top.title('Nothing Matters Anyway')
        top.geometry('350x30+400+400')
        label = tk.Label(top, text='Have zero for every weight')
        label.pack(side=tk.TOP)
    
weight_eggs = jr, clav, nmaw    
def do_weight_eggs(get_weight, default_weights, numeric_cats):
    for egg in weight_eggs:
        egg(get_weight, default_weights, numeric_cats)