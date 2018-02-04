# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:36:04 2018

@author: rober
"""

"""The module that contains the main application."""

import tkinter as tk
import math
import os
import scoutingdatagetters as sdg
import games as gms

class CannotGetCompetitionError(BaseException):
    pass

class ZScoutFrame(tk.Frame):
    """The frame the ZScout Gui is in."""
           
    def __init__(self, parent):
        """Make a ZScoutFrame."""
        
        tk.Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        
        self.full_file_name = self.dir_path + "\\cache.zsc"
        
        self.initUI()
    
    def initUI(self):
        """Initialize the user interface."""
        #frame methods
        def go_to_scouting_frame():
            go_to_frame(self.scouting_frame)
        
        def go_to_teams_frame():
            go_to_frame(self.teams_frame)
        
        def go_to_competition_frame():
            go_to_frame(self.competition_frame)
        
        def go_to_ranking_frame():
            go_to_frame(self.ranking_frame)
        
        def go_to_frame(frame):
            if self.active_frame == frame:
                return
            self.active_frame.pack_forget()
            frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.active_frame = frame
        #end frame methods

        #scouting methods
        def set_comp():
            """Set the current competition to the one specified in the comp_choose field, set relevant variables, and get team contribution data."""
            self.comp = self.comp_choose.get()
            self.year = self.comp[:4]
            if self.year == '2017':
                self.m_wid = 1200
            else:
                self.m_wid = 600
            self.game = gms.GAMES_FROM_YEARS[self.year]

            self.raw_scouting = sdg.get_raw_scouting_data(self.comp)
            self.contrs = gms.contrs(self.raw_scouting, self.game)
            self.averages = gms.averages_from_contrs(self.contrs)
            self.categories = self.game.categories
            self.teams = list(self.contrs.keys())
            
            self.error.set("")
            
            config_teams_frame()
            config_ranking_frame()
                
        def config_teams_frame():
            self.teams.sort(key=lambda t: int(t[3:]))
            num_in_chunk = 10
            self.teams_text.insert(tk.INSERT, '\n')
            self.teams_text.insert(tk.INSERT, ' ' * (3*num_in_chunk - 3 + 10) + 'Teams:\n')

            for i in range(0, int((len(self.teams) / num_in_chunk) + 1)):
                string = ' ' * 10
                for j in range(0, num_in_chunk):
                    ind = num_in_chunk*i + j
                    if(ind < len(self.teams)):
                        team = self.teams[ind][3:]
                        ln = len(team)
                        string += team + ' '*(6-ln)
                        
                self.teams_text.insert(tk.INSERT, string + '\n')
                
        def config_ranking_canvas(canvas, width=1343, height=50):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.config(width=width,height=height)
            
        def config_inner_ranking_canvas(canvas):
                canvas.configure(scrollregion=canvas.bbox('all'))
                canvas.config(width=100,height=500)
        
        def config_ranking_frame():
            
            def score(team):
                avs = self.averages[team]
                score = 0
#                print('')
                for cat in self.game.numeric_categories:
                    av = avs[cat]
                    w = float(self.cat_weight_fields[cat].get())
#                    print(cat, av, w)
                    score += av * w
                return score
            
            
            
            def refresh_rankings():
                
                self.team_ranks_panel.pack_forget()
                self.team_ranks_panel = tk.Frame(self.ranking_frame)
                self.team_ranks_panel.grid(row=3, column=0)
                
#                self.team_ranks_canvas_scroll = tk.Scrollbar(self.team_ranks_panel, orient=tk.VERTICAL)
                
#                self.team_ranks_canvas = tk.Canvas(self.team_ranks_panel)#, yscrollcommand=self.team_ranks_canvas_scroll.set)
#                self.team_ranks_canvas.grid(row=0, column=0)
#                self.team_ranks_panel.bind('<Configure>', lambda e: config_inner_ranking_canvas(self.team_ranks_canvas))
#                self.team_ranks_canvas_scroll.config(command=self.team_ranks_canvas.yview)
                
#                self.team_ranks_canvas_scroll.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E)#+tk.W)
                
                self.team_ranks_inner_panel = tk.Frame(self.team_ranks_panel)#self.team_ranks_canvas)
                self.team_ranks_inner_panel.pack(side=tk.TOP)#grid(row=0, column=0)
                
#                self.team_ranks_canvas.create_window((0, 0), window=self.team_ranks_inner_panel, anchor='nw', tags='self.team_ranks_inner_panel')
                
                self.team_ranks_textbox = tk.Text(self.team_ranks_inner_panel, width=25)
                self.team_ranks_textbox.pack(side=tk.TOP)
                
                r_teams = self.teams[:]
                r_teams.sort(key=lambda t:-score(t))
                for i in range(0, len(r_teams)):
                    team = r_teams[i]
                    string = str(i+1) + ': ' + str(team[3:])
                    string += ' ' * (11-len(string)) + 'with ' + '%.2f' % score(team)# + '\n'
#                    print('length:', len(string))
                    if i != len(r_teams) - 1:
                        string += '\n'
                    self.team_ranks_textbox.insert(tk.INSERT, chars=string)
#                    t_label = tk.Label(self.team_ranks_inner_panel, text=string, anchor=tk.CENTER)
#                    t_label.pack(side=tk.TOP)
                self.team_ranks_textbox.config(state=tk.DISABLED)
                    
                
            for child in self.ranking_frame.winfo_children():
                child.destroy()
            
            self.ranking_scroll = tk.Scrollbar(self.ranking_frame, orient=tk.HORIZONTAL)
            
            self.rank_box_canvas = tk.Canvas(self.ranking_frame, relief=tk.RAISED, xscrollcommand=self.ranking_scroll.set)
            
            self.ranking_scroll.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            self.rank_box_canvas.grid(row=1, column=0)
            self.rank_box_frame = tk.Frame(self.rank_box_canvas, relief=tk.RAISED)
            self.rank_box_frame.grid(row=0, column=0)
            self.rank_box_frame.bind('<Configure>', lambda e: config_ranking_canvas(self.rank_box_canvas))
            self.rank_box_canvas.create_window((0, 0), window=self.rank_box_frame, tags='self.rank_box_frame')
            self.ranking_scroll.config(command=self.rank_box_canvas.xview)
            
            self.cat_weight_fields = {}
            
            for cat in self.game.numeric_categories: #Construct weight_setting panel
                entry_panel = tk.Frame(self.rank_box_frame, relief=tk.RAISED)
                entry_panel.pack(side=tk.LEFT)
                
                label = tk.Label(entry_panel, text=cat)
                label.pack(side=tk.TOP)
                entry = tk.Entry(entry_panel)
                entry.insert(index=0, string='0.0')
                entry.pack(side=tk.TOP)
                self.cat_weight_fields[cat] = entry
            
            self.ranking_refresh_button = tk.Button(self.ranking_frame, text='Refresh Rankings', command=refresh_rankings)
            self.ranking_refresh_button.grid(row=2, column=0)
            
            self.team_ranks_panel = tk.Frame(self.ranking_frame)
            self.team_ranks_panel.grid(row=3, column=0)
            
        #end scouting methods
        
        #team summary methods
        def get_match_scouting_string(match, line_data):
            """Return a string describing the match and line data in human-readable format."""
            
            result = ''
            
            line_data_types = ['match_id']
            line_data['match_id'] = match
            for data_type in self.categories:
                line_data_types.append(data_type)
                
#            print('line_data:', line_data)
            for line_data_type in line_data_types:
                data = line_data.get(line_data_type, '')
#                print('data:', data, 'line_data_type:', line_data_type, 'length:', len(line_data_type))
                length = len(line_data_type)
                
                inner_length = length - len(data.__str__())
#                print('inner_length:', inner_length)
#                print('')
                result += ' '*math.floor(inner_length /2) + data.__str__() + ' '*math.ceil(inner_length / 2) + ' '*2
             
            return result.rstrip()
        
        def get_column_string():
            """Return the string at the top of the scouting summary that labels the columns."""
            result = 'match_id  '
            for data_type in self.categories:
                result += data_type.__str__() + '  '
                
            return result.rstrip()
        
        def config_text_canvas(canvas):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.config(width=1000,height=400)
        
        def show_summary():
            team = 'frc' + self.team_summary_team_field.get()
            self.team_summary_inner_frame.pack_forget()
            self.team_summary_inner_frame = tk.Frame(self.team_summary_canvas_frame, relief=tk.RAISED, borderwidth=1)
            self.team_summary_inner_frame.pack(side=tk.TOP)
            
            scouting_text_scrollbar = tk.Scrollbar(self.team_summary_inner_frame, orient=tk.HORIZONTAL)
            scouting_text_canvas = tk.Canvas(self.team_summary_inner_frame, xscrollcommand=scouting_text_scrollbar.set, width=1000)
            scouting_text_canvas.pack(side=tk.TOP, fill=tk.NONE)
            self.team_summary_inner_frame.bind('<Configure>', lambda e: config_text_canvas(scouting_text_canvas))
            
            scouting_text_pane = tk.Text(self.team_summary_canvas, wrap=tk.NONE)
            scouting_text_pane.grid(row=0, column=0)#(side=tk.TOP, fill=tk.NONE, padx=0, pady=1)
#            
            scouting_text_scrollbar.pack(side=tk.TOP, fill=tk.X, padx=150, pady=2)
            scouting_text_scrollbar.config(command=scouting_text_canvas.xview)
            
            scouting_text_canvas.create_window((0, 0), window=scouting_text_pane, anchor='nw', tags='scouting_text_pane')
            
            raw_team_scouting = self.raw_scouting.get(team, []) #Scouting for this team
            scouting_string_list = [get_column_string()]
            
            lens = []
            for match, line_data in raw_team_scouting:
                string = get_match_scouting_string(match, line_data)
                lens.append(len(string))
                scouting_string_list.append(get_match_scouting_string(match, line_data))
            av_string = get_match_scouting_string('Avs:', self.averages[team])
            lens.append(len(av_string))
            scouting_string_list.append(av_string)
            
            #Expand text box to right width
            scouting_text_pane.config(width = max(lens) + 1)
            
            for s in scouting_string_list:
                scouting_text_pane.insert(tk.INSERT, s + '\n')
            scouting_text_pane.config(state=tk.DISABLED)
            
            first=True
            
            #Graphs
            for category in self.game.numeric_categories:
                prediction = self.contrs[team][category]
                if not first:
                    tk.Label(self.team_summary_inner_frame, text=' ').pack(side=tk.TOP, padx=0, pady=5)
                label = tk.Label(self.team_summary_inner_frame, text=category + ':')
                label.pack(side=tk.TOP, padx=5, pady=5)
#                print(prediction)
                graph_data = get_scouting_graph_data(prediction, red_and_blue=False, num_margins=None)
                graph_frame = GraphDataPanel(self.team_summary_inner_frame, graph_data, g_height=100, max_width=self.m_wid/2)#, red_and_blue=False)
                graph_frame.pack(side=tk.TOP, padx=5, pady=5)
                
                first = False
        #end team summary methods
        
        def config_canvas(canvas, width=1343, height=650): #1343, 662   change to 2000
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.config(width=width,height=height)
        
        
        def setup_menu():
            self.menubar = tk.Menu(self)
            self.frame_select = tk.Menu(self.menubar, tearoff=0)
            self.frame_select.add_command(label='Scouting', command=go_to_scouting_frame)
            self.frame_select.add_command(label='Teams', command=go_to_teams_frame)
            self.frame_select.add_command(label='Competition', command=go_to_competition_frame)
            self.frame_select.add_command(label='Ranking', command=go_to_ranking_frame)
            self.menubar.add_cascade(label='Sections', menu=self.frame_select)
            self.parent.config(menu=self.menubar)
        
        def setup_team_summary_frame():
            self.scouting_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
            self.active_frame = self.scouting_frame
            
            self.team_summary_y_scroll = tk.Scrollbar(self.scouting_frame, orient=tk.VERTICAL)
            self.team_summary_y_scroll.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
            
            self.team_summary_canvas = tk.Canvas(self.scouting_frame, yscrollcommand=self.team_summary_y_scroll.set)
            self.team_summary_canvas.grid(row=0, column=0)
            
            self.team_summary_canvas_frame = tk.Frame(self.team_summary_canvas)
            self.team_summary_canvas_frame.bind('<Configure>', lambda e: config_canvas(self.team_summary_canvas))
            
            self.team_summary_canvas.create_window((0,0), window=self.team_summary_canvas_frame, anchor='nw', tags='self.team_summary_canvas_frame')
            
            self.team_summary_y_scroll.config(command=self.team_summary_canvas.yview)
            
            self.team_summary_team_label = tk.Label(self.team_summary_canvas_frame, text='Team:')
            self.team_summary_team_label.pack(side=tk.TOP, padx=5, pady=5)
            
            self.team_summary_team_field = tk.Entry(self.team_summary_canvas_frame)
            self.team_summary_team_field.pack(side=tk.TOP, padx=5, pady=5)
            
            self.team_summary_button = tk.Button(self.team_summary_canvas_frame, command=show_summary, text='Show Summary')
            self.team_summary_button.pack(side=tk.TOP, padx=5, pady=5)
            
            self.team_summary_inner_frame = tk.Frame(self.team_summary_canvas_frame, relief=tk.RAISED, borderwidth=1)
        
        def setup_comp_frame():
            #vars
            self.error = tk.StringVar()
            self.contrs_from_team_from_category = {}
            self.categories = []
            #end vars
            
            self.competition_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
            self.comp_label = tk.Label(self.competition_frame, text="Competition:")
            self.comp_label.pack(side=tk.TOP, padx=5, pady=5)
    
            self.comp_choose = tk.Entry(self.competition_frame)
            self.comp_choose.pack(side=tk.TOP, padx=5, pady=5)
    
            self.comp_button = tk.Button(self.competition_frame, text="Accept", command=set_comp)
            self.comp_button.pack(side=tk.TOP, padx=5, pady=5)
    
            self.error_label = tk.Label(self.competition_frame, textvariable=self.error)
            self.error_label.pack(side=tk.TOP, pady=5)
        
        def setup_ranking_frame():
            self.ranking_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        
        def setup_teams_frame():
            self.teams_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
            self.teams_text = tk.Text(self.teams_frame, wrap=tk.NONE, width=1200)
            self.teams_text.pack(side=tk.TOP, padx=0, pady=5)
        
        self.parent.title('ZScout')
        self.pack(fill=tk.BOTH, expand=True)
        self.year = ''
        
        setup_menu()
        setup_team_summary_frame()
        setup_comp_frame()
        setup_ranking_frame()
        setup_teams_frame()

def get_scouting_graph_data(match_data, red_and_blue, num_margins=None):
    
    MARGIN_TIERS = [1, 5, 15, 25, 50, 100, 150, 200, 250, 300]
    
    def get_num_margins(max_red_margin, max_blue_margin):
            if num_margins == None:
                result = None
                result = max(max_red_margin, max_blue_margin)#*2 + 1
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
    
    def get_margin(match): #Get rid of this come un-kludge day
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
    
    def __init__(self, parent, graph_data, g_height=600, max_width = 1300, disp_probs=False, pix_per_margin=None, text_pad=16):
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
        
        self.pad = 2
        
        tot_height = g_height + text_pad
        
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
            if y < 20:
                return y + 10
            return y - 7
        
        tk.Frame.__init__(self, parent, background="white")
        
        num_margins = len(graph_data.margins)
        pix_per_margin = get_pix_per_margin(num_margins)
        
        if num_margins == 1: #make one-margin graphs thinner
            max_width /= 2
        
        self.canvas = tk.Canvas(self, width=get_x((num_margins // 2) if graph_data.red_and_blue else num_margins) + 1*pix_per_margin, height=tot_height, bd=1, bg="white")
        self.canvas.pack(side=tk.TOP)
        
        h_w = pix_per_margin // 2
        
        light_gray = "#efefef"
        darker_gray = "#dfdfdf"
        even_darker_gray = "#9f9f9f"
        
        for margin in graph_data.label_margins:
            x = get_x(margin)
            top = 15

            self.canvas.create_text(x, 8, text=abs(margin).__str__())
            if margin % 10 == 0:
                if margin == 0:
                    self.canvas.create_line(x, tot_height, x, top, fill = even_darker_gray)
                else:
                    self.canvas.create_line(x, tot_height, x, top, fill = darker_gray)
            else:
                self.canvas.create_line(x, tot_height, x, top, fill = light_gray)
        self.canvas.create_line(0, tot_height, get_x(num_margins / 2 + 5), tot_height)
        self.canvas.create_line(0, get_y(1.0), get_x(num_margins / 2 + 5), get_y(1.0))#, fill = light_gray)
        self.canvas.create_line(0, get_y(0.75), get_x(num_margins / 2 + 5), get_y(0.75), fill = light_gray)
        self.canvas.create_line(0, get_y(0.5), get_x(num_margins / 2 + 5), get_y(0.5), fill = light_gray)
        self.canvas.create_line(0, get_y(0.25), get_x(num_margins / 2 + 5), get_y(0.25), fill = light_gray)
        
        for margin in graph_data.margins.keys():
            prob, color = graph_data.margins[margin]
            
            y = get_y(prob)
            x = get_x(margin)
            
            if not y == tot_height:
                self.canvas.create_rectangle(x-h_w, tot_height, x+h_w, y, fill=color)
                
            text_y = get_percent_height(y)
            self.canvas.create_text(x+3, text_y, text=(int((prob*100 + 0.5))).__str__() + '%') #to the tenth percent

def main():
    """Run ZScout."""
    root = tk.Tk()
    root.geometry('350x250+300+300')
    tk.app = ZScoutFrame(root)
    root.mainloop()  

if __name__ == '__main__':
    main()
