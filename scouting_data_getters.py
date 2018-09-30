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
    """
    Return the given line data in a dict from categories to dicts from match nums to dicts from team nums to values
    
    Parameters:
        line_data: The line data to convert into a dict.
    """
    
    match_num = line_data['match_id']
    team_num = line_data['team_id'].__str__()
    
    result = {}
    for key in line_data.keys():
#        if not key in ['match_id', 'team_id']:
        if key != 'match_id' and key != 'team_id': #These values aren't added
            result[key] = {match_num: {team_num: line_data[key]}}
    
    return result

def get_game(folder, year=None):
    """
    Return the game in the given folder.
    
    Parameters:
        folder: The folder to game the game from.
        year: The year to get a game for.
    """
    
    directory = os.path.dirname(os.path.realpath(__file__)) + '\\scouting\\' + folder + '\\gamedef' #The full path of the directory to look in
    try:
        for file_name in os.listdir(directory): #There should only be one .py file, but I don't know its name
#            The game should be defined in this file
            if not '__pycache__' in file_name:
                file = open(directory + '\\' + file_name, 'r') #Open the file
                module = imp.load_module(file_name,
                                         file,
                                         directory,
                                         details=('', 'r', imp.PY_SOURCE)) #Load the python code in the file as a module
                game = module.get_game() #The module is supposed to have this method
                return game
    except FileNotFoundError:
        print('getting game from year')
        if year == None:
            #The first four letters of the folder will *probably* be the year
            year = folder[:4] #TODO make into robust regex for year 10,000 AD
        return games.GAMES_FROM_YEARS[year]

#These lines are here because at one competition we shared scouting data with team 3322 and they had a different format
#I could make this more robust and easily changeable
match_num_from_source = {'RAT':'match_id', '3322':'Match Number'}
team_num_from_source = {'RAT':'team_id', '3322':'Team Number'}

def get_raw_scouting_data(folder):
    """
    Return the raw scouting data in the folder in a dict from teams to lists of tuples of match numbers and dicts from names to amounts.
    
    Parameters:
        folder: The folder to get raw scouting data from.
    """
    
    result = {}
    directory = os.path.dirname(os.path.realpath(__file__)) + '\\scouting\\' + folder #The full name of the directory to search in.
    
    if not os.path.exists(directory):
        return {}
    
    for file_name in os.listdir(directory): #Go through every file and collect data
        
        if (not 'gamedef' in file_name) and (not '__pycache__' in file_name): #gamedef and pychache files don't have scouting data
            
            file = open(directory + '\\' + file_name, 'r', newline='') #Open the file to read from
            source = '3322' if '3322' in file_name.upper() else 'RAT' #Checking the source of the file
                                                                      #Because one time we shared scouting data with 3322
            line_datas = read_scouting(file, source=source) #Read the line data
                                                            #I said "datas"
                                                            #Ha ha ha, grammar man
            
            for line_data in line_datas: #Procees the line datas
#                team_num = line_data['team_id'].__str__()
                team_key = team_num_from_source[source] #Get the keys
                match_key = match_num_from_source[source] #Because once we shared scouting data with 3322
                
                team_num = line_data[team_key].__str__() #Get the team num
                
#                match_num = line_data['match_id']
                match_num = line_data[match_key]
                line_data = line_data.copy()
#                line_data.pop('team_id')
#                line_data.pop('match_id')
                line_data.pop(team_key) #Remove the team and match parts from the line data
                line_data.pop(match_key)
                match_scouting_data = (match_num, line_data)
                
                if not team_num in result:
                    result[team_num] = []
                result[team_num].append(match_scouting_data)
                
            for team in result:
                result[team].sort(key=lambda m:m[0]) #Sort by match number increasing
            
    return result

def eval_token(token):
    """
    Return the python object corresponding to the token.
    
    Parameters:
        token: The token to evaluate.
    """
    
    if token.lower() in ['true', 'yes']:
        return 1
    if token.lower() in ['false', 'no']:
        return 0
    try: 
        return ast.literal_eval(token) #Evaluate the token
    except ValueError: #Just a string
        return token

def read_scouting(file, source='RAT'):
    """
    Return a list of lines.
    
    Parameters:
        file: The file to read from.
        source: Which team made the file.
    """
    lines = []
    
    csv_reader = csv.reader(file) #To read the csv
    for line in csv_reader:
        lines.append(line) #Convert the csv into lists of tokens
        
    order_line = lines[0]  #The first line has the column headers
    lines = lines[1:]      #All the rest have the data
    
    line_datas = [] #I know
    for line in lines:
        line_data = {}
        
        for i in range(0, len(order_line)): #Go through all the data
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
            line_data[name] = token_data #Add the data
        line_data['source'] = source #Add the source data
        line_datas.append(line_data)
        
    return line_datas