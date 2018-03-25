"""
@Author: Komorebil
"""
from . import overwatch as OW
from . import game
from . import pool
from json import load
from sys import argv


def log(*args):
    print(args)


class Program(object):
    def __init__(self):
        self.game_instance = None
        self.argv = argv

    def _get_data(self, key):
        """
        Extract key from sys.argv, then delete the key
        """
        key += '='
        key_index = len(key)
        for i, s in enumerate(self.argv):
            if s[:key_index] == key:
                string = s[key_index:]
                del self.argv[i]
                return string
        return None

    def _user_input(self):
        """
        Retrieving info from user input in command line
        """
        # Getting fps
        fps = self._get_data('fps')
        info = {
            'fps': 2 if fps is None else fps,
            '_player': self._get_data('player'),
            'start_time': self._get_data('start_time') or 0,
            'end_time': self._get_data('end_time') or 0,
        }
        if len(self.argv) <= 3 or len(self.argv) > 4:
            raise ValueError("""
            Please input with proper amount of arguments.
            Example:
                main.exe F:/video.mp4 F:/ 0 players=player.txt fps=2 start_time=0 end_time=0

            Mandatory arguments:
                F:/video.mp4         Absolute path of video
                F:/                  Absolute path of output file
                0                    A number representing game type. 0: OWL, 1: Non-OWL

            Optional:
                players=players.txt  A text file saving info of all 12 players with JSON formatting
                fps=2                FPS of analyzer (2 by default)
                start_time=0         Starting time in seconds
                end_time=0           Ending time in seconds (If both are 0, then the whole video is analyzed)
            """)
        info['video_path'] = self.argv[1]
        info['output_path'] = self.argv[2]
        info['game_type'] = self.argv[3]
        return info

    def info(self):
        info = self._user_input()
        player_path = info.pop('_player')
        if player_path is None:
            info['name_team_left'] = 'Team A'
            info['name_team_right'] = 'Team B'
            info['name_players_team_left'] = ['player' + str(i) for i in range(1, 7)]
            info['name_players_team_right'] = ['player' + str(i) for i in range(7, 13)]
        else:
            data = load(open(player_path, 'r'))
            """
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
        return info

    def run(self):
        info = self.info()
        game_type = OW.GAMETYPE_OWL if info['game_type'] == 0 else OW.GAMETYPE_CUSTOM
        self.game_instance = game.Game(game_type)
        self.game_instance.set_game_info(info)
        self.game_instance.analyze(info['start_time'], info['end_time'], is_test=False)
        pool.PROCESS_POOL.close()
        pool.PROCESS_POOL.join()
        self.game_instance.output_to_json()
        self.game_instance.output_to_excel()
        log('ok')

program = Program()
