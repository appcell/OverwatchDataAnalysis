"""
@Author: Komorebil
"""
from . import overwatch as OW
from . import game
from . import pool
from .cml import *
from sys import argv

__all__ = ['program']


class Program(object):
    def __init__(self):
        self.game_instance = None
        self.argv = argv
        self.data = self._get_data_to_dict()

    def _get_data_to_dict(self):
        if len(self.argv) < 4:
            raise ValueError(MSG.get('need_help'))

        result = {
            'video_path': self.argv[1],
            'output_path': self.argv[2],
            'game_type': self.argv[3],
        }
        for i, s in enumerate(self.argv[4:]):
            if '=' not in s:
                raise ValueError('<{}> {}'.format(s, MSG.get('lack')))
            k, v = s.split('=')
            result[k] = v
        return result

    def run(self):
        data = user_input(self.data)
        info = get_info(data)
        game_type = OW.GAMETYPE_OWL if info['game_type'] == 0 else OW.GAMETYPE_CUSTOM
        self.game_instance = game.Game(game_type)
        self.game_instance.set_game_info(info)
        self.game_instance.analyze(info['start_time'], info['end_time'], is_test=False)
        pool.PROCESS_POOL.close()
        pool.PROCESS_POOL.join()
        self.game_instance.output()
        log('ok')

program = Program()
