# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:36:04 2018

@author: rober
"""

"""The module that contains the main application."""

import tkinter as tk
import math
import os
import scouting_data_getters as sdg
import games as gms
import graph as gph

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
                self.m_wid = 1200
            self.game = gms.GAMES_FROM_YEARS[self.year]
            
            #Get scouting
            self.raw_scouting = sdg.get_raw_scouting_data(self.comp)
            self.raw_scouting = self.game.process_scouting(self.raw_scouting)
            
            #Get contrs and averages
            self.contrs = gms.contrs(self.raw_scouting, self.game)
            self.averages = gms.averages_from_contrs(self.contrs)
            
            #Get categories
            scouting_cats = self.raw_scouting[list(self.raw_scouting.keys())[0]][0][1].keys()
            self.categories = gms.get_cats(scouting_cats, self.game.categories)
            self.numeric_cats = gms.get_cats(scouting_cats, self.game.numeric_categories, numeric=True)
            
            #Get teams
            self.teams = list(self.contrs.keys())
            
            self.error.set("")
            
            config_teams_frame()
            config_ranking_frame()
                
        def config_teams_frame():
            self.teams.sort(key=lambda t: int(t[3:]))
            num_in_chunk = 10
            
            self.teams_text.delete('1.0', tk.END) #Clear entire panel
            self.teams_text.insert(tk.INSERT, '\n')
            self.teams_text.insert(tk.INSERT, ' ' * (3*num_in_chunk - 3 + 10) + 'Teams:\n')

            for i in range(0, int((len(self.teams) / num_in_chunk) + 1)): #Go through teams in chunks of ten
                string = ' ' * 10
                for j in range(0, num_in_chunk):
                    index = num_in_chunk*i + j
                    if(index < len(self.teams)):
                        team = self.teams[index][3:]
                        ln = len(team)
                        string += team + ' '*(6-ln)
                        
                self.teams_text.insert(tk.INSERT, string + '\n')
                
#        def config_ranking_canvas(canvas, width=1343, height=50):
#            canvas.configure(scrollregion=canvas.bbox('all'))
#            canvas.config(width=width,height=height)
#            
#        def config_inner_ranking_canvas(canvas):
#            canvas.configure(scrollregion=canvas.bbox('all'))
#            canvas.config(width=100,height=500)
        
        def config_ranking_frame():
            
            def score(team):
                avs = self.averages[team]
                score = 0
                for cat in self.numeric_cats:
                    av = avs[cat]
                    w = float(self.cat_weight_fields[cat].get())
                    score += av * w
                return score
            
            def refresh_rankings():
                
                self.team_ranks_panel.pack_forget()
                self.team_ranks_panel = tk.Frame(self.ranking_frame)
                self.team_ranks_panel.grid(row=3, column=0)
                
                self.team_ranks_textbox = tk.Text(self.team_ranks_panel, width=24, wrap=tk.NONE)
                self.team_ranks_textbox.pack(side=tk.TOP)
                
                r_teams = self.teams[:]
                r_teams.sort(key=lambda t:-score(t))
                
                for i in range(0, len(r_teams)):
                    team = r_teams[i]
                    string = str(i+1) + ': ' + str(team[3:])
                    string += ' ' * (11-len(string)) + 'with ' + '%.2f' % score(team)
                    if i != len(r_teams) - 1:
                        string += '\n'
                    self.team_ranks_textbox.insert(tk.INSERT, chars=string)
                
                self.team_ranks_textbox.config(state=tk.DISABLED, height=30)
                    
            for child in self.ranking_frame.winfo_children():
                child.destroy()
            
            self.ranking_scroll = tk.Scrollbar(self.ranking_frame, orient=tk.HORIZONTAL)
            
            self.rank_box_canvas = tk.Canvas(self.ranking_frame, relief=tk.RAISED, xscrollcommand=self.ranking_scroll.set)
            
            self.ranking_scroll.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            self.rank_box_canvas.grid(row=1, column=0)
            self.rank_box_frame = tk.Frame(self.rank_box_canvas, relief=tk.RAISED)
            self.rank_box_frame.grid(row=0, column=0)
#            self.rank_box_frame.bind('<Configure>', lambda e: config_ranking_canvas(self.rank_box_canvas))
            self.rank_box_frame.bind('<Configure>', get_conf_canv(self.rank_box_canvas, width=1343, height=50))
            self.rank_box_canvas.create_window((0, 0), window=self.rank_box_frame, tags='self.rank_box_frame')
            self.ranking_scroll.config(command=self.rank_box_canvas.xview)
            
            self.cat_weight_fields = {}
            
            for cat in self.numeric_cats: #Construct weight-setting panel
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
                
            for line_data_type in line_data_types:
                data = line_data.get(line_data_type, '')
                length = len(line_data_type)
                inner_length = length - len(data.__str__())
                result += ' '*math.floor(inner_length /2) + data.__str__() + ' '*math.ceil(inner_length / 2) + ' '*2
             
            return result.rstrip()
        
        def get_column_string():
            """Return the string at the top of the scouting summary that labels the columns."""
            result = 'match_id  '
            for data_type in self.categories:
                result += data_type.__str__() + '  '
                
            return result.rstrip()
        
#        def config_text_canvas(canvas):
#            canvas.configure(scrollregion=canvas.bbox('all'))
#            canvas.config(width=1000,height=400)
        
        def show_summary():
            team = 'frc' + self.team_summary_team_field.get()
            self.team_summary_inner_frame.pack_forget()
            self.team_summary_inner_frame = tk.Frame(self.team_summary_canvas_frame, relief=tk.RAISED, borderwidth=1)
            self.team_summary_inner_frame.pack(side=tk.TOP)
            
            scouting_text_scrollbar = tk.Scrollbar(self.team_summary_inner_frame, orient=tk.HORIZONTAL)
            scouting_text_canvas = tk.Canvas(self.team_summary_inner_frame, xscrollcommand=scouting_text_scrollbar.set, width=1000)
            scouting_text_canvas.pack(side=tk.TOP, fill=tk.NONE)
#            self.team_summary_inner_frame.bind('<Configure>', lambda e: config_text_canvas(scouting_text_canvas))
            self.team_summary_inner_frame.bind('<Configure>', get_conf_canv(scouting_text_canvas, width=1000, height=400))
            
            scouting_text_pane = tk.Text(self.team_summary_canvas, wrap=tk.NONE)
            scouting_text_pane.grid(row=0, column=0)#(side=tk.TOP, fill=tk.NONE, padx=0, pady=1)
#            
            scouting_text_scrollbar.pack(side=tk.TOP, fill=tk.X, padx=150, pady=2)
            scouting_text_scrollbar.config(command=scouting_text_canvas.xview)
            
            scouting_text_canvas.create_window((0, 0), window=scouting_text_pane, anchor='nw', tags='scouting_text_pane')
            
            raw_team_scouting = self.raw_scouting.get(team, []) #Scouting for this team
            scouting_string_list = [get_column_string()]
            
            lens = [len(scouting_string_list[0])] #start with len of column string
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
            for category in self.numeric_cats:
                prediction = self.contrs[team][category]
                if not first:
                    tk.Label(self.team_summary_inner_frame, text=' ').pack(side=tk.TOP, padx=0, pady=5)
                label = tk.Label(self.team_summary_inner_frame, text=category + ':')
                label.pack(side=tk.TOP, padx=5, pady=5)
#                print(prediction)
                graph_data = gph.get_scouting_graph_data(prediction, red_and_blue=False, num_margins=None)
                graph_frame = gph.GraphDataPanel(self.team_summary_inner_frame, graph_data, g_height=100, max_width=self.m_wid/2)#, red_and_blue=False)
                graph_frame.pack(side=tk.TOP, padx=5, pady=5)
                
                first = False
        #end team summary methods
        
        def config_canvas(canvas, width=1343, height=650): #1343, 662   change to 2000
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.config(width=width,height=height)
        
        def get_conf_canv(canvas, width, height):
            return lambda event: config_canvas(canvas, width, height)
        
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

def main():
    """Run ZScout."""
    root = tk.Tk()
    root.geometry('350x250+300+300')
    tk.app = ZScoutFrame(root)
    root.mainloop()  

if __name__ == '__main__':
    main()
