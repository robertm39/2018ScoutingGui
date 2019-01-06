# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:38:09 2018

@author: rober
"""

class Game:
    """The game for a year."""
    
    def __init__(self,
                 categories,
                 numeric_categories,
                 get_scouting_from_match,
                 process_scouting=lambda s:s,
                 default_weights={}):
        self.categories = categories
        self.numeric_categories = numeric_categories
        self.get_scouting_from_match = get_scouting_from_match
        self.process_scouting = process_scouting
        
        self.default_weights = default_weights.copy()
        for category in self.numeric_categories:
            if not category in self.default_weights:
                self.default_weights[category] = 0

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
                result = results[cat]
                if type(result) in [int, float]: #Ignore 'NA'
                    contrs[cat].append(results[cat])
                
    for cat in contrs:
        contrs[cat] = put_in_histogram(contrs[cat])
        
    return contrs

def get_cats(scouting_cats, game_cats, numeric=False):
    if len(game_cats) == 0:
        result = scouting_cats[:]
        if numeric and 'comments' in result:
            result.remove('comments')
        return result
    return [cat for cat in game_cats if cat in scouting_cats] #intersection

def change_names(name_dict, match_dict):
    result = {}
    for cat in match_dict:
        if cat in name_dict:
            result[name_dict[cat]] = match_dict[cat]
#        else:
#            result[cat] = match_dict[cat]
#            print('Couldn\'t convert:', cat)
    return result

def process_scouting_by_match(scouting, process_match):
    result = {}
    for team in scouting:
        matches = []
        for match in scouting[team]:
            matches.append((match[0], process_match(match[1])))
        result[team] = matches
    return result

def combine_matches_from_sources(matches, source_order):
    matches_from_source = {}
    for match_id, match in matches:
        matches_from_source[match['source']] = match_id, match
        
    for source in source_order:
        if source in matches_from_source:
            return matches_from_source[source]
    return None

def combine_scouting_from_sources(scouting, source_order):
    result = {}
    for team in scouting:
        t_scouting = scouting[team]
        ts_from_match_id = {}
        for match_id, match in t_scouting:
            l = ts_from_match_id.get(match_id, [])
            l.append((match_id, match))
            if not match_id in ts_from_match_id:
                ts_from_match_id[match_id] = l
        
        n_ts = []
        match_ids = list(ts_from_match_id)
        match_ids.sort()
        for match_id in match_ids:
            matches = ts_from_match_id[match_id]
            match = combine_matches_from_sources(matches, source_order)
#            print(match)
            if match:
                n_ts.append(match)
                
        result[team] = n_ts
    return result

###STEAMWORKS
def steamworks_process_match(match):
    if 'caught_rope' in match:
        match = match.copy()
        match['caught_rope'] |= match['hanging']
    return match

def steamworks_process_scouting(scouting):
    return process_scouting_by_match(scouting, steamworks_process_match)

steamworks_cats = ['auton_lowgoal',
                   'auton_highgoal',
                   'auton_gears',
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
                       'auton_gears':30,
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
STEAMWORKS = Game(steamworks_cats, steamworks_cats[:-1], None, steamworks_process_scouting, steamworks_rankings)

###Code for using scouting data from 3322.
EAGLE_NAME_DICT = {'Crosses the auto line (auto-run)':'cross_line',
                   'Number of Cubes in Exchange':'cube_vault',
                   'Number of cubes in auton':'auton_cube_count',
                   'Number of Cubes on Scale':'cube_scale',
                   'Extra Notes':'comments',
                   'source':'source'}

def zealous_convert(token):
    if type(token) is int:
        return token
    if token.lower() in ['yes', 'same side', 'from center', 'in position', 'in the middle']:
        return 1
    return 0

def eagle_climb_convert_parked(token):
    if type(token) is int:
        return 0
    if 'parked' in token.lower():
        return 1
    return 0

def eagle_climb_convert_climb(token):
    if type(token) is int:
        return token
    if token.lower() == 'yes':
        return 1
    return 0

#POWERUP
def powerup_process_match(match):
    match = match.copy()
    
    if match['source'] == 'RAT':
        endgame_action = match.pop('endgame_action')
        match['climbing'] = int(endgame_action == 0) #climbing is action 0
        match['parking'] =int(endgame_action == 1) #parking is action 1
#    if not 'source' in match:
#        match['source'] = 'RAT'
    
    elif match['source'] == '3322':
        n_match = change_names(EAGLE_NAME_DICT, match)
#        print(list(n_match))
        n_match['auton_ci_switch'] = zealous_convert(match['Switch capabilities'])
        n_match['auton_ci_scale'] = zealous_convert(match['Scale capabilities'])
        n_match['auton_cube_count'] = 'NA'
        n_match['parking'] = eagle_climb_convert_parked(match['Climb'])
        n_match['climbing'] = eagle_climb_convert_climb(match['Climb'])
        n_match['cube_switch'] = match['Number of Cubes on Own Switch'] + match['Number of Cubes on Opponent\'s Switch']
        n_match['cube_count'] = 'NA'
        n_match['fouls'] = 'NA'
        n_match['tech_fouls'] = 'NA'
        match = n_match
#        print(list(match))
#        print('')
        
    return match

def powerup_process_scouting(scouting):
    print('processing scouting')
    preprocessed = process_scouting_by_match(scouting, powerup_process_match)
    print('combining sources')
    result = combine_scouting_from_sources(preprocessed, ['RAT', '3322'])
    return result

powerup_cats = ['cross_line',
                'auton_ci_switch',
                'auton_ci_scale',
                'auton_cube_count',
                'cube_count',
                'cube_switch',
                'cube_scale',
                'cube_vault',
                'fouls',
                'tech_fouls',
                'parking',
                'climbing',
                'hanging',
                'helping_robot',
                'source',
                'comments']
powerup_rankings = {'tech_fouls':0}
POWER_UP = Game(powerup_cats, powerup_cats[:-2], None, powerup_process_scouting, powerup_rankings)

#DEEP SPACE
def deepspace_process_scouting(scouting):
    pass

deepspace_cats = ['source',
                  'comments']
deepspace_rankings = {}

DEEP_SPACE = Game(deepspace_cats, deepspace_cats[:-2], None, deepspace_process_scouting, deepspace_rankings)

GAMES_FROM_YEARS = {'2017':STEAMWORKS,
                    '2018':POWER_UP,
                    '2019':DEEP_SPACE}
