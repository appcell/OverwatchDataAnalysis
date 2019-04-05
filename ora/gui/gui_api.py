
from ora import game
from ora import pool
from ora import overwatch as OW


def get_video_info(video_path):
    """
    Get video info show in video list.
    :param video_path:
    :return: teamname1, teamname2, length

    """
    pass


def publish_analysis():
    """Run when checked 'Publish your analysis'"""
    pass


def analyze_button_clicked(is_owl, info):
    """
    Run when click 'ANALYZE' button
    You should add args as need.
    """
    is_owl = OW.GAMETYPE_OWL if is_owl else OW.GAMETYPE_CUSTOM
    game_instance = game.Game(is_owl)
    game_instance.set_game_info(info)
    pool.initPool()
    try:
        game_instance.analyze(info['start_time'], info['end_time'], is_test=False)
    except Exception as err:
        print(err)
    else:
        game_instance.output()

    pool.PROCESS_POOL.close()
    pool.PROCESS_POOL.join()


def save_button_clicked(*args):
    """
    Run when click 'SAVE' button
    You should add args as need.
    """
    pass


def auto_check_update_checked():
    """Run when checked 'Automatically check for update'"""
    pass




