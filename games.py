# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:38:09 2018

@author: rober
"""

class Game:
    def __init__(self, categories, numeric_categories, get_scouting_from_match):
        self.categories = categories
        self.numeric_categories = numeric_categories
        self.get_scouting_from_match = get_scouting_from_match

def put_in_histogram(contrs, upper_limit = False, verbose=False):
    result = {}
    tot = 0
    for contr in contrs:
        result[contr] = result.get(contr, 0) + 1
        tot += 1
        
    for contr in result:
        result[contr] = result[contr] / tot
    
    return result

def averages_from_contrs(contrs):
    result = {}
    for team in contrs.keys():
        result[team] = averages_from_contrs_for_team(contrs[team])
    return result

def averages_from_contrs_for_team(contrs):
    result = {}
    for cat in contrs.keys():
        tot = 0
        cc = contrs[cat]
        for num in cc.keys():
            tot += num * cc[num]
        result[cat] = int(tot*100)/100 #Two decimal places
    return result

def contrs(raw_scouting, game):
    contrs = {}
    for team in raw_scouting.keys():
        contrs[team] = team_contrs(raw_scouting[team], game)
        
    return contrs

def team_contrs(team_scouting, game, pr=False):
    """Return the contrs. Contrs is cat -> distr (num -> amount)"""
    cats = game.numeric_categories
    
    contrs = {}
    for num, results in team_scouting:
        if pr:
            print('num, results:', num, results)
            print('')
        for cat in cats:
            if cat in results:
                if not cat in contrs:
                    contrs[cat] = []
                contrs[cat].append(results[cat])
                
    for cat in contrs:
        contrs[cat] = put_in_histogram(contrs[cat])
        
    return contrs

STEAMWORKS = Game(['auton_lowgoal',
                   'auton_highgoal',
                   'try_lft_auton_gears',
                   'try_cen_auton_gears',
                   'try_rgt_auton_gears',
                   'lft_auton_gears',
                   'cen_auton_gears',
                   'rgt_auton_gears',
                   'crossed_baseline',
                   'pickup_gears',
                   'teleop_lowgoal',
                   'teleop_highgoal',
                   'teleop_gears',
                   'hanging',
                   'caught_rope',
                   'comments'], 
                    ['auton_lowgoal',
                   'auton_highgoal',
                   'try_lft_auton_gears',
                   'try_cen_auton_gears',
                   'try_rgt_auton_gears',
                   'lft_auton_gears',
                   'cen_auton_gears',
                   'rgt_auton_gears',
                   'crossed_baseline',
                   'pickup_gears',
                   'teleop_lowgoal',
                   'teleop_highgoal',
                   'teleop_gears',
                   'hanging',
                   'caught_rope'], None)
POWER_UP = Game([], [], None)

GAMES_FROM_YEARS = {'2017':STEAMWORKS, '2018': POWER_UP}
