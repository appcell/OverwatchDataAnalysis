"""
@Author: Komorebil
"""
from . import overwatch as OW
from . import game
from . import pool
from sys import argv
import json


def log(*args):
    print(args)


class Program(object):
    def __init__(self):
        self.game_instance = None
        self.argv = argv[:4]
        self.msg = self._msg()
        self.data = self._get_data_to_dict(argv)

    def _get_data_to_dict(self, argv):
        if 'help' in argv:
            print(self.msg.get('help'))
            exit(0)
        if len(self.argv) < 4:
            raise ValueError(self.msg.get('need_help'))

        result = {}
        argv = argv[4:]
        if argv:
            for i, s in enumerate(argv):
                if '=' not in s:
                    raise ValueError('<{}> {}'.format(s, self.msg.get('lack')))
                k, v = s.split('=')
                result[k] = v
            return result
        return result

    @staticmethod
    def _msg():
        result = {}
        result['help'] = """
            Example:
                main_cli.exe <video_path> <output_path> <number> version=0 players=player.txt fps=2 start_time=0 end_time=0

            Mandatory arguments:
                <video_path>         Absolute path of video(example: F:/video.mp4)
                <output_path>        Absolute path of output file(example: F:/)
                <number>             A number representing game type. 0: OWL, 1: Non-OWL

            Optional:
                version=0            OWL stage number(0=preseason, 1, 2, 3, 4)
                players=players.txt  A text file saving info of all 12 players with JSON formatting
                fps=2                FPS of analyzer (2 by default)
                start_time=0         Starting time in seconds
                end_time=0           Ending time in seconds (If both are 0, then the whole video is analyzed)
        """
        result['need_help'] = """
            Please input with proper amount of arguments.
            If you need any help, please type: main_cli.py help
        """
        result['lack'] = "optional lack of token '='"
        result['json'] = """
        JSON format:
        {
            "right": {
                "players": [
                    "player7",
                    "player8",
                    "player9",
                    "player10",
                    "player11",
                    "player12"
                ],
                "team": "Team B"
            },
            "left": {
                "players": [
                    "player1",
                    "player2",
                    "player3",
                    "player4",
                    "player5",
                    "player6",
                ],
                "team": "Team A"
            }
        }
        """
        return result

    def _user_input(self):
        """
        Retrieving info from user input in command line
        """
        info = {
            'fps': self.data.get('fps', 2),
            '_players': self.data.get('players'),
            'start_time': self.data.get('start_time', 0),
            'end_time': self.data.get('end_time', 0),
            'game_version': self.data.get('version', 0),
            'video_path': self.argv[1],
            'output_path': self.argv[2],
            'game_type': self.argv[3]
        }
        return info

    def info(self):
        info = self._user_input()
        player_path = info.pop('_players')
        if player_path is None:
            info['name_team_left'] = 'Team A'
            info['name_team_right'] = 'Team B'
            info['name_players_team_left'] = ['player' + str(i) for i in range(1, 7)]
            info['name_players_team_right'] = ['player' + str(i) for i in range(7, 13)]
        else:
            try:
                with open(player_path, 'r') as f:
                    data = json.load(f)
            except json.decoder.JSONDecodeError:
                print(self.msg.get('json'))
                exit(0)
            info['name_team_left'] = data['left']['team']
            info['name_team_right'] = data['right']['team']
            info['name_players_team_left'] = data['left']['players']
            info['name_players_team_right'] = data['right']['players']

        try:
            info['start_time'] = int(info['start_time'])
        except ValueError:
            log('Invalid video start time!')

        try:
            info['end_time'] = int(info['end_time'])
        except ValueError:
            log('Invalid video end time!')

        try:
            info['fps'] = int(info['fps'])
        except ValueError:
            log('Invalid analysis fps!')

        if not (info['end_time'] >= info['start_time'] >= 0 and info['start_time'] >= 0):
            raise ValueError('Invalid video end time!')

        if not (info['fps'] > 0):
            raise ValueError('Invalid analysis fps!')

        try:
            info['game_type'] = int(info['game_type'])
        except ValueError:
            log('Invalid game type!')

        if not (info['game_type'] == 0 or info['game_type'] == 1):
            raise ValueError('Invalid game type!')

        try:
            print(info['game_version'])
            info['game_version'] = int(info['game_version'])
        except ValueError:
            log('Invalid OWL stage number!')

        if info['game_type'] == 0 and info['game_version'] not in [0, 1, 2, 3, 4]:
            raise ValueError('Invalid OWL stage number!')
        return info

    def run(self):
        info = self.info()
        game_type = OW.GAMETYPE_OWL if info['game_type'] == 0 else OW.GAMETYPE_CUSTOM
        self.game_instance = game.Game(game_type)
        self.game_instance.set_game_info(info)
        self.game_instance.analyze(info['start_time'], info['end_time'], is_test=False)
        pool.PROCESS_POOL.close()
        pool.PROCESS_POOL.join()
        self.game_instance.output()
        log('ok')

program = Program()
