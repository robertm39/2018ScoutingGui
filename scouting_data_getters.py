# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 13:37:51 2018

@author: rober
"""

import os
import ast
import csv

#import categories as ct

def get_data(line_data):
    match_num = line_data['match_id']
    team_num = 'frc' + line_data['team_id'].__str__()
    
    result = {}
    for key in line_data.keys():
        if key != 'match_id' and key != 'team_id':
            result[key] = {match_num: {team_num: line_data[key]}}
    
    return result

def get_raw_scouting_data(folder):
    """Return the raw scouting data in the folder in a dict from teams to lists of tuples of match numbers and dicts from names to amounts."""
    result = {}
    directory = os.path.dirname(os.path.realpath(__file__)) + "\\scouting\\" + folder
#    print(directory)
    
    if not os.path.exists(directory):
        return {}
    
    for file in os.listdir(directory):
        
        file = open(directory + '\\' + file, "r", newline='') #newline=''
        
        line_datas = read_scouting(file)
        
        for line_data in line_datas:
            team_num = 'frc' + line_data['team_id'].__str__()
            
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


def get_scouting_data(get_data_from_match, folder):
    result = {}
    
    directory = os.path.dirname(os.path.realpath(__file__)) + "\\scouting\\" + folder
    #print("directory: " + directory)    
    
    if not os.path.exists(directory):
        return {}
    
    for file in os.listdir(directory):
        
        file = open(directory + '\\' + file, "r", newline='') #newline=''
        
        #print("file: " + file.__str__())
        file_data = get_file_scouting_data(get_data_from_match, file)
        
        for match_data in file_data:
            for category in match_data:
                #print("category: " + category.__str__())
                if not category in result:
                    result[category] = {}
                self_category_map = result[category]
                category_map = match_data[category]
                for match_num in category_map:
                    if not match_num in self_category_map:
                        self_category_map[match_num] = {}
                    self_team_map = self_category_map[match_num]
                    team_map = category_map[match_num]
                    for team in team_map:
                        if not team in self_team_map:
                            self_team_map[team] = team_map[team]
                        #else:
                        #    self_team_map + team_map[team]
            #print("")
    return result
        
def get_file_scouting_data(get_data_from_match, file):
    line_datas = read_scouting(file)
    return process_scouting(line_datas, get_data_from_match)

def eval_token(token):
    if token.lower() == 'true':
        return 1
    if token.lower() == 'false':
        return 0
    return ast.literal_eval(token)
#    try:
#        return float(token)
#    except ValueError:
#        return token

def read_scouting(file):
    """Return a list of lines."""
    lines = []
    
    csv_reader = csv.reader(file)
    for line in csv_reader:
        lines.append(line)
    order_line = lines[0]#.replace(',', ' ').split()
    lines = lines[1:]
    
    line_datas = []
    for data in lines:
#        line = line.replace('TRUE', 'True')
#        line = line.replace('FALSE', 'False')
#        line = line.replace('Yes', 'True')
#        line = line.replace('No', 'False')
#        
#        line = line.replace('True', '1')
#        line = line.replace('False', '0')
#        line = line.replace(' ', '_')
#        line = line.replace(',', ' ')
#        data = line.split()
        line_data = {}
        
        #print('data: ' + data.__str__())
        #if len(data) >= len(order_line) - 2:
        for i in range(0, len(order_line)):
            name = order_line[i]
#            if name != 'comments':
            #print("")
            #print(name)
            token_data = data[i]
            #print(token_data)
            try:
                #print(data[i])
                token_data = token_data.replace('\n', ' ').replace('\r', ' ') if name == 'comments' else eval_token(token_data)#ast.literal_eval(data[i])
            except SyntaxError:
                pass
            line_data[name] = token_data
        line_datas.append(line_data)
        
    return line_datas

def process_scouting(line_datas, get_data_from_match): #segmenter
    match_datas = []
    for line_data in line_datas:
        #print("line_data: " + line_data.__str__())
        match_data = get_data_from_match(line_data)
        match_datas.append(match_data)
    return match_datas

def get_chunk_entry_getter(get_min, get_max):
    pass