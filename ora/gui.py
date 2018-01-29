# coding: utf-8
"""
@Author: vega13
"""
import threading
import time
import tkMessageBox
import tkFileDialog as filedialog
from request import json_request
import Tkinter
from Tkinter import (Tk,
                     Frame, Message, Button, Entry, Toplevel,
                     Label, Text, X, LEFT, RIGHT)
import overwatch as OW
import game

def log(*args):
    print args

class Gui(object):
    def __init__(self):
        
        self.root = Tk()
        self.root.title('Overwatch Replay Analyzer')
        self.root.geometry('500x300+400+200')

        self.read_path = None
        self.save_path = None
        self.left_frame = None
        self.right_frame = None
        # path
        self.create_path()
        # player
        self.create_player()
        # run
        self.run_btn = Button(self.root, text="Analyze", command=self.run)
        self.run_btn.pack()
        self.create_text()
        # check for update
        self.t = threading.Thread(target=self.check_update)
        self.t.start()

    def create_path(self):
        width_msg = 100
        width_path = 400

        path_frame = Frame(self.root)
        path_frame.pack(fill=X)
        # read
        read_frame = Frame(path_frame)
        read_frame.pack(fill=X)
        read_msg = Message(read_frame, width=width_msg, text='Video path:')
        read_msg.pack(side=LEFT)
        read_path = Message(read_frame, width=width_path, text='file1')
        read_path.pack(side=LEFT)
        read_btn = Button(read_frame, text="Choose file", command=self.click_read)
        read_btn.pack(side=RIGHT)
        # save
        save_frame = Frame(path_frame)
        save_frame.pack(fill=X)
        save_msg = Message(save_frame, width=width_msg, text='Save to:')
        save_msg.pack(side=LEFT)
        save_path = Message(save_frame, width=width_path, text='file2')
        save_path.pack(side=LEFT)
        save_btn = Button(save_frame, text="Choose file", command=self.click_save)
        save_btn.pack(side=RIGHT)

        self.read_path = read_path
        self.save_path = save_path

    def create_player(self):
        player = Frame(self.root)
        player.pack(fill=X, expand=1)
        # left
        left_frame = Frame(player)
        left_frame.pack(side=LEFT)
        left_team_name = Entry(left_frame, bg='pink', fg='black')
        left_team_name.insert(0, 'Team A')
        left_team_name.pack()
        for i in range(1, 7):
            e = Entry(left_frame, bg='red', fg='white')
            name = 'Player' + str(i)
            e.insert(0, name)
            e.pack()
        # right
        right_frame = Frame(player)
        right_frame.pack(side=RIGHT)
        right_team_name = Entry(right_frame, bg='lightBlue', fg='black')
        right_team_name.insert(0, 'Team B')
        right_team_name.pack()
        for i in range(7, 13):
            e = Entry(right_frame, bg='blue', fg='white')
            name = 'Player' + str(i)
            e.insert(0, name)
            e.pack()

        self.left_frame = left_frame
        self.right_frame = right_frame

    def create_text(self):
        self.notice_window = Toplevel(self.root)
        self.notice_window.title('Notice')
        self.notice_window.geometry('400x400+300+100')
        self.notice = Text(self.notice_window)
        self.notice.insert(Tkinter.INSERT, 
            """Overwatch Replay Analyzer, a data extractor of Overwatch game replays

Copyright (C) 2017-2018 ORA developers

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

You can contact the author or report issues by: https://github.com/appcell/OverwatchDataAnalysis/issues""")
        self.notice.pack()

    def click_save(self):
        filename = filedialog.askdirectory(initialdir='~/')
        self.save_path.config(text=filename)

    def click_read(self):
        # self.root.
        filename = filedialog.askopenfilename(initialdir='~/OW/OverwatchDataAnalysis/videos')
        self.read_path.config(text=filename)

    def check_update(self):
        version = {
            'name': 'ORA OWL',
            'current_version': 0.1,
        }

    def info(self):
        info = {
            "name_team_left": "left",
            "name_team_right": "right",
            "name_players_team_left": [],
            "name_players_team_right": [],
            "video_path": "/",
            "output_path": "/",
        }
        frame_left = self.left_frame.pack_slaves()
        frame_right = self.right_frame.pack_slaves()

        info['name_team_left'] = frame_left[0].get()
        info['name_team_right'] = frame_right[0].get()
        #
        team_left = []
        team_right = []
        for i in range(1, 7):
            player_left = frame_left[i].get()
            team_left.append(player_left)
            player_right = frame_right[i].get()
            team_right.append(player_right)

        info['name_players_team_left'] = team_left
        info['name_players_team_right'] = team_right
        info['video_path'] = self.read_path['text']
        info['output_path'] = self.save_path['text']

        return info

    def show(self):
        self.root.mainloop()

    def show_finish_msg(self):
        tkMessageBox.showinfo('一个微小的弹窗', '保存成功！')

    def show_progress(self, progress):
        self.notice.insert(Tkinter.INSERT, str(progress))

    def run(self):
        self.game_instance = game.Game(OW.GAMETYPE_OWL, OW.ANALYZER_FPS)
        self.game_instance.set_game_info(self.info())
        self.game_instance.analyze(289, 292, is_test=False)
        self.game_instance.output_to_excel()
        self.show_finish_msg()

gui_instance = Gui()