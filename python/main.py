import time
from game import Game
# from gui import Gui
import overwatch as OW



def analyze():
    """Pre-analysis process

    Write GUI input into Game instance, then start analysis in Game.

    Author:
        Appcell

    Args:
        None

    Returns:
        None 
    """
    gui_info = {"name_team_left": "SHD",
                "name_team_right": "BU",
                "name_players_team_left": [
                    "Player1", 
                    "Player2", 
                    "Player3", 
                    "Player4", 
                    "Player5", 
                    "Player6"],
                "name_players_team_right": [
                    "Player7", 
                    "Player8", 
                    "Player9", 
                    "Player10", 
                    "Player11", 
                    "Player12"],
                "video_path": "../videos/1.mp4",
                "output_path": ""
               }

    game = Game(OW.GAMETYPE_OWL, OW.ANALYZER_FPS)
    game.set_game_info(gui_info)
    game.analyze()
    game.output_to_excel()


if __name__ == '__main__':
    # GUI = Gui()
    # GUI.show()
    T = time.time()
    analyze()
    print "time:", time.time() - T
