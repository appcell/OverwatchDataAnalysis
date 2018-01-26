from utils import image as ImageUtils
import os
from numpy import tan, arctan

# **********************************************************
# ==========================================================
#                       Meta Macros
# ==========================================================
# **********************************************************
GAMETYPE_OWL = 0
GAMETYPE_CUSTOM = 1
ANALYZER_FPS = 2
DEFAULT_SCREEN_WIDTH = 1280
DEFAULT_SCREEN_HEIGHT = 720
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

ASSIST_CHARACTER_LIST = [ANA, GENJI, JUNKRAT, MCCREE, MEI,
                         MERCY, ORISA, REINHARDT, ROADHOG, SOMBRA, ZARYA, ZENYATTA]

#: A list of all non-character objects in the killfeed.
NON_CHARACTER_OBJECT_LIST = [MEKA, RIPTIRE,
                             SHIELD, SUPERCHARGER, TELEPORTER, TURRET]

#: All possible objects in killfeed.
KILLFEED_OBJECT_LIST = CHARACTER_LIST + NON_CHARACTER_OBJECT_LIST

#: Max number of killfeeds in a screen in the same time.
KILLFEED_ITEM_MAX_COUNT_IN_SCREEN = 6


def get_chara_name(name):
    """Get chara name given object/chara name.

    Author:
        Appcell

    Args:
        name: object/chara name

    Returns:
        A string with corresponding chara name
    """
    if name == MEKA:
        return DVA
    elif name == RIPTIRE:
        return JUNKRAT
    elif name == SHIELD:
        return SYMMETRA
    elif name == SUPERCHARGER:
        return ORISA
    elif name == TELEPORTER:
        return SYMMETRA
    elif name == TURRET:
        return TORBJON
    return name


# **********************************************************
# ==========================================================
#           Team Theme Color Pixel Position Defs
# ==========================================================
# **********************************************************
TEAM_COLOR_PICK_POS_LEFT_OWL = [53, 40]
TEAM_COLOR_PICK_POS_RIGHT_OWL = [54, 1183]
TEAM_COLOR_PICK_POS_LEFT_CUSTOM = [0, 0]
TEAM_COLOR_PICK_POS_RIGHT_CUSTOM = [0, 1279]
# **********************************************************
# ==========================================================
#              Ultimate Icon Position Defs
# ==========================================================
# **********************************************************
ULT_ICON_X_MIN_LEFT_OWL = 31
ULT_ICON_X_MIN_RIGHT_OWL = 825
ULT_ICON_WIDTH_OWL = 33
ULT_ICON_Y_MIN_OWL = 47
ULT_ICON_HEIGHT_OWL = 26
ULT_ICON_GAP_OWL = 70

ULT_ICON_X_MIN_LEFT_CUSTOM = 34
ULT_ICON_X_MIN_RIGHT_CUSTOM = 835
ULT_ICON_WIDTH_CUSTOM = 30
ULT_ICON_Y_MIN_CUSTOM = 51
ULT_ICON_HEIGHT_CUSTOM = 26
ULT_ICON_GAP_CUSTOM = 71

ULT_ICON_MAX_PROB = {GAMETYPE_OWL: 0.8, GAMETYPE_CUSTOM: 0.8}
ULT_ICON_MAX_BRIGHTNESS = {GAMETYPE_OWL: 230, GAMETYPE_CUSTOM: 220}


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
                           ULT_ICON_WIDTH_OWL],
            GAMETYPE_CUSTOM: [ULT_ICON_Y_MIN_CUSTOM,
                              ULT_ICON_HEIGHT_CUSTOM,
                              ULT_ICON_X_MIN_LEFT_CUSTOM + index * ULT_ICON_GAP_CUSTOM,
                              ULT_ICON_WIDTH_CUSTOM]
        }
    return {
        GAMETYPE_OWL: [ULT_ICON_Y_MIN_OWL,
                       ULT_ICON_HEIGHT_OWL,
                       ULT_ICON_X_MIN_RIGHT_OWL +
                       (index - 6) * ULT_ICON_GAP_OWL,
                       ULT_ICON_WIDTH_OWL],
        GAMETYPE_CUSTOM: [ULT_ICON_Y_MIN_CUSTOM,
                          ULT_ICON_HEIGHT_CUSTOM,
                          ULT_ICON_X_MIN_LEFT_CUSTOM + index * ULT_ICON_GAP_CUSTOM,
                          ULT_ICON_WIDTH_CUSTOM]
    }


