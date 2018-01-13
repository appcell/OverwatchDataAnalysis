"""
@Author: Xiaochen (leavebody) Li 
"""
from gamedata import GameData
from frame import FrameAnalyzer


def analyze_video(video_loader, gamedata):
    """
    Analyze the killfeed of an video.
    @param video_loader: a video.VideoLoader object
    @return:
    """
    step = int(round(video_loader.fps/2))
    killfeed_list = []
    index = 0
    frame = video_loader.get_frame(index)
    analyzer = FrameAnalyzer(frame, index, gamedata)
    analyzer.set_team_color()  # only need to do this once for one game
    while frame is not None:
        analyzer = FrameAnalyzer(frame, index, gamedata)
        analyzer.analyze()
        gamedata.add_frame(analyzer.frame)
        index += step
        frame = video_loader.get_frame(index)

    ######### to test killfeed output #############
    for kf in gamedata.killfeeds:
        print kf
    ######### end of test             #############




    video_loader.close()
