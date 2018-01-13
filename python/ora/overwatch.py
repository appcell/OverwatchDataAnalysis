# -*- coding:utf-8 -*-
"""
@Author: Xiaochen (leavebody) Li 
"""
import util
import cv2
from util import singleton


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

class Frame:
    """
    Data retrieved from a frame.
    """
    def __init__(self):
        self.is_valid = False
        self.charas = None
        self.killfeeds = None


class Killfeed:
    """
    A killfeed entry.
    """
    def __init__(self, file_id, time=0, character1="", character2="", team1="", team2="", event=""):
        self.file_id = file_id
        self.time = time
        self.team1 = team1
        self.team2 = team2
        self.character1 = character1
        self.character2 = character2
        self.event = event
        #: the x coordinate of the icon in the killfeed item image
        self.character1_x = None  # todo do we really need these????
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
        result = self.event + "\t"
        if self.event == SUICIDE:
            result += self.team2 + "\t" + self.character2 + "\t"
        else:
            result += self.team1 + "\t" + self.character1 + "\t" + self.team2 + "\t" + self.character2 + "\t"
        result += "time: "+str(self.time)
        return result


class Chara:
    """
    Info of ONE player in the player zone in ONE frame
    """
    def __init__(self, player=None):
        self.time = None
        #: the player name
        self.player = player
        #: the character that this player is playing
        self.character = None
        #: whether this player has ultimate ability now
        self.ultimate_status = None

        # todo: future work
        self.is_observed = None  # is the daddy camera watching this guy?
        self.health = None
        self.ultimate_charge = None
        self.is_onfire = None


class UltimateSkill:
    def __init__(self, time, ultimate_list):
        self.time = time
        self.ultimate = self.new_ultimate(ultimate_list)

    @staticmethod
    def new_ultimate(ultimate):
        d = {
            'True': [],
            'False': [],
        }
        for i, s in enumerate(ultimate):
            if s is True:
                d['True'].append(i + 1)
            else:
                d['False'].append(i + 1)
        return d


# Killfeed events in overwatch.
ELIMINATION = "elimination"
SUICIDE = "suicide"
RESURRECTION = "resurrection"


ULTIMATE_SKILL_DICT = {
    'LEFT': 'visitingUlt',
    'RIGHT': 'homeUlt',
}


@singleton
class UltimateSkillIcons:
    def __init__(self, frame_height=None):
        self.ICONS = self._read_720p_icons()

    @staticmethod
    def _read_720p_icons():
        return {key: util.read_img("./../images/" + value + ".png")
                for (key, value) in ULTIMATE_SKILL_DICT.iteritems()}

    def _get_resized_icons(self):
        pass


@singleton
class KillfeedIcons:
    def __init__(self, frame_height=1080):
        """
        Only supports 16:9 resolution now.
        @param frame_height: the height of the whole frame.
        """
        self._width_1080p = 49
        self._height_1080p = 34
        self._icon_dic_1080p = self._read_1080p_icons()
        ratio = frame_height*1.0/1080
        self.ICON_CHARACTER_WIDTH = int(round(self._width_1080p * ratio))
        self.ICON_CHARACTER_HEIGHT = int(round(self._height_1080p * ratio))

        self.ICONS_CHARACTER = self._get_resized_icons()

    def _read_1080p_icons(self):
        return {obj: util.read_img("../../images/icons/" + obj + ".png") for obj in KILLFEED_OBJECT_LIST}

    def _get_resized_icons(self):
        """
        Resize the icons in ICON_KILLFEED_DICT to other resolution.
        If this function is not run, ICON_KILLFEED_DICT contains icon in 1080p resolution.
        Only supports 16:9 resolution now.
        @return: the resized dictionary
        """
        return {obj: cv2.resize(img, (self.ICON_CHARACTER_WIDTH, self.ICON_CHARACTER_HEIGHT))
                for (obj, img) in self._icon_dic_1080p.iteritems()}


