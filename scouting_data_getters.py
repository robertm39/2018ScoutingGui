# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 13:37:51 2018

@author: rober
"""

import os
import ast
import csv
import imp

import games

def get_data(line_data):
    match_num = line_data['match_id']
    team_num = line_data['team_id'].__str__()
    
    result = {}
    for key in line_data.keys():
        if key != 'match_id' and key != 'team_id':
            result[key] = {match_num: {team_num: line_data[key]}}
    
    return result

def get_game(folder, year=None):
    directory = os.path.dirname(os.path.realpath(__file__)) + '\\scouting\\' + folder + '\\gamedef'# + '\\game_def.py'
    print('directory:', directory)
    try:
        for file_name in os.listdir(directory): #There should only be one .py file, but I don't know its name
#            The game should be defined in this file
#            module = __import__(directory)
            if not '__pycache__' in file_name:
                full_name = directory + '\\' + file_name
                print('full_name:', full_name)
                print('')
                file = open(directory + '\\' + file_name, 'r')
                module = imp.load_module(file_name,
                                         file,
                                         directory,
                                         details=('', 'r', imp.PY_SOURCE))
                game = module.get_game()
#                print(module)
#                print(game)
#                print(game.process_scouting)
#                print('')
                return game
    except FileNotFoundError:
        print('getting game from year')
        if year == None:
            #The first four letters of the folder will *probably* be the year
            year = folder[:4]
        return games.GAMES_FROM_YEARS[year]

def get_raw_scouting_data(folder):
    """Return the raw scouting data in the folder in a dict from teams to lists of tuples of match numbers and dicts from names to amounts."""
    result = {}
    directory = os.path.dirname(os.path.realpath(__file__)) + '\\scouting\\' + folder
    
    if not os.path.exists(directory):
        return {}
    
    for file_name in os.listdir(directory):
        
        if (not 'gamedef' in file_name) and (not '__pycache__' in file_name):
            
            file = open(directory + '\\' + file_name, 'r', newline='')
            line_datas = read_scouting(file)
            
            for line_data in line_datas:
                team_num = line_data['team_id'].__str__()
                
                match_num = line_data['match_id']
                line_data = line_data.copy()
                line_data.pop('team_id')
                line_data.pop('match_id')
                match_scouting_data = (match_num, line_data)
                
                if not team_num in result:
                    result[team_num] = []
                result[team_num].append(match_scouting_data)
                
            for team in result:
                result[team].sort(key=lambda m:m[0])
            
    return result

def eval_token(token):
    if token.lower() == 'true':
        return 1
    if token.lower() == 'false':
        return 0
    return ast.literal_eval(token)

def read_scouting(file):
    """Return a list of lines."""
    lines = []
    
    csv_reader = csv.reader(file)
    for line in csv_reader:
        lines.append(line) #Convert the csv into lists of tokens
    order_line = lines[0]  #The first line has the column headers
    lines = lines[1:]      #All the rest have the data
    
    line_datas = [] #I know
    for line in lines:
        line_data = {}
        
        for i in range(0, len(order_line)):
            name = order_line[i]
            token_data = line[i]
            if 'comments' in name.lower():
                #Get rid of newlines in comments
                token_data = token_data.replace('\n', ' ').replace('\r', ' ')
            else:
                try:
                    token_data = eval_token(token_data)
                except SyntaxError:
                    pass #Leave token_data as a string
            line_data[name] = token_data
        line_datas.append(line_data)
        
    return line_datas