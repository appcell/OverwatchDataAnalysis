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
        从 sys.argv 中提取出 key，并把key从sys.argv中删除。
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
        获取用户从命令行输入的信息
        """
        # 获取 fps
        fps = self._get_data('fps')
        info = {
            'fps': 2 if fps is None else fps,
            '_player': self._get_data('player'),
            'start_time': self._get_data('start_time') or 0,
            'end_time': self._get_data('end_time') or 0,
        }
        if len(self.argv) <= 3 or len(self.argv) > 4:
            raise ValueError("""
            请输入正确数目的参数
            示例:
                main.exe F:/video.mp4 F:/ 0 players=player.txt fps=2 start_time=0 end_time=0

            其中:
                main.exe             为程序名
                F:/video.mp4         为视频名(绝对路径)
                F:/                  为文件保存的目录(绝对路径)
                0                    这里的值可为 0或1
                                     0 代表 owl, 1 代表 训练赛

            可选:
                players=players.txt  内容为"以json格式储存了12个玩家以及队员信息"的文本
                fps=2                为每一秒分析的帧数(默认为2)
                start_time=0         开始分析的时间（两者默认为0的话，
                end_time=0           结束分析的时间 则是分析整个视频）
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
            此处为 json 格式:
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
