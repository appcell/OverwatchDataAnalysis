# -*- coding:utf-8 -*-
from excel import Excel
from gamedata import GameData
from util import VideoLoader
from ora import analyze_video
import time


def main():
    path = '../../videos/1.mp4'
    game = GameData()
    game.set_team_name("SHD", "BU")
    video = VideoLoader(path)
    analyze_video(video, game)
    video.close()


if __name__ == '__main__':
    t = time.time()
    main()
    print "time:", time.time()-t
