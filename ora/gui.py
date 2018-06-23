# coding: utf-8
"""
@Author: vega13
"""
import threading
import time
import tkinter
import requests
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from .request import json_request
from . import overwatch as OW
from . import game
from . import pool

def log(*args):
    print(args)

class Gui(object):
    def __init__(self):
        
        self.root = tkinter.Tk()
        self.root.title('Overwatch Replay Analyzer v0.1 Beta')
        self.root.geometry('550x350+400+200')

        self.read_path = None
        self.save_path = None
        self.left_frame = None
        self.right_frame = None
        # path
        self.create_path()
        self.create_time_inputs()
        # player
        self.create_player()
        # run
        self.run_btn = tkinter.Button(self.root, text="Analyze", command=self.run)
        self.run_btn.pack()
        self.create_text()
        # check for update
        self.t = threading.Thread(target=self.check_update)
        self.t.start()

    def create_path(self):
        width_msg = 100
        width_path = 400

        path_frame = tkinter.Frame(self.root)
        path_frame.pack(fill=X)
        # read
        read_frame = tkinter.Frame(path_frame)
        read_frame.pack(fill=X)
        read_msg = tkinter.Message(read_frame, width=width_msg, text='Video path:')
        read_msg.pack(side=LEFT)
        read_path = tkinter.Message(read_frame, width=width_path, text='file1')
        read_path.pack(side=LEFT)
        read_btn = tkinter.Button(read_frame, text="Choose file", command=self.click_read)
        read_btn.pack(side=RIGHT)
        # save
        save_frame = tkinter.Frame(path_frame)
        save_frame.pack(fill=X)
        save_msg = tkinter.Message(save_frame, width=width_msg, text='Save to:')
        save_msg.pack(side=LEFT)
        save_path = tkinter.Message(save_frame, width=width_path, text='file2')
        save_path.pack(side=LEFT)
        save_btn = tkinter.Button(save_frame, text="Choose file", command=self.click_save)
        save_btn.pack(side=RIGHT)

        self.read_path = read_path
        self.save_path = save_path

    def create_player(self):
        player = tkinter.Frame(self.root)
        player.pack(fill=X, expand=1)
        # left
        left_frame = tkinter.Frame(player)
        left_frame.pack(side=LEFT)
        left_team_name = tkinter.Entry(left_frame, bg='pink', fg='black')
        left_team_name.insert(0, 'Team A')
        left_team_name.pack()
        for i in range(1, 7):
            e = tkinter.Entry(left_frame, bg='red', fg='white')
            name = 'Player' + str(i)
            e.insert(0, name)
            e.pack()
        # right
        right_frame = tkinter.Frame(player)
        right_frame.pack(side=RIGHT)
        right_team_name = tkinter.Entry(right_frame, bg='lightBlue', fg='black')
        right_team_name.insert(0, 'Team B')
        right_team_name.pack()
        for i in range(7, 13):
            e = tkinter.Entry(right_frame, bg='blue', fg='white')
            name = 'Player' + str(i)
            e.insert(0, name)
            e.pack()

        self.left_frame = left_frame
        self.right_frame = right_frame

    def create_time_inputs(self):
        time_inputs_frame = tkinter.Frame(self.root)
        time_inputs_frame.pack(fill=X, expand=1)

        left_frame = tkinter.Frame(time_inputs_frame)
        left_frame.pack(side=LEFT)

        label_start_time = tkinter.Label(left_frame, text="Start time in seconds (0 = start from beginning):")
        label_end_time = tkinter.Label(left_frame, text="End time in seconds (0 = analyze till the end):")
        label_fps = tkinter.Label(left_frame, text='FPS of analyzer:')
        label_game_type = tkinter.Label(left_frame, text='Game type (0 = OWL, 1 = Custom game):')
        label_game_version = tkinter.Label(left_frame, text='OWL stage number(0=preseason, 1, 2, 3, 4):')
        label_start_time.pack()
        label_end_time.pack()
        label_fps.pack()
        label_game_type.pack()
        label_game_version.pack()

        right_frame = tkinter.Frame(time_inputs_frame)
        right_frame.pack(side=RIGHT)

        start_time = tkinter.Entry(right_frame, bg='lightBlue', fg='black')
        start_time.insert(0, '0')
        start_time.pack()
        end_time = tkinter.Entry(right_frame, bg='lightBlue', fg='black')
        end_time.insert(0, '0')
        end_time.pack()
        fps = tkinter.Entry(right_frame, bg='lightBlue', fg='black')
        fps.insert(0, '2')
        fps.pack()
        game_type = tkinter.Entry(right_frame, bg='lightBlue', fg='black')
        game_type.insert(0, '0')
        game_type.pack()
        game_version = tkinter.Entry(right_frame, bg='lightBlue', fg='black')
        game_version.insert(0, '1')
        game_version.pack()

        self.time_inputs_frame = right_frame
    def create_text(self):
        self.notice_window = tkinter.Toplevel(self.root)
        self.notice_window.title('Notice')
        self.notice_window.geometry('400x400+300+100')
        self.notice = tkinter.Text(self.notice_window)
        self.notice.insert(tkinter.INSERT, 
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
        import configparser
        config = configparser.ConfigParser()
        config.read('ora/etc/config.ini')

        current_version = config['version']['client_version']
        r = requests.get(
                config['api']['url'] + config['api']['check_update']
                + current_version
            ).json()

        if not r['is_latest']:
            tkinter.messagebox.showinfo('Update Available',
                'There is a newer version of ORA available, please download at \n{}'.format(r['url']))


    def info(self):
        valid = True
        info = {
            "name_team_left": "left",
            "name_team_right": "right",
            "name_players_team_left": [],
            "name_players_team_right": [],
            "video_path": "/",
            "output_path": "/",
            "start_time": 0,
            "end_time": 0,
            "fps": 0,
            "game_type": 0,
            "game_version": 1
        }
        frame_left = self.left_frame.pack_slaves()
        frame_right = self.right_frame.pack_slaves()
        time_inputs_frame = self.time_inputs_frame.pack_slaves()
        info['name_team_left'] = frame_left[0].get()
        info['name_team_right'] = frame_right[0].get()
        try:
            info['start_time'] = int(time_inputs_frame[0].get())
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'Invalid video start time!')
            valid = False
            return [info, valid]

        try:
            info['end_time'] = int(time_inputs_frame[1].get())
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'Invalid video end time!')
            valid = False
            return [info, valid]

        try:
            info['fps'] = int(time_inputs_frame[2].get())
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'Invalid analysis fps!')
            valid = False
            return [info, valid]

        if not (info['end_time'] >= 0 and info['start_time'] >= 0 \
            and info['end_time'] >= info['start_time']):
            tkinter.messagebox.showinfo('Error', 'Invalid video end time!')
            valid = False
            return [info, valid]

        if not (info['fps'] > 0):
            tkinter.messagebox.showinfo('Error', 'Invalid analysis fps!')
            valid = False
            return [info, valid]

        try:
            info['game_type'] = int(time_inputs_frame[3].get())
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'Invalid game type!')
            valid = False
            return [info, valid]

        try:
            info['game_version'] = int(time_inputs_frame[4].get())
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'Invalid owl stage number!')
            valid = False
            return [info, valid]
            
        if not (info['game_type'] == 0 or info['game_type'] == 1):
            tkinter.messagebox.showinfo('Error', 'Invalid game type!')
            valid = False
            return [info, valid]

        if not (info['game_version'] >= 0 or info['game_version'] < 5):
            tkinter.messagebox.showinfo('Error', 'Invalid OWL stage number!')
            valid = False
            return [info, valid]

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

        return [info, valid]

    def show(self):
        self.root.mainloop()

    def show_finish_msg(self):
        tkinter.messagebox.showinfo('An alert box', 'Output file successfully saved!')

    def show_progress(self, progress):
        self.notice.insert(Tkinter.INSERT, str(progress))

    def run(self):
        info, valid = self.info()
        game_type = OW.GAMETYPE_OWL if info['game_type'] == 0 else OW.GAMETYPE_CUSTOM
        self.game_instance = game.Game(game_type)
        if valid is True:
            self.game_instance.set_game_info(info)
            pool.initPool()

            try:
                self.game_instance.analyze(info['start_time'], info['end_time'], is_test=False)
            except Exception as err:
                print(err)
            else:
                self.game_instance.output()
                self.show_finish_msg()
                
            pool.PROCESS_POOL.close()
            pool.PROCESS_POOL.join()

gui_instance = Gui()