def get_ult_icon_ref(index):
    if index < 6:
        return {
            GAMETYPE_OWL: ImageUtils.read("./images/awayUlt.png"),
            GAMETYPE_CUSTOM: ImageUtils.read("./images/awayUlt.png")
        }
    return {
        GAMETYPE_OWL: ImageUtils.read("./images/homeUlt.png"),
        GAMETYPE_CUSTOM: ImageUtils.read("./images/homeUlt.png")
    }


# **********************************************************
# ==========================================================
#              Ultimate Charge Position Defs
# ==========================================================
# **********************************************************
ULT_TF_SHEAR_OWL = 0.26396
ULT_TF_OBSERVED_RIGHT_SHEAR_OWL = 0.435
ULT_ADJUST_LOG_INDEX = 4.0
#  Region to determine the color of ultimate charge number, pre-shear
ULT_CHARGE_COLOR_PRE_X_MIN_LEFT_OWL = 20
ULT_CHARGE_COLOR_PRE_X_MIN_RIGHT_OWL = 1178
ULT_CHARGE_COLOR_PRE_WIDTH_OWL = 65
ULT_CHARGE_COLOR_PRE_Y_MIN_OWL = 50
ULT_CHARGE_COLOR_PRE_HEIGHT_OWL = 50
#  Region to determine the color of ultimate charge number, post-shear
ULT_CHARGE_COLOR_X_MIN_LEFT_OWL = 16
ULT_CHARGE_COLOR_X_MIN_RIGHT_OWL = 0
ULT_CHARGE_COLOR_WIDTH_OWL = 31
ULT_CHARGE_COLOR_Y_MIN_OWL = 0
ULT_CHARGE_COLOR_HEIGHT_OWL = 24

#  Region to read ultimate charge number, pre-shear
ULT_CHARGE_PRE_X_MIN_LEFT_OWL = 20
ULT_CHARGE_PRE_X_MIN_RIGHT_OWL = 825
ULT_CHARGE_PRE_WIDTH_OWL = 65
ULT_CHARGE_PRE_Y_MIN_OWL = 50
ULT_CHARGE_PRE_HEIGHT_OWL = 50
#  Very ugly! Maybe switch to 1080P?
ULT_CHARGE_PRE_GAP_LEFT_OWL = [70, 70, 70, 71, 71]
ULT_CHARGE_PRE_GAP_RIGHT_OWL = [70, 71, 71, 71, 71]

ULT_CHARGE_PRE_OBSERVED_X_MIN_LEFT_OWL = 20
ULT_CHARGE_PRE_OBSERVED_X_MIN_RIGHT_OWL = 820
ULT_CHARGE_PRE_OBSERVED_WIDTH_OWL = 76
ULT_CHARGE_PRE_OBSERVED_HEIGHT_OWL = 57
ULT_CHARGE_PRE_RESIZE_WIDTH_RATIO_OWL = 65.0/76.0
ULT_CHARGE_PRE_RESIZE_HEIGHT_RATIO_OWL = 50.0/57.0

#  Region to read ultimate charge number, post-shear, 1st and 2nd number
ULT_CHARGE_0_X_MIN_LEFT_OWL = 22
ULT_CHARGE_0_X_MIN_RIGHT_OWL = 11
ULT_CHARGE_1_X_MIN_LEFT_OWL = 30
ULT_CHARGE_1_X_MIN_RIGHT_OWL = 19
ULT_CHARGE_WIDTH_OWL = 6
ULT_CHARGE_Y_MIN_OWL = 5
ULT_CHARGE_HEIGHT_OWL = 16