@singleton
class CharacterIcons:
    def __init__(self):
        self.icons_and_alpha = self._read_720p_icons_and_alpha()
        # cv2.resize 处理不了无穷小数 (如1280/1920) 因此这里的 width height 先写死
        self._width = 38
        self._height = 30
        self.icon_and_alpha_to_resize = self._get_resized_icons_and_alpha()

    @staticmethod
    def _read_720p_icons_and_alpha():
        """
        获取图片以及图片的alpha
        :return: {character: [img, alpha], ...}
        """
        return {obj: util.read_unchanged_img("../../images/charas/" + obj + ".png") for obj in CHARACTER_LIST}

    def _get_resized_icons_and_alpha(self):
        # 缩放 img 以及 alpha
        resize = lambda img_alpha: \
            (cv2.resize(img_alpha[0], (self._width, self._height)),
             cv2.resize(img_alpha[1], (self._width, self._height)))
        return {obj: resize(img_alpha) for (obj, img_alpha) in self.icons_and_alpha.iteritems()}


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

    PLAYER_ZONE_TEAM1_LEFT_X = None
    PLAYER_ZONE_TEAM2_LEFT_X = None
    PLAYER_ZONE_WIDTH = None
    PLAYER_ZONE_HORIZONTAL_STEP = None
    PLAYER_ZONE_TOP_Y = None
    PLAYER_ZONE_HEIGHT = None

    # todo need to delete/switch these constants after this refactor
    ULTIMATE_TOP_X_LEFT = None
    ULTIMATE_TOP_X_RIGHT = None
    ULTIMATE_TOP_Y = None
    ULTIMATE_WIDTH = None
    ULTIMATE_HEIGHT = None
    ULTIMATE_MAX_WIDTH = None

    CHARA_TOP_X = None
    CHARA_TOP_Y = None
    CHARA_HEIGHT = None
    CHARA_WIDTH = None

    def __init__(self, frame_height=720):
        #: The height of a killfeed item.
        self.KILLFEED_ITEM_HEIGHT = 35
        self.ULTIMATE_ITEM_X = 70

    def check_abstract_fields(self):
        abstract_fields = [
            self.KILLFEED_TOP_Y,
            self.KILLFEED_RIGHT_X,
            self.KILLFEED_MAX_WIDTH,
            self.KILLFEED_CHARACTER2_MAX_WIDTH,

            self.PLAYER_ZONE_TEAM1_LEFT_X,
            self.PLAYER_ZONE_TEAM2_LEFT_X,
            self.PLAYER_ZONE_WIDTH,
            self.PLAYER_ZONE_HORIZONTAL_STEP,
            self.PLAYER_ZONE_TOP_Y,
            self.PLAYER_ZONE_HEIGHT,

            self.ULTIMATE_TOP_X_LEFT,
            self.ULTIMATE_TOP_X_RIGHT,
            self.ULTIMATE_TOP_Y,
            self.ULTIMATE_WIDTH,
            self.ULTIMATE_HEIGHT,
            self.ULTIMATE_MAX_WIDTH,

            self.CHARA_TOP_X,
            self.CHARA_TOP_Y,
            self.CHARA_HEIGHT,
            self.CHARA_WIDTH,
        ]
        if None in abstract_fields:
            raise NotImplementedError('Subclasses must define all abstract attributes of killfeeds')


@singleton
class OWLFrameStructure(AbstractGameFrameStructure):
    def __init__(self, frame_height=720):
        AbstractGameFrameStructure.__init__(self, frame_height)
        self.KILLFEED_TOP_Y = 116
        self.KILLFEED_RIGHT_X = 1270
        self.KILLFEED_MAX_WIDTH = 350  # TODO Not very sure about this number.
        self.KILLFEED_CHARACTER2_MAX_WIDTH = 140

        self.PLAYER_ZONE_TEAM1_LEFT_X = 20
        self.PLAYER_ZONE_TEAM2_LEFT_X = 827
        self.PLAYER_ZONE_WIDTH = 81
        self.PLAYER_ZONE_HORIZONTAL_STEP = 71.4
        self.PLAYER_ZONE_TOP_Y = 47
        self.PLAYER_ZONE_HEIGHT = 51

        self.ULTIMATE_TOP_X_LEFT = 34
        self.ULTIMATE_TOP_X_RIGHT = 835
        self.ULTIMATE_TOP_Y = 11
        self.ULTIMATE_HEIGHT = 26
        self.ULTIMATE_WIDTH = 30
        self.ULTIMATE_MAX_WIDTH = self.ULTIMATE_ITEM_X * 6

        self.CHARA_TOP_X = 42
        self.CHARA_TOP_Y = 0
        self.CHARA_HEIGHT = 30
        self.CHARA_WIDTH = 38
