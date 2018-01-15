# -*- coding:utf-8 -*-
from game import Game
import overwatch as OW
import time


def main():
    gui_info = {"name_team_left": "SHD", 
           "name_team_right": "BU", 
           "name_players_team_left": ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6"],
           "name_players_team_right": ["Player7", "Player8", "Player9", "Player10", "Player11", "Player12"],
           "video_path": "../../videos/1.mp4",
           "output_path": ""
           }

    game = Game(OW.GAMETYPE_OWL, OW.ANALYZER_FPS)
    game.set_game_info(gui_info)
    game.analyze()


if __name__ == '__main__':
    t = time.time()
    main()
    print "time:", time.time()-t
