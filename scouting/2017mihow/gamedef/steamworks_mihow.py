# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:21:00 2018

@author: rober
"""

import games as gms

steamworks_cats = ['auton_lowgoal',
                   'auton_highgoal',
                   'try_lft_auton_gears',
                   'try_cen_auton_gears',
                   'try_rgt_auton_gears',
                   'lft_auton_gears',
                   'cen_auton_gears',
                   'rgt_auton_gears',
                   'crossed_baseline',
                   'pickup_gears',
                   'dropped_gears',
                   'teleop_lowgoal',
                   'teleop_highgoal',
                   'teleop_gears',
                   'hanging',
                   'caught_rope',
                   'comments']

steamworks_rankings = {'auton_lowgoal':1,
                       'auton_highgoal':3,
                       'try_lft_auton_gears':0,
                       'try_cen_auton_gears':0,
                       'try_rgt_auton_gears':0,
                       'lft_auton_gears':30,
                       'cen_auton_gears':30,
                       'rgt_auton_gears':30,
                       'crossed_baseline':5,
                       'pickup_gears':0,
                       'dropped_gears':0,
                       'teleop_lowgoal':0.3333,
                       'teleop_highgoal':1,
                       'teleop_gears':20,
                       'hanging':50,
                       'caught_rope':0}
STEAMWORKS = gms.Game(steamworks_cats, steamworks_cats[:-1], None, gms.steamworks_process_scouting, steamworks_rankings)

def get_game():
    return STEAMWORKS