"""
@Author: Xiaochen (leavebody) Li 
"""
import image
import cv2
from abc import ABCMeta, abstractmethod, abstractproperty


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
        #: the x coordinate of the icon in the killfeed item image
        self.character1_x = None
        self.character2_x = None

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

    def __str__(self):
        # todo make this more user-friendly
        if self.character1 is None:
            return "time:" + str(self.time) + " character2:" + self.character2
        return "time:" + str(self.time) + " character1:" + self.character1 + " character2:" + self.character2


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

#: The max number of killfeeds in a screen in the same time.
KILLFEED_ITEM_MAX_COUNT_IN_SCREEN = 6

ULTIMATE_SKILL_DICT = {
    'LEFT': 'visitingUlt',
    'RIGHT': 'homeUlt',
}


class UltimateSkillIcons:
    def __init__(self, frame_height=None):
        self.ICONS = self._read_1080p_icons()

    @staticmethod
    def _read_1080p_icons():
        return {key: image.read_img("./../../images/" + value + ".png")
                for (key, value) in ULTIMATE_SKILL_DICT.iteritems()}

    def _get_resized_icons(self):
        pass


class KillfeedIcons:
    def __init__(self, frame_height=1080):
        """
        Only supports 16:9 resolution now.
        @param frame_height: the height of the whole frame.
        """
        self._width_1080p = 49
        self._height_1080p = 34
        self._icon_dic_1080p = KillfeedIcons._read_1080p_icons()

        ratio = frame_height*1.0/1080
        self.ICON_CHARACTER_WIDTH = int(round(self._width_1080p * ratio))
        self.ICON_CHARACTER_HEIGHT = int(round(self._height_1080p * ratio))

        self.ICONS_CHARACTER = self._get_resized_icons()

    @staticmethod
    def _read_1080p_icons():
        return {obj: image.read_img("./../../images/icons/" + obj + ".png") for obj in KILLFEED_OBJECT_LIST}

    def _get_resized_icons(self):
        """
        Resize the icons in ICON_KILLFEED_DICT to other resolution.
        If this function is not run, ICON_KILLFEED_DICT contains icon in 1080p resolution.
        Only supports 16:9 resolution now.
        @return: the resized dictionary
        """
        return {obj: cv2.resize(img, (self.ICON_CHARACTER_WIDTH, self.ICON_CHARACTER_HEIGHT))
                for (obj, img) in self._icon_dic_1080p.iteritems()}


class AbstractGameFrameStructureMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.check_abstract_fields()
        return obj


class AbstractGameFrameStructure(object):
    __metaclass__ = AbstractGameFrameStructureMeta
    #: The y value of the top most pixel of the icon in the first killfeed.
    KILLFEED_TOP_Y = None
    #: The x value of the right most pixel of killfeeds.
    KILLFEED_RIGHT_X = None
    #: The max width of an killfeed item.
    KILLFEED_MAX_WIDTH = None
    #: The max width of the second character's icon and name in the killfeed.
    KILLFEED_CHARACTER2_MAX_WIDTH = None

    PLAYERS_STATUS_ZONE_X = None
    PLAYERS_STATUS_ZONE_Y = None
    PLAYERS_STATUS_ZONE_WIDTH = None
    PLAYERS_STATUS_ZONE_HEIGHT = None

    ULTIMATE_TOP_X_LEFT = None
    ULTIMATE_TOP_X_RIGHT = None
    ULTIMATE_TOP_Y = None
    ULTIMATE_WIDTH = None
    ULTIMATE_HEIGHT = None
    ULTIMATE_MAX_WIDTH = None

    def __init__(self, frame_height=720):
        #: The height of a killfeed item.
        self.KILLFEED_ITEM_HEIGHT = 35
        self.ULTIMATE_ITEM_X = 70

    def check_abstract_fields(self):
        if (
            self.KILLFEED_TOP_Y is None or
            self.KILLFEED_RIGHT_X is None or
            self.KILLFEED_MAX_WIDTH is None or
            self.KILLFEED_CHARACTER2_MAX_WIDTH is None
            or
            self.PLAYERS_STATUS_ZONE_X is None or
            self.PLAYERS_STATUS_ZONE_Y is None or
            self.PLAYERS_STATUS_ZONE_WIDTH is None or
            self.PLAYERS_STATUS_ZONE_HEIGHT is None or

            self.ULTIMATE_TOP_X_LEFT is None or
            self.ULTIMATE_TOP_X_RIGHT is None or
            self.ULTIMATE_TOP_Y is None or
            self.ULTIMATE_WIDTH is None or
            self.ULTIMATE_HEIGHT is None or
            self.ULTIMATE_MAX_WIDTH is None
        ):
            raise NotImplementedError('Subclasses must define all abstract attributes of killfeeds')


class OWLFrameStructure(AbstractGameFrameStructure):
    def __init__(self, frame_height=720):
        AbstractGameFrameStructure.__init__(self, frame_height)
        self.KILLFEED_TOP_Y = 116
        self.KILLFEED_RIGHT_X = 1270
        self.KILLFEED_MAX_WIDTH = 350  # TODO Not very sure at this number.
        self.KILLFEED_CHARACTER2_MAX_WIDTH = 140

        self.PLAYERS_STATUS_ZONE_X = 0
        self.PLAYERS_STATUS_ZONE_Y = 40
        self.PLAYERS_STATUS_ZONE_HEIGHT = 60
        self.PLAYERS_STATUS_ZONE_WIDTH = 1280

        self.ULTIMATE_TOP_X_LEFT = 37
        self.ULTIMATE_TOP_X_RIGHT = 833
        self.ULTIMATE_TOP_Y = 6
        self.ULTIMATE_HEIGHT = 26
        self.ULTIMATE_WIDTH = 26
        self.ULTIMATE_MAX_WIDTH = self.ULTIMATE_ITEM_X * 6


class OverwatchGame:
    """
    Holds the basic information of a game.
    """
    def __init__(self, team1name, team2name):
        #: The name of both team.
        self.name_team1 = team1name
        self.name_team2 = team2name
        #: The theme color of both team. In format [b,g,r] and each color is in [0,256).
        self.color_team1 = None
        self.color_team2 = None
