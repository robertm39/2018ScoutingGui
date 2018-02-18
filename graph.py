# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 21:21:09 2018

@author: rober
"""

import math

import tkinter as tk

def get_scouting_graph_data(match_data, red_and_blue, num_margins=None):
    
    MARGIN_TIERS = [1, 5, 15, 25, 50, 100, 150, 200, 250, 300, 400, 500, 1000]
    
    def get_num_margins(max_red_margin, max_blue_margin):
            if num_margins == None:
                result = None
                result = max(max_red_margin, max_blue_margin)
                for tier in MARGIN_TIERS:#(TWO_SIDE_MARGIN_TIERS if red_and_blue else ONE_SIDE_MARGIN_TIERS):
                    if result <= tier:
                        result = tier*2+1 if red_and_blue else tier
                        #print('num_margins: ' + result.__str__())
                        return result
                tier = MARGIN_TIERS[-1]
                return tier*2+1 if red_and_blue else tier
            else:
                return num_margins
        
    def get_one_side_margins():
        return (num_margins // 2 - 1) if red_and_blue else num_margins
    
    def get_margin(match):
        """Return the margin of the match's scores. Matches blue wins in have a negative margin."""
        return match
        
    def data_sort(match):
        """Return the margin of the match's scores. Used as a sort key."""
        return get_margin(match)
    
    class GraphData:
        def __init__(self, red_and_blue, margins, label_margins):
            self.red_and_blue = red_and_blue
            self.margins = margins
            self.label_margins = label_margins
    
    max_red_margin = 0
    max_blue_margin = 0
    for match in match_data:
        if match_data[match] > 0:
            max_red_margin = max(max_red_margin, abs(get_margin(match)))
            max_blue_margin = max(max_blue_margin, abs(-get_margin(match)))
    
    num_margins = get_num_margins(max_red_margin, max_blue_margin)
    
    margins = {}
    
    if red_and_blue:
        for i in range(-(num_margins // 2), num_margins//2 + 1):
            margins[i] = match_data.get(i, 0), 'red' if i > 0 else 'blue' if i < 0 else 'magenta'
    else:
        for i in range(0, num_margins + 1):
            margins[i] = match_data.get(i, 0), 'red' if i > 0 else 'magenta'

    label_margins = list(margins.keys())
    
    result = GraphData(red_and_blue, margins, label_margins)
    
    return result

class GraphDataPanel(tk.Frame): #clean up
    """A Panel that shows predicted match score information in a graph."""
    
    def __init__(self, parent, graph_data, g_height=600, max_width=1300, disp_probs=False, pix_per_margin=None, text_pad=16):
        """Make a GraphDataPanel.
        
        Arguments:
            parent -- the parent of the GraphDataPanel
            match_data -- the match score data to show in the graph
        
        Keyword Arguments:
            g_height -- the height of the graph (default 600)
            max_width -- the maximum width of the graph (default 1300)
            pix_per_margin -- how many pixels each bar gets (default None)
            text_pad -- how much padding to have for the bar labels (default 16)
            num_margins -- how many margins to show on the graph (default None)
        """
        
        def get_x(margin):
            """Return the x value of the center of the bar for the margin."""
            return pix_per_margin * (((num_margins // 2) if graph_data.red_and_blue else 0) + margin + 1)

        def get_y(prob):
            """Return the y value of the top of a bar representing this prob."""
            if prob == 0:
                return text_pad + g_height
            return text_pad + min(g_height - 1, (1 - prob) * g_height)
         
        def get_pix_per_margin(num_margins):
            """Return how many pixels wide each bar should be."""
            if pix_per_margin == None:
                result = math.floor(max_width / (num_margins + 1))
                return result
            return pix_per_margin
        
        def get_percent_height(y):
            """Return the y coordinate of the % label."""
            if y < 20: #For tall bars, the % sign is inside the bar
                return y + 10
            return y - 7 #For most bars, the % sign is above the bar
        
        def create_horizontal_graph_line(percent, **kwargs):
            self.canvas.create_line(0, get_y(percent), get_x(num_margins / 2 + 5), get_y(percent), **kwargs)
        
        def create_vertical_graph_line(x, **kwargs):
            self.canvas.create_line(x, get_y(0), x, get_y(1), **kwargs)
        
        tk.Frame.__init__(self, parent, background="white")
        
        num_margins = len(graph_data.margins)
        pix_per_margin = get_pix_per_margin(num_margins)
        
        if num_margins == 1: #make one-margin graphs thinner
            max_width /= 2
        
        self.canvas = tk.Canvas(self,
                                width=get_x((num_margins // 2) if graph_data.red_and_blue else num_margins) + 1*pix_per_margin,
                                height=get_y(0),
                                bd=1,
                                bg="white")
        self.canvas.pack(side=tk.TOP)
        
        h_w = pix_per_margin // 2 #The distance from the center of a bar to the edge
        
        light_gray = "#efefef"
        darker_gray = "#dfdfdf"
        even_darker_gray = "#9f9f9f"
        
        #Top and bottom outlines of graph
        create_horizontal_graph_line(percent=0)
        create_horizontal_graph_line(percent=1)
        
        #Horizontal lines in middle of graph
        create_horizontal_graph_line(percent=0.25, fill=light_gray)
        create_horizontal_graph_line(percent=0.5, fill=light_gray)
        create_horizontal_graph_line(percent=0.75, fill=light_gray)
        
        for margin in graph_data.label_margins:
            x = get_x(margin)
            text_y = 8
            
            self.canvas.create_text(x, text_y, text=str(abs(margin)))
            fill = light_gray
            if margin % 10 == 0:
                if margin == 0:
                    fill = even_darker_gray
                else:
                    fill = darker_gray
            create_vertical_graph_line(x, fill=fill)
        
        for margin in graph_data.margins.keys():
            prob, color = graph_data.margins[margin]
            
            y = get_y(prob)
            x = get_x(margin)
            
            if not y == get_y(0):
                self.canvas.create_rectangle(x-h_w, get_y(0), x+h_w, y, fill=color)
                
            text_y = get_percent_height(y)
            percent_text = str(int((prob*100 + 0.5))) + '%'
            self.canvas.create_text(x+3, text_y, text=percent_text) #to the tenth percent