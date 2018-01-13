"""
@Author: Xiaochen (leavebody) Li 
"""

import cv2
import overwatch
import util
import frame
import gamedata

path = '../../videos/2.mp4'
game = gamedata.GameData()
game.set_team_name("t1", "t2")
frame_number = 500

# path = '../../videos/SHD_VS_SD_GAME_3_round_1.mp4'
# frame_number = 7745


#path = '../../videos/SDvsNYXL_Preseason.mp4'
# frame_number = 880

v = util.VideoLoader(path)
print "fps:", v.fps
frame_image = v.get_frame(frame_number)

cv2.imshow("df", frame_image)

analyzer = frame.FrameAnalyzer(frame_image, 0, game)
analyzer.set_team_color()
kf = analyzer.get_killfeed()
for k in kf:
    print k

print "done"
cv2.waitKey(0)

# def compare_images(imageA, imageB, title):
# 	# compute the mean squared error and structural similarity
# 	# index for the images
#     s = ssim(imageA, imageB, multichannel=True)
#     return s
#
# def compare_matchtemp(imageA, imageB, title=''):
#     return cv2.matchTemplate(imageA, imageB, cv2.TM_CCOEFF_NORMED)[0][0]


# path = '../../videos/SDvsNYXL_Preseason.mp4'
# frame_number = 880
#
# v = video.VideoLoader(path)
# print "fps:", v.fps
# frame = v.get_frame(frame_number)
# analyzer = __init__.FrameAnalyzer(frame, 0)
# killfeed_image = analyzer.get_killfeed_row_image(0)
# cv2.imshow("test frame", frame)
# cv2.imshow("killfeed", killfeed_image)
#
# icons = overwatch.KillfeedIcons(720)
# t = time.time()
# for i in range(100):
#     for chara in icons.ICONS_CHARACTER:
#         img = icons.ICONS_CHARACTER[chara]
#         cv2.matchTemplate(killfeed_image, img, cv2.TM_CCOEFF_NORMED)
# print "time match all:", time.time()-t
#
# for fcount in range(12):
#     t = time.time()
#     for j in range(100):
#         for i in range(fcount):
#             cropped = image.crop_by_limit(killfeed_image, 0, icons.ICON_CHARACTER_HEIGHT, i*10, icons.ICON_CHARACTER_WIDTH)
#             for chara in icons.ICONS_CHARACTER:
#                 img = icons.ICONS_CHARACTER[chara]
#                 cv2.matchTemplate(img, cropped, cv2.TM_CCOEFF)
#     print "time match: "+str(fcount), time.time()-t
#
# cv2.waitKey(0)


