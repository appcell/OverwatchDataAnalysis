"""
@Author: Komorebil
"""
from . import overwatch as OW
from . import game
from . import pool
from .cml import *
from sys import argv
import json

__all__ = ['program']


class Program(object):
    def __init__(self):
        self.game_instance = None
        self.filename = argv[1]

    def run(self):
        with open(self.filename, 'r') as f:
            tasks = json.load(f)
        for i, task in enumerate(tasks):
            info = get_info(user_input(task))
            game_type = OW.GAMETYPE_OWL if info['game_type'] == 0 else OW.GAMETYPE_CUSTOM
            self.game_instance = game.Game(game_type)
            self.game_instance.set_game_info(info)
            self.game_instance.analyze(info['start_time'], info['end_time'], is_test=False)
            self.game_instance.output()
            log('{} done!'.format(i + 1))
        pool.PROCESS_POOL.close()
        pool.PROCESS_POOL.join()

program = Program()
