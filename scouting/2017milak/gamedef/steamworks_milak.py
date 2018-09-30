# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:13:31 2018

@author: rober
"""

import games as gms

steamworks_cats = ['crossed_baseline',
                   'auton_lowgoal',
                   'auton_highgoal',
                   'auton_gears',
                   'auton_fouls',
                   'auton_techfouls',
                   'pickup_gears',
                   'pickup_fuel',
                   'teleop_lowgoal',
                   'teleop_highgoal',
                   'teleop_gears',
                   'teleop_fouls',
                   'teleop_techfouls',
                   'hanging',
                   'comments']

steamworks_weights = {'auton_lowgoal':1,
                       'auton_highgoal':3,
                       'auton_gears':30,
                       'crossed_baseline':5,
                       'pickup_gears':0,
                       'pickup_fuel':0,
                       'dropped_gears':0,
                       'teleop_lowgoal':0.3333,
                       'teleop_highgoal':1,
                       'teleop_gears':20,
                       'hanging':50}

STEAMWORKS = gms.Game(steamworks_cats, steamworks_cats[:-1], None, gms.steamworks_process_scouting, steamworks_weights)

def get_game():
    return STEAMWORKS