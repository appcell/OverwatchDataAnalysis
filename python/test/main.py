# -*- coding:utf-8 -*-
from game import Game
import overwatch as OW
import time


def main():
    gui_info = {"name_team_left": "SHD", 
           "name_team_right": "BU", 
           "name_players_team_left": ["1", "2", "3", "4", "5", "6"],
           "name_players_team_right": ["7", "8", "9", "10", "11", "12"],
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
