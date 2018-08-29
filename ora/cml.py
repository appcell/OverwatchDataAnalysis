"""
@Author: Komorebil
"""
import json


__all__ = ['log', 'MSG', 'user_input', 'get_info']


def log(*args):
    print(*args)


def message():
    result = {}
    result['help'] = """
        欢迎使用命令行版的ORA，本启动器现在有两种模式，分别是通过以下形式判断：
        1.  单任务版
                判断条件是输入的参数大于1，
                比如 main_cli.exe <video_path> <output_path> <number>
                此时的参数为3，如果想查看详细的说明可以输入 main_cli.exe help1
        2.  多任务版
                判断条件是输入的参数等于1.
                比如 main_cli.exe <json_path>
                其中 <json_path> 是一个txt或者json文件的目录，我们规定了其中的格式
                具体请输入 main_cli.exe help2 查看
    """

    result['help1'] = """
        Example:
            main_cli.exe <video_path> <output_path> <number> version=0 players=player.txt fps=2 start_time=0 end_time=0

        Mandatory arguments:
            <video_path>         Absolute path of video(example: F:/video.mp4)
            <output_path>        Absolute path of output file(example: F:/)
            <number>             A number representing game type. 0: OWL, 1: Non-OWL

        Optional:
            version=0            OWL stage number(0=preseason, 1, 2, 3, 4)
            players=players.txt  A text file saving info of all 12 players with JSON formatting。 help => main_cli.exe --json1
            fps=2                FPS of analyzer (2 by default)
            start_time=0         Starting time in seconds
            end_time=0           Ending time in seconds (If both are 0, then the whole video is analyzed)
    """
    result['need_help'] = """
        Please input with proper amount of arguments.
        如需帮助请输入 main_cli.py help
    """
    result['lack'] = "optional lack of token '='"
    result['json1'] = """
    player JSON format:
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
    result['help2'] = """
    假如我要依次分析两个视频， 那么JSON为：
    [
        {
            "video_path": "F:\\01.mp4",
            "output_path": "F:\\videos",
            "game_type": 0,
        },
        {
            "video_path": "F:\\02.mp4",
            "output_path": "F:\\videos",
            "game_type": 0,
            "version": 4,
        },
    ]
    也就是说格式如右边这样：[video_config, video_config]
    video_config 中的 video_path、output_path、game_type为必填参数。
    可选配置以及说明如下:
        version              OWL stage number(0=preseason, 1, 2, 3, 4)
        players              A text file saving info of all 12 players with JSON formatting。 help => main_cli.exe --json1
        fps                  FPS of analyzer (2 by default)
        start_time           Starting time in seconds
        end_time             Ending time in seconds (If both are 0, then the whole video is analyzed)
    你可以如同第二个 video_config 那样举一反三
    """
    result['key_error'] = 'ora_cmd got an unexpected keyword argument "{}"'
    return result


MSG = message()


def user_input(data):
    """
    Retrieving info from user input in command line
    """
    keys = ['fps', 'players', 'start_time', 'end_time', 'version', 'video_path', 'output_path', 'game_type']
    error_value = set(data) - set(keys)
    if len(error_value) > 0:
        raise ValueError(MSG.get('key_error').format(error_value))
    info = {
        'fps': data.get('fps', 2),
        '_players': data.get('players'),
        'start_time': data.get('start_time', 0),
        'end_time': data.get('end_time', 0),
        'game_version': data.get('version', 0),
        'video_path': data.get('video_path'),
        'output_path': data.get('output_path'),
        'game_type': data.get('game_type')
    }
    print(info)
    return info


def get_info(info):
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
            print(MSG.get('json1'))
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

    if info['game_type'] is None:
        raise KeyError('not found game_type')

    if info['video_path'] is None:
        raise KeyError('not found video_path')

    if info['output_path'] is None:
        raise KeyError('not found output_path')

    try:
        info['game_type'] = int(info['game_type'])
    except ValueError:
        log('Invalid game type!')

    if not (info['game_type'] == 0 or info['game_type'] == 1):
        raise ValueError('Invalid game type!')

    try:
        info['game_version'] = int(info['game_version'])
    except ValueError:
        log('Invalid OWL stage number!')

    if info['game_type'] == 0 and info['game_version'] not in [0, 1, 2, 3, 4]:
        raise ValueError('Invalid OWL stage number!')
    return info