ULT_CHARGE_OBSERVED_0_X_MIN_LEFT_OWL = 14
ULT_CHARGE_OBSERVED_0_X_MIN_RIGHT_OWL = 9
ULT_CHARGE_OBSERVED_1_X_MIN_LEFT_OWL = 22
ULT_CHARGE_OBSERVED_1_X_MIN_RIGHT_OWL = 16
ULT_CHARGE_OBSERVED_X_MIN_RIGHT_BIAS_OWL = []
ULT_CHARGE_OBSERVED_Y_MIN_OWL = 2

#  TODO: Custom game


def get_tf_observed_right_shear():
    return {
        GAMETYPE_OWL: ULT_TF_OBSERVED_RIGHT_SHEAR_OWL,
        GAMETYPE_CUSTOM: 0
    }


def get_tf_shear(is_positive):
    if is_positive:
        return {
            GAMETYPE_OWL: ULT_TF_SHEAR_OWL,
            GAMETYPE_CUSTOM: 0
        }
    return {
        GAMETYPE_OWL: -1 * ULT_TF_SHEAR_OWL,
        GAMETYPE_CUSTOM: 0
    }


def get_ult_charge_color_pre_pos(is_left):
    if is_left:
        return {
            GAMETYPE_OWL: [ULT_CHARGE_COLOR_PRE_Y_MIN_OWL,
                           ULT_CHARGE_COLOR_PRE_HEIGHT_OWL,
                           ULT_CHARGE_COLOR_PRE_X_MIN_LEFT_OWL,
                           ULT_CHARGE_COLOR_PRE_WIDTH_OWL],
            GAMETYPE_CUSTOM: []
        }
    return {
        GAMETYPE_OWL: [ULT_CHARGE_COLOR_PRE_Y_MIN_OWL,
                       ULT_CHARGE_COLOR_PRE_HEIGHT_OWL,
                       ULT_CHARGE_COLOR_PRE_X_MIN_RIGHT_OWL,
                       ULT_CHARGE_COLOR_PRE_WIDTH_OWL],
        GAMETYPE_CUSTOM: []
    }


def get_ult_charge_color_pos(is_left):
    if is_left:
        return {
            GAMETYPE_OWL: [ULT_CHARGE_COLOR_Y_MIN_OWL,
                           ULT_CHARGE_COLOR_HEIGHT_OWL,
                           ULT_CHARGE_COLOR_X_MIN_LEFT_OWL,
                           ULT_CHARGE_COLOR_WIDTH_OWL],
            GAMETYPE_CUSTOM: []
        }
    return {
        GAMETYPE_OWL: [ULT_CHARGE_COLOR_Y_MIN_OWL,
                       ULT_CHARGE_COLOR_HEIGHT_OWL,
                       ULT_CHARGE_COLOR_X_MIN_RIGHT_OWL,
                       ULT_CHARGE_COLOR_WIDTH_OWL],
        GAMETYPE_CUSTOM: []
    }


def get_ult_charge_pre_pos(index):
    if index < 6:
        return {
            GAMETYPE_OWL: [ULT_CHARGE_PRE_Y_MIN_OWL,
                           ULT_CHARGE_PRE_HEIGHT_OWL,
                           ULT_CHARGE_PRE_X_MIN_LEFT_OWL + sum(ULT_CHARGE_PRE_GAP_LEFT_OWL[:index]),
                           ULT_CHARGE_PRE_WIDTH_OWL],
            GAMETYPE_CUSTOM: []
        }
    return {
        GAMETYPE_OWL: [ULT_CHARGE_PRE_Y_MIN_OWL,
                       ULT_CHARGE_PRE_HEIGHT_OWL,
                       ULT_CHARGE_PRE_X_MIN_RIGHT_OWL + sum(ULT_CHARGE_PRE_GAP_RIGHT_OWL[:index - 6]),
                       ULT_CHARGE_PRE_WIDTH_OWL],
        GAMETYPE_CUSTOM: []
    }


