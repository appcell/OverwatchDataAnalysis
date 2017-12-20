"""
@Author: Xiaochen (leavebody) Li 
"""
from video import VideoLoader


def analyze_video(video_loader):
    """
    analyze the killfeed of an video
    :param video_loader: a video.VideoLoader object
    :return:
    """
    step = video_loader.fps/2.0
    killfeed_list = []
    index = 0
    frame = video.get_frame(index)
    while frame:
        pass



if __name__ == '__main__':
    path = '../../videos/2.mp4'
    video = VideoLoader(path)
    analyze_video(video)
    video.close()
