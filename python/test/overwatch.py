# -*- coding:utf-8 -*-
from utils import image as ImageUtils


# **********************************************************
# ==========================================================
#                       Meta Macros
# ==========================================================
# **********************************************************

GAMETYPE_OWL = 0
GAMETYPE_CUSTOM = 1
ANALYZER_FPS = 2


# **********************************************************
# ==========================================================
#               Chara & Non-chara Objects List
# ==========================================================
# **********************************************************

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

#: All possible objects in killfeed.
KILLFEED_OBJECT_LIST = CHARACTER_LIST + NON_CHARACTER_OBJECT_LIST

#: Max number of killfeeds in a screen in the same time.
KILLFEED_ITEM_MAX_COUNT_IN_SCREEN = 6


# **********************************************************
# ==========================================================
#           Team Theme Color Pixel Position Defs
# ==========================================================
# **********************************************************

TEAM_COLOR_PICK_POS_LEFT_OWL = [0, 0]
TEAM_COLOR_PICK_POS_RIGHT_OWL = [0, 1279]
TEAM_COLOR_PICK_POS_LEFT_CUSTOM = [0, 0]
TEAM_COLOR_PICK_POS_RIGHT_CUSTOM = [0, 1279]


# **********************************************************
# ==========================================================
#              Ultimate Icon Position Defs
# ==========================================================
# **********************************************************

ULT_ICON_X_MIN_LEFT_OWL = 30
ULT_ICON_X_MIN_RIGHT_OWL = 830
ULT_ICON_WIDTH_OWL = 30
ULT_ICON_Y_MIN_OWL = 47
ULT_ICON_HEIGHT_OWL = 26
ULT_ICON_GAP_OWL = 71

ULT_ICON_X_MIN_LEFT_CUSTOM = 34
ULT_ICON_X_MIN_RIGHT_CUSTOM = 835
ULT_ICON_WIDTH_CUSTOM = 30
ULT_ICON_Y_MIN_CUSTOM = 51
ULT_ICON_HEIGHT_CUSTOM = 26
ULT_ICON_GAP_CUSTOM = 71

ULT_ICON_MAX_PROB = {GAMETYPE_OWL: 0.5, GAMETYPE_CUSTOM: 0.5}
ULT_ICON_MAX_BRIGHTNESS = {GAMETYPE_OWL: 230, GAMETYPE_CUSTOM: 230}

def get_team_color_pick_pos():
    return {
        GAMETYPE_OWL: [TEAM_COLOR_PICK_POS_LEFT_OWL, TEAM_COLOR_PICK_POS_RIGHT_OWL],
        GAMETYPE_CUSTOM: [TEAM_COLOR_PICK_POS_LEFT_CUSTOM, TEAM_COLOR_PICK_POS_RIGHT_CUSTOM]
    }

def get_ult_icon_pos(index):
    if index < 6:
        return {
        GAMETYPE_OWL: [ULT_ICON_Y_MIN_OWL, 
            ULT_ICON_HEIGHT_OWL, 
            ULT_ICON_X_MIN_LEFT_OWL + index * ULT_ICON_GAP_OWL, 
            ULT_ICON_WIDTH_OWL
            ],
        GAMETYPE_CUSTOM: [ULT_ICON_Y_MIN_CUSTOM, 
            ULT_ICON_HEIGHT_CUSTOM, 
            ULT_ICON_X_MIN_LEFT_CUSTOM + index * ULT_ICON_GAP_CUSTOM, 
            ULT_ICON_WIDTH_CUSTOM
            ]
        }
    else:
        return {
        GAMETYPE_OWL: [ULT_ICON_Y_MIN_OWL, 
            ULT_ICON_HEIGHT_OWL, 
            ULT_ICON_X_MIN_RIGHT_OWL + (index - 6) * ULT_ICON_GAP_OWL, 
            ULT_ICON_WIDTH_OWL
            ],
        GAMETYPE_CUSTOM: [ULT_ICON_Y_MIN_CUSTOM, 
            ULT_ICON_HEIGHT_CUSTOM, 
            ULT_ICON_X_MIN_LEFT_CUSTOM + index * ULT_ICON_GAP_CUSTOM, 
            ULT_ICON_WIDTH_CUSTOM
            ]
        }

def get_ult_icon_ref(index):
    if index < 6:
        return {
            GAMETYPE_OWL: ImageUtils.read("../../images/awayUlt.png"),
            GAMETYPE_CUSTOM: ImageUtils.read("../../images/awayUlt.png")
        }
    else:
        return {
            GAMETYPE_OWL: ImageUtils.read("../../images/homeUlt.png"),
            GAMETYPE_CUSTOM: ImageUtils.read("../../images/homeUlt.png")
        }



# **********************************************************
# ==========================================================
#               Topbar Avatar Position Defs
# ==========================================================
# **********************************************************

# Dimensions of referece avatar images
AVATAR_WIDTH_REF = 38
AVATAR_HEIGHT_REF = 30

# Dimensions & positions of topbar avatars in OWL (observed)
AVATAR_X_MIN_LEFT_OWL = 62  # x of starting point from left side
AVATAR_X_MIN_RIGHT_OWL = 857  # x of starting point from right side
AVATAR_WIDTH_OWL = 38  # width of avatar
AVATAR_Y_MIN_OWL = 48  # y of starting point
AVATAR_HEIGHT_OWL = 30  # height of avatar
AVATAR_GAP_OWL = 71  # x-gap between 2 avatars