def get_ult_charge_pos(index, number):
    if number == 0:
        if index < 6:
            return {
                GAMETYPE_OWL: [ULT_CHARGE_Y_MIN_OWL,
                               ULT_CHARGE_HEIGHT_OWL,
                               ULT_CHARGE_0_X_MIN_LEFT_OWL,
                               ULT_CHARGE_WIDTH_OWL],
                GAMETYPE_CUSTOM: []
            }
        else:
            return {
                GAMETYPE_OWL: [ULT_CHARGE_Y_MIN_OWL,
                               ULT_CHARGE_HEIGHT_OWL,
                               ULT_CHARGE_0_X_MIN_RIGHT_OWL,
                               ULT_CHARGE_WIDTH_OWL],
                GAMETYPE_CUSTOM: []
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
AVATAR_X_MIN_RIGHT_OWL = 854  # x of starting point from right side
AVATAR_WIDTH_OWL = 38  # width of avatar
AVATAR_Y_MIN_OWL = 45  # y of starting point
AVATAR_HEIGHT_OWL = 30  # height of avatar
AVATAR_GAP_OWL = 70  # x-gap between 2 avatars

# Dimensions & positions of topbar avatars in OWL (not observed)
AVATAR_X_MIN_LEFT_SMALL_OWL = 62
AVATAR_X_MIN_RIGHT_SMALL_OWL = 857
AVATAR_WIDTH_SMALL_OWL = 34
AVATAR_Y_MIN_SMALL_OWL = 55
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
    """Read all reference avatar images and write into a dict

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of all reference avatar images
    """
    return {chara: ImageUtils.resize(
        ImageUtils.read_with_transparency("./images/charas/" + chara + ".png"),
        AVATAR_WIDTH_REF,
        AVATAR_HEIGHT_REF) for chara in CHARACTER_LIST}


def get_avatar_pos_small(index):
    """Get position of an avatar in one frame, given player index.

    The player is currently not observed by cam.

    Author:
        Appcell

    Args:
        index: index of player

    Returns:
        Pos array of this avatar
    """
    if index < 6:
        return {
            GAMETYPE_OWL: [AVATAR_Y_MIN_SMALL_OWL,
                           AVATAR_HEIGHT_SMALL_OWL,
                           AVATAR_X_MIN_LEFT_SMALL_OWL + index * AVATAR_GAP_SMALL_OWL,
                           AVATAR_WIDTH_SMALL_OWL],
            GAMETYPE_CUSTOM: [AVATAR_Y_MIN_SMALL_CUSTOM,
                              AVATAR_HEIGHT_SMALL_CUSTOM,
                              AVATAR_X_MIN_LEFT_SMALL_CUSTOM + index * AVATAR_GAP_SMALL_CUSTOM,
                              AVATAR_WIDTH_SMALL_CUSTOM]
        }
    else:
        return {
            GAMETYPE_OWL: [AVATAR_Y_MIN_SMALL_OWL,
                           AVATAR_HEIGHT_SMALL_OWL,
                           AVATAR_X_MIN_RIGHT_SMALL_OWL +
                           (index - 6) * AVATAR_GAP_SMALL_OWL,
                           AVATAR_WIDTH_SMALL_OWL],
            GAMETYPE_CUSTOM: [AVATAR_Y_MIN_SMALL_CUSTOM,
                              AVATAR_HEIGHT_SMALL_CUSTOM,
                              AVATAR_X_MIN_LEFT_SMALL_CUSTOM + index * AVATAR_GAP_SMALL_CUSTOM,
                              AVATAR_WIDTH_SMALL_CUSTOM]
        }


def get_avatar_pos(index):
    """Get position of an avatar in one frame, given player index.

    The player is currently observed by cam.

    Author:
        Appcell

    Args:
        index: index of player

    Returns:
        Pos array of this avatar
    """
    if index < 6:
        return {
            GAMETYPE_OWL: [AVATAR_Y_MIN_OWL,
                           AVATAR_HEIGHT_OWL,
                           AVATAR_X_MIN_LEFT_OWL + index * AVATAR_GAP_OWL,
                           AVATAR_WIDTH_OWL],
            GAMETYPE_CUSTOM: [AVATAR_Y_MIN_CUSTOM,
                              AVATAR_HEIGHT_CUSTOM,
                              AVATAR_X_MIN_LEFT_CUSTOM + index * AVATAR_GAP_CUSTOM,
                              AVATAR_WIDTH_CUSTOM]
        }
    else:
        return {
            GAMETYPE_OWL: [AVATAR_Y_MIN_OWL,
                           AVATAR_HEIGHT_OWL,
                           AVATAR_X_MIN_RIGHT_OWL +
                           (index - 6) * AVATAR_GAP_OWL,
                           AVATAR_WIDTH_OWL],
            GAMETYPE_CUSTOM: [AVATAR_Y_MIN_CUSTOM,
                              AVATAR_HEIGHT_CUSTOM,
                              AVATAR_X_MIN_LEFT_CUSTOM + index * AVATAR_GAP_CUSTOM,
                              AVATAR_WIDTH_CUSTOM]
        }


def get_avatar_diff_pos(index):
    """Get position of an avatar in one frame, given player index.

    The player is currently observed by cam.

    Author:
        Appcell

    Args:
        index: index of player

    Returns:
        Pos array of this avatar
    """
    if index < 6:
        return {
            GAMETYPE_OWL: [47,
                           4,
                           AVATAR_X_MIN_LEFT_OWL + index * AVATAR_GAP_OWL - 28,
                           28],
            GAMETYPE_CUSTOM: [AVATAR_Y_MIN_CUSTOM,
                              AVATAR_HEIGHT_CUSTOM,
                              AVATAR_X_MIN_LEFT_CUSTOM + index * AVATAR_GAP_CUSTOM,
                              AVATAR_WIDTH_CUSTOM]
        }
    else:
        return {
            GAMETYPE_OWL: [47,
                           4,
                           AVATAR_X_MIN_RIGHT_OWL + (index - 6) * AVATAR_GAP_OWL - 28,
                           28],
            GAMETYPE_CUSTOM: [AVATAR_Y_MIN_CUSTOM,
                              AVATAR_HEIGHT_CUSTOM,
                              AVATAR_X_MIN_LEFT_CUSTOM + index * AVATAR_GAP_CUSTOM,
                              AVATAR_WIDTH_CUSTOM]
        }


# **********************************************************
# ==========================================================
#                    Killfeed Row
# ==========================================================
# **********************************************************
KILLFEED_ICON_HEIGHT = {GAMETYPE_OWL: 21, GAMETYPE_CUSTOM: 21}
KILLFEED_ICON_WIDTH = {GAMETYPE_OWL: 31, GAMETYPE_CUSTOM: 31}

KILLFEED_ICON_EDGE_HEIGHT_RATIO_LEFT = {
    GAMETYPE_OWL: 0.7, GAMETYPE_CUSTOM: 0.7}
KILLFEED_ICON_EDGE_HEIGHT_RATIO_RIGHT = {
    GAMETYPE_OWL: 0.7, GAMETYPE_CUSTOM: 0.7}

KILLFEED_WIDTH = {GAMETYPE_OWL: 320, GAMETYPE_CUSTOM: 320}
KILLFEED_RIGHT_WIDTH = {GAMETYPE_OWL: 140, GAMETYPE_CUSTOM: 140}

KILLFEED_X_MIN_OWL = 963
KILLFEED_Y_MIN_OWL = 114
KILLFEED_WIDTH_OWL = 320
KILLFEED_HEIGHT_OWL = 27
KILLFEED_GAP_OWL = 35

KILLFEED_X_MIN_CUSTOM = 963
KILLFEED_Y_MIN_CUSTOM = 109
KILLFEED_WIDTH_CUSTOM = 320
KILLFEED_HEIGHT_CUSTOM = 35
KILLFEED_GAP_CUSTOM = 35

KILLFEED_MAX_PROB = {GAMETYPE_OWL: 0.6, GAMETYPE_CUSTOM: 0.6}

KILLFEED_MAX_COLOR_DISTANCE = {GAMETYPE_OWL: 90, GAMETYPE_CUSTOM: 20}


def get_killfeed_icons_ref():
    """Read all reference killfeed avatars, then write into dict

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of all reference killfeed icons
    """
    return {
        GAMETYPE_OWL: {chara: ImageUtils.resize(
            ImageUtils.read("./images/icons/" + chara + ".png"),
            KILLFEED_ICON_WIDTH[GAMETYPE_OWL],
            KILLFEED_ICON_HEIGHT[GAMETYPE_OWL]) \
            for chara in KILLFEED_OBJECT_LIST},
        GAMETYPE_CUSTOM: {chara: ImageUtils.resize(
            ImageUtils.read("./images/icons/" + chara + ".png"),
            KILLFEED_ICON_WIDTH[GAMETYPE_CUSTOM],
            KILLFEED_ICON_HEIGHT[GAMETYPE_CUSTOM]) \
            for chara in KILLFEED_OBJECT_LIST},
    }


def get_assist_icons_ref():
    """Read all reference killfeed assist avatars, then write into dict

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of all reference killfeed assist avatars
    """
    return {
        GAMETYPE_OWL: {chara: ImageUtils.resize(
            ImageUtils.read("./images/assists/" + chara + ".png"),
            ASSIST_ICON_WIDTH[GAMETYPE_OWL], ASSIST_ICON_HEIGHT[GAMETYPE_OWL]) \
            for chara in ASSIST_CHARACTER_LIST},
        GAMETYPE_CUSTOM: {chara: ImageUtils.resize(
            ImageUtils.read("./images/assists/" + chara + ".png"),
            ASSIST_ICON_WIDTH[GAMETYPE_CUSTOM],
            ASSIST_ICON_HEIGHT[GAMETYPE_CUSTOM]) \
            for chara in ASSIST_CHARACTER_LIST},
    }


def get_killfeed_team_color_pos(pos_x, position):
    """Get pixel position from which to get team color from killfeed

    Author:
        Appcell

    Args:
        pox_x: x-axis coordinate of killfeed avatar
        position: on which side the avatar lies, 'left' or 'right'

    Returns:
        Pos array of this pixel
    """

    if position == 'left':
        return {
            GAMETYPE_OWL: [2, pos_x - 10],
            GAMETYPE_CUSTOM: [2, pos_x - 10]
        }
    else:
        return {
            GAMETYPE_OWL: [2, pos_x + KILLFEED_ICON_WIDTH[GAMETYPE_OWL] + 10],
            GAMETYPE_CUSTOM: [1, pos_x + KILLFEED_ICON_WIDTH[GAMETYPE_CUSTOM] + 10]
        }


def get_killfeed_pos(index):
    """Get position of one killfeed row in one frame, given row index.

    Author:
        Appcell

    Args:
        index: index of killfeed row

    Returns:
        pos array of this killfeed row
    """
    return {
        GAMETYPE_OWL: [KILLFEED_Y_MIN_OWL + index * KILLFEED_GAP_OWL,
                       KILLFEED_HEIGHT_OWL,
                       KILLFEED_X_MIN_OWL,
                       KILLFEED_WIDTH_OWL],
        GAMETYPE_CUSTOM: [KILLFEED_Y_MIN_CUSTOM + index * KILLFEED_GAP_CUSTOM,
                          KILLFEED_HEIGHT_CUSTOM,
                          KILLFEED_X_MIN_CUSTOM,
                          KILLFEED_WIDTH_CUSTOM]
    }


def get_killfeed_with_gap_pos(index):
    """Get position of one killfeed row in one frame, given row index.

    Here it gives the image with gap. This is mainly for ability recognition,
    since sometimes the icon gets larger than killfeed itself.

    Author:
        Appcell

    Args:
        index: index of killfeed row

    Returns:
        pos array of this killfeed row
    """
    return {
        GAMETYPE_OWL: [KILLFEED_Y_MIN_OWL + index * KILLFEED_GAP_OWL,
                       KILLFEED_GAP_OWL,
                       KILLFEED_X_MIN_OWL,
                       KILLFEED_WIDTH_OWL],
        GAMETYPE_CUSTOM: [KILLFEED_Y_MIN_CUSTOM + index * KILLFEED_GAP_CUSTOM,
                          KILLFEED_GAP_CUSTOM,
                          KILLFEED_X_MIN_CUSTOM,
                          KILLFEED_WIDTH_CUSTOM]
    }


# **********************************************************
# ==========================================================
#                     Ability Code
# ==========================================================
# **********************************************************
ABILITY_NONE = 0
ABILITY_SHIFT = 1
ABILITY_E = 2
ABILITY_Q_1 = 3
ABILITY_Q_2 = 4
ABILITY_RIGHT_CLICK = 5
ABILITY_PASSIVE = 6

ABILITY_ICON_WIDTH = {GAMETYPE_OWL: 26, GAMETYPE_CUSTOM: 26}
ABILITY_ICON_HEIGHT = {GAMETYPE_OWL: 26, GAMETYPE_CUSTOM: 26}

ABILITY_ICON_REF_WIDTH = {GAMETYPE_OWL: 22, GAMETYPE_CUSTOM: 22}
ABILITY_ICON_REF_HEIGHT = {GAMETYPE_OWL: 22, GAMETYPE_CUSTOM: 22}

ABILITY_ICON_COLOR_FILTER_THRESHOLD = {GAMETYPE_OWL: 70, GAMETYPE_CUSTOM: 50}

ABILITY_GAP_ICON = {GAMETYPE_OWL: 26, GAMETYPE_CUSTOM: 26}
ABILITY_GAP_NORMAL = {GAMETYPE_OWL: 30, GAMETYPE_CUSTOM: 32}

ABILITY_ICON_Y_MIN = {GAMETYPE_OWL: 6, GAMETYPE_CUSTOM: 11}

ABILITY_LIST = {
    ANA: [1, 2],
    BASTION: [3],
    DOOMFIST: [1, 2, 3, 5],
    DVA: [1, 2, 3, 4],
    GENJI: [1, 3],
    HANZO: [1, 2, 3],
    JUNKRAT: [1, 2, 3, 6],
    LUCIO: [5],
    MCCREE: [2, 3],
    MEI: [3],
    MERCY: [2],
    MOIRA: [2, 3],
    ORISA: [5],
    PHARAH: [2, 3],
    REAPER: [3],
    REINHARDT: [1, 2, 3],
    ROADHOG: [1, 3],
    SOLDIER76: [3, 5],
    SOMBRA: [],
    SYMMETRA: [1],
    TORBJON: [1],
    TRACER: [3],
    WIDOWMAKER: [2],
    WINSTON: [1, 3],
    ZARYA: [3],
    ZENYATTA: []
}


def get_ability_icons_ref():
    """Read in all ability icons.

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of all ability icons, with chara names as keys and list of all
        abilities of this chara as values.
    """
    res_owl = {}
    res_custom = {}
    for (chara, ability_list) in ABILITY_LIST.iteritems():
        icons_list_owl = []
        icons_list_custom = []
        for i in ability_list:
            icon = ImageUtils.rgb_to_gray(ImageUtils.read(
                "./images/abilities/" + chara + "/" + str(i) + ".png"))
            icons_list_owl.append(ImageUtils.resize(
                icon,
                ABILITY_ICON_WIDTH[GAMETYPE_OWL],
                ABILITY_ICON_HEIGHT[GAMETYPE_OWL]
            ))
            icons_list_custom.append(ImageUtils.resize(
                icon,
                ABILITY_ICON_WIDTH[GAMETYPE_CUSTOM],
                ABILITY_ICON_HEIGHT[GAMETYPE_CUSTOM]
            ))
        res_owl[chara] = icons_list_owl
        res_custom[chara] = icons_list_custom

    return {
        GAMETYPE_OWL: res_owl,
        GAMETYPE_CUSTOM: res_custom
    }


def get_ability_icon_pos(pos_right):
    """Get position of ability icon

    Given left/right x-axis coordinates of 2 avatars in a killfeed row,
    calculates position of ability icon and return.

    Author:
        Appcell

    Args:
        pos_right: x-axis coordiate of right-side avatar

    Returns:
        A pos array of ability icon position in a killfeed row image.
    """
    return {
        GAMETYPE_OWL: [
            2,
            ABILITY_ICON_HEIGHT[GAMETYPE_OWL],
            pos_right - ABILITY_ICON_WIDTH[GAMETYPE_OWL] - 23,
            ABILITY_ICON_WIDTH[GAMETYPE_OWL]
        ],
        GAMETYPE_CUSTOM: [
            0,
            ABILITY_ICON_HEIGHT[GAMETYPE_CUSTOM],
            pos_right - ABILITY_ICON_WIDTH[GAMETYPE_CUSTOM] - 23,
            ABILITY_ICON_WIDTH[GAMETYPE_CUSTOM]
        ],
    }


# Not really sure about this
ASSIST_GAP = {GAMETYPE_OWL: 18, GAMETYPE_CUSTOM: 20}

ASSIST_ICON_HEIGHT = {GAMETYPE_OWL: 18, GAMETYPE_CUSTOM: 18}
ASSIST_ICON_WIDTH = {GAMETYPE_OWL: 12, GAMETYPE_CUSTOM: 12}
# **********************************************************
# ==========================================================
#                   Frame Validation
# ==========================================================
# **********************************************************
FRAME_VALIDATION_POS = {GAMETYPE_OWL: [
    0, 15, 0, 70], GAMETYPE_CUSTOM: [0, 15, 0, 70]}
FRAME_VALIDATION_COLOR_MEAN = {GAMETYPE_OWL: 230, GAMETYPE_CUSTOM: 230}
FRAME_VALIDATION_COLOR_STD = {GAMETYPE_OWL: 3, GAMETYPE_CUSTOM: 3}
FRAME_VALIDATION_EFFECT_TIME = {GAMETYPE_OWL: 2.0, GAMETYPE_CUSTOM: 2.0}
FRAME_VALIDATION_REPLAY_PROB = {GAMETYPE_OWL: 0.5, GAMETYPE_CUSTOM: 0.5}


def get_replay_icon_pos():
    return {
        GAMETYPE_OWL: [109, 66, 64, 74],
        GAMETYPE_CUSTOM: [111, 64, 64, 74],
    }


def get_replay_icon_preseason_pos():
    return {
        GAMETYPE_OWL: [109, 66, 23, 74],
        GAMETYPE_CUSTOM: [111, 64, 40, 74],
    }


def get_replay_icon_ref():
    """Read in relay icon.

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of replay icons. Actualy this is only used by OWL games.
    """
    return {
        GAMETYPE_OWL: ImageUtils.read("./images/replay.png"),
        GAMETYPE_CUSTOM: ImageUtils.read("./images/replay.png")
    }
