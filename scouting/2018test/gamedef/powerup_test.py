# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:03:30 2018

@author: rober
"""

import games as gms

def powerup_process_match(match):
    match = match.copy()
    endgame_action = match.pop('endgame_action')
    match['climbing'] = int(endgame_action == 0) #climbing is action 0
    match['parking'] =int(endgame_action == 1) #parking is action 1
    return match

def powerup_process_scouting(scouting):
    return gms.process_scouting_by_match(scouting, powerup_process_match)

powerup_cats = ['auton_ci_switch',
                'auton_ci_scale',
                'auton_cube_count',
                'cube_count',
                'cube_switch',
                'cube_scale',
                'cube_vault',
                'fouls',
                'tech_fouls',
                'climbing',
                'hanging',
                'helping_robot',
                'comments']
powerup_rankings = {'tech_fouls':0}
POWER_UP = gms.Game(powerup_cats, powerup_cats[:-1], None, powerup_process_scouting, powerup_rankings)

def get_game():
    return POWER_UP