# Dimensions & positions of topbar avatars in OWL (not observed)
AVATAR_X_MIN_LEFT_SMALL_OWL = 62
AVATAR_X_MIN_RIGHT_SMALL_OWL = 857
AVATAR_WIDTH_SMALL_OWL = 34
AVATAR_Y_MIN_SMALL_OWL = 52
AVATAR_HEIGHT_SMALL_OWL = 23
AVATAR_GAP_SMALL_OWL = 71

# Dimensions & positions of topbar avatars in custom games (observed)
AVATAR_X_MIN_LEFT_CUSTOM = 34
AVATAR_X_MIN_RIGHT_CUSTOM = 835
AVATAR_WIDTH_CUSTOM = 30
AVATAR_Y_MIN_CUSTOM = 51
AVATAR_HEIGHT_CUSTOM = 26
AVATAR_GAP_CUSTOM = 71

# Dimensions & positions of topbar avatars in custom games (not observed)
AVATAR_X_MIN_LEFT_SMALL_CUSTOM = 62
AVATAR_X_MIN_RIGHT_SMALL_CUSTOM = 857
AVATAR_WIDTH_SMALL_CUSTOM = 34
AVATAR_Y_MIN_SMALL_CUSTOM = 52
AVATAR_HEIGHT_SMALL_CUSTOM = 23
AVATAR_GAP_SMALL_CUSTOM = 71


def get_avatars_ref():
    """
    Get a dict of all reference avatar images
    @Author: Appcell
    @return: a dict of all reference avatar images
    """
    return {chara: ImageUtils.resize(ImageUtils.read_with_transparency("../../images/charas/" + chara + ".png"), AVATAR_WIDTH_REF, AVATAR_HEIGHT_REF) \
     for chara in CHARACTER_LIST}

def get_avatar_pos_small(index):
    """
    Get position of an avatar in one frame, given player index.
    The player is currently not observed by cam.
    @Author: Appcell
    @param index: index of player
    @return: pos array of this avatar
    """
    if index < 6:
        return {
        GAMETYPE_OWL:  [AVATAR_Y_MIN_SMALL_OWL, 
            AVATAR_HEIGHT_SMALL_OWL, 
            AVATAR_X_MIN_LEFT_SMALL_OWL + index * AVATAR_GAP_SMALL_OWL, 
            AVATAR_WIDTH_SMALL_OWL
            ],
        GAMETYPE_CUSTOM:  [AVATAR_Y_MIN_SMALL_CUSTOM, 
            AVATAR_HEIGHT_SMALL_CUSTOM, 
            AVATAR_X_MIN_LEFT_SMALL_CUSTOM + index * AVATAR_GAP_SMALL_CUSTOM, 
            AVATAR_WIDTH_SMALL_CUSTOM
            ]
        }
    else:
        return {
        GAMETYPE_OWL: [AVATAR_Y_MIN_SMALL_OWL, 
            AVATAR_HEIGHT_SMALL_OWL, 
            AVATAR_X_MIN_RIGHT_SMALL_OWL + (index - 6) * AVATAR_GAP_SMALL_OWL, 
            AVATAR_WIDTH_SMALL_OWL
            ],
        GAMETYPE_CUSTOM: [AVATAR_Y_MIN_SMALL_CUSTOM, 
            AVATAR_HEIGHT_SMALL_CUSTOM, 
            AVATAR_X_MIN_LEFT_SMALL_CUSTOM + index * AVATAR_GAP_SMALL_CUSTOM, 
            AVATAR_WIDTH_SMALL_CUSTOM
            ]
        }

def get_avatar_pos(index):
    """
    Get position of an avatar in one frame, given player index.
    The player is currently observed by cam.
    @Author: Appcell
    @param index: index of player
    @return: pos array of this avatar
    """
    if index < 6:
        return {
        GAMETYPE_OWL:  [AVATAR_Y_MIN_OWL, 
            AVATAR_HEIGHT_OWL, 
            AVATAR_X_MIN_LEFT_OWL + index * AVATAR_GAP_OWL, 
            AVATAR_WIDTH_OWL
            ],
        GAMETYPE_CUSTOM:  [AVATAR_Y_MIN_CUSTOM, 
            AVATAR_HEIGHT_CUSTOM, 
            AVATAR_X_MIN_LEFT_CUSTOM + index * AVATAR_GAP_CUSTOM, 
            AVATAR_WIDTH_CUSTOM
            ]
        }
    else:
        return {
        GAMETYPE_OWL: [AVATAR_Y_MIN_OWL, 
            AVATAR_HEIGHT_OWL, 
            AVATAR_X_MIN_RIGHT_OWL + (index - 6) * AVATAR_GAP_OWL, 
            AVATAR_WIDTH_OWL
            ],
        GAMETYPE_CUSTOM: [AVATAR_Y_MIN_CUSTOM, 
            AVATAR_HEIGHT_CUSTOM, 
            AVATAR_X_MIN_LEFT_CUSTOM + index * AVATAR_GAP_CUSTOM, 
            AVATAR_WIDTH_CUSTOM
            ]
        }

# **********************************************************
# ==========================================================
#                     Ability Code
# ==========================================================
# **********************************************************
ABILITY_SHIFT = 1
ABILITY_E = 2
ABILITY_Q_1 = 3
ABILITY_Q_2 = 4