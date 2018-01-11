# -*- coding:utf-8 -*-
from excel import Excel
from src.overwatch import OverwatchGame
from src.video import VideoLoader
from src import analyze_video
import time


def main():
    path = '../videos/2.mp4'
    game = OverwatchGame(team1name="SHD", team2name="BU")
    video = VideoLoader(path)
    analyze_video(video, game, excel=Excel())
    video.close()


if __name__ == '__main__':
    t = time.time()
    main()
    print "time:", time.time()-t
