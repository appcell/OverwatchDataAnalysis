# -*- coding:utf-8 -*-
from excel import Excel
from src.overwatch import OverwatchGame
from src.video import VideoLoader
from src import analyze_video
import time


def write_excel(game_data):
    e = Excel()
    e.sheet1.append(game_data)
    e.save(filename='test')


def main():
    path = '../videos/2.mp4'
    game = OverwatchGame(team1name="SHD", team2name="BU")
    video = VideoLoader(path)
    game_data = analyze_video(video, game)
    video.close()
    write_excel(game_data)


if __name__ == '__main__':
    t = time.time()
    main()
    print "time:", time.time()-t
