"""
@Author: Xiaochen (leavebody) Li 
"""
import image
import cv2


class KillFeed:
    """
    A killfeed entry.
    """
    def __init__(self, file_id, time=None, character1=None, character2=None, event=None):
        self.file_id = file_id
        self.time = time
        self.character1 = character1
        self.character2 = character2
        self.event = event

    def __eq__(self, other):
        """
        Check if this killfeed describes the same event as another killfeed.
        @param other: a KillFeed object to compare
        @return: "True" for a same event and "False" for a different event
        """
        if type(other) != type(self):
            return False

        if self.character1 == other.character1 and self.character2 == other.character2 and self.event == other.event:
            return True
        else:
            return False


ANA = "ana"
BASTION = "bastion"
DOOMFIST = "doomfist"
DVA = "dva"
GENJI = "genji"
HANZO = "hanzo"
JUNKRAT = "junkrat"
LUCIO = "lucio"
MCCREE = "mccree"
MEI = "mei"
MERCY = "mercy"
MOIRA = "moira"
ORISA = "orisa"
PHARAH = "pharah"
REAPER = "reaper"
REINHARDT = "reinhardt"
ROADHOG = "roadhog"
SOLDIER76 = "soldier76"
SOMBRA = "sombra"
SYMMETRA = "symmetra"
TORBJON = "torbjon"
TRACER = "tracer"
WIDOWMAKER = "widowmaker"
WINSTON = "winston"
ZARYA = "zarya"
ZENYATTA = "zenyatta"

MEKA = "meka"
RIPTIRE = "riptire"
SHIELD = "shield"
SUPERCHARGER = "supercharger"
TELEPORTER = "teleporter"
TURRET = "turret"

#: A list of all characters in overwatch.
CHARACTER_LIST = [ANA, BASTION, DOOMFIST, DVA, GENJI, HANZO, JUNKRAT,
                  LUCIO, MCCREE, MEI, MERCY, MOIRA, ORISA, PHARAH,
                  REAPER, REINHARDT, ROADHOG, SOLDIER76, SOMBRA,
                  SYMMETRA, TORBJON, TRACER, WIDOWMAKER, WINSTON, ZARYA,
                  ZENYATTA]
#: A list of all non-character objects in the killfeed.
NON_CHARACTER_OBJECT_LIST = [MEKA, RIPTIRE, SHIELD, SUPERCHARGER, TELEPORTER, TURRET]

#: All possible object in the killfeed.
KILLFEED_OBJECT_LIST = CHARACTER_LIST + NON_CHARACTER_OBJECT_LIST


#: The dictionary that maps the name of object to its image in killfeed. This is the 1080p version of the icons.
ICON_KILLFEED_DICT_1080P = {obj: image.read_img("./../../images/icons/" + obj + ".png") for obj in KILLFEED_OBJECT_LIST}
#: The size of the 1080p icons in killfeed.
ICON_KILLFEED_1080P_WIDTH = 49
ICON_KILLFEED_1080P_HEIGHT = 34


def get_resized_icons(height=1080):
    """
    Resize the icons in ICON_KILLFEED_DICT to other resolution. Default is 1080p.
    If this function is not run, ICON_KILLFEED_DICT contains icon in 1080p resolution.
    Only supports 16:9 resolution now.
    Result size for 720p: (33, 23)
    @param height: the height of the frame
    @return: the resized dictionary
    """
    ratio = height*1.0/1080
    print "resized size:", (int(round(ICON_KILLFEED_1080P_WIDTH*ratio)), int(round(ICON_KILLFEED_1080P_HEIGHT*ratio)))

    return {obj: cv2.resize(img,
                            (int(round(ICON_KILLFEED_1080P_WIDTH*ratio)), int(round(ICON_KILLFEED_1080P_HEIGHT*ratio))))
            for (obj, img) in ICON_KILLFEED_DICT_1080P.iteritems()}


#: The dictionary that maps the name of object to its image in killfeed. This is the 720p version of the icons.
ICON_KILLFEED_DICT_720P = get_resized_icons(720)
#: The size of the 720p icons in killfeed.
ICON_KILLFEED_720P_WIDTH = 33
ICON_KILLFEED_720P_HEIGHT = 23


