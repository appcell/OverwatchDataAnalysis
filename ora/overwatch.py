from .utils import image as ImageUtils
import os
import numpy as np

""" Conventions of overwatch.py macros:
    VARIABLE_NAME = {
        GAMETYPE: {
            UI_VERSION: value
        }
    }
"""

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
VERSION_NUM = {
    GAMETYPE_OWL: 2,
    GAMETYPE_CUSTOM: 1
}
MIN_RESPAWN_TIME = 10
# **********************************************************
# ==========================================================
#                       Name Codes
# ==========================================================
# **********************************************************
TEAM_LEFT = 0
TEAM_RIGHT = 1
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

ABILITY_NONE = 0
ABILITY_SHIFT = 1
ABILITY_E = 2
ABILITY_Q_1 = 3
ABILITY_Q_2 = 4
ABILITY_RIGHT_CLICK = 5
ABILITY_PASSIVE = 6

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

TEAM_COLOR_PICK_POS_LEFT = {
    GAMETYPE_OWL: {
        0: [53, 40],
        1: [53 + 27, 40 + 1]
    },
    GAMETYPE_CUSTOM: {
        0: [0, 0]
    }
}
TEAM_COLOR_PICK_POS_RIGHT = {
    GAMETYPE_OWL: {
        0: [54, 1183],
        1: [54 + 27, 1183 - 6]
    },
    GAMETYPE_CUSTOM: {
        0: [0, DEFAULT_SCREEN_WIDTH - 1]
    }
}
# **********************************************************
# ==========================================================
#              Ultimate Icon Position Defs
# ==========================================================
# **********************************************************
ULT_ICON_X_MIN_LEFT = {
    GAMETYPE_OWL: {
        0: 31,
        1: 31 + 1
    },
    GAMETYPE_CUSTOM: {
        0: 31
    }
}
ULT_ICON_X_MIN_RIGHT = {
    GAMETYPE_OWL: {
        0: 829,
        1: 829 - 6
    },
    GAMETYPE_CUSTOM: {
        0: 829
    }
}
ULT_ICON_WIDTH = {
    GAMETYPE_OWL: {
        0: 33,
        1: 33
    },
    GAMETYPE_CUSTOM: {
        0: 33
    }
}
ULT_ICON_Y_MIN = {
    GAMETYPE_OWL: {
        0: 47,
        1: 47 + 27
    },
    GAMETYPE_CUSTOM: {
        0: 47
    }
}
ULT_ICON_HEIGHT = {
    GAMETYPE_OWL: {
        0: 30,
        1: 30
    },
    GAMETYPE_CUSTOM: {
        0: 30
    }
}
ULT_ICON_GAP = {
    GAMETYPE_OWL: {
        0: 70,
        1: 70
    },
    GAMETYPE_CUSTOM: {
        0: 70
    }
}

ULT_ICON_MAX_PROB = {
    GAMETYPE_OWL: {
        0: 0.7,
        1: 0.7
    },
    GAMETYPE_CUSTOM: {
        0: 0.7
    }
}
ULT_ICON_MAX_PROB_SSIM = {
    GAMETYPE_OWL: {
        0: 0.6,
        1: 0.6
    },
    GAMETYPE_CUSTOM: {
        0: 0.6
    }
}
ULT_ICON_MAX_BRIGHTNESS = {
    GAMETYPE_OWL: {
        0: 230,
        1: 230
    },
    GAMETYPE_CUSTOM: {
        0: 230
    }
}
ULT_ICON_MAX_DEVIATION = {
    GAMETYPE_OWL: {
        0: 15,
        1: 15
    },
    GAMETYPE_CUSTOM: {
        0: 15
    }
}


def get_team_color_pick_pos(gametype, version):
    return [TEAM_COLOR_PICK_POS_LEFT[gametype][version], 
            TEAM_COLOR_PICK_POS_RIGHT[gametype][version]]


def get_ult_icon_pos(index, gametype, version):
    if index < 6:
        return [ULT_ICON_Y_MIN[gametype][version],
                ULT_ICON_HEIGHT[gametype][version],
                ULT_ICON_X_MIN_LEFT[gametype][version] + index * ULT_ICON_GAP[gametype][version],
                ULT_ICON_WIDTH[gametype][version]]
    else:
        return [ULT_ICON_Y_MIN[gametype][version],
                ULT_ICON_HEIGHT[gametype][version],
                ULT_ICON_X_MIN_RIGHT[gametype][version] + (index - 6) * ULT_ICON_GAP[gametype][version],
                ULT_ICON_WIDTH[gametype][version]]


def get_ult_icon_ref(index, gametype, version):
    if index < 6:
        return ImageUtils.read("./images/ultimate/awayUlt.png")
    else:
        return ImageUtils.read("./images/ultimate/homeUlt.png")


# **********************************************************
# ==========================================================
#              Ultimate Charge Position Defs
# ==========================================================
# **********************************************************

ULT_TF_SHEAR_LEFT ={
    GAMETYPE_OWL: {
        0: 0.25396,
        1: 0.25396
    },
    GAMETYPE_CUSTOM: {
        0: 0.25396
    }
}
ULT_TF_SHEAR_RIGHT = {
    GAMETYPE_OWL: {
        0: 0.22,
        1: 0.22
    },
    GAMETYPE_CUSTOM: {
        0: 0.22
    }
}
ULT_ADJUST_LOG_INDEX = {
    GAMETYPE_OWL: {
        0: 1.2,
        1: 1.2
    },
    GAMETYPE_CUSTOM: {
        0: 1.2
    }
}

#  Region to read ultimate charge number, pre-shear
ULT_CHARGE_PRE_X_MIN_LEFT = {
    GAMETYPE_OWL: {
        0: 20,
        1: 20 + 1
    },
    GAMETYPE_CUSTOM: {
        0: 20
    }
}
ULT_CHARGE_PRE_X_MIN_RIGHT = {
    GAMETYPE_OWL: {
        0: 825,
        1: 825 - 3
    },
    GAMETYPE_CUSTOM: {
        0: 825
    }
}
ULT_CHARGE_PRE_WIDTH = {
    GAMETYPE_OWL: {
        0: 65,
        1: 65
    },
    GAMETYPE_CUSTOM: {
        0: 65
    }
}
ULT_CHARGE_PRE_Y_MIN = {
    GAMETYPE_OWL: {
        0: 50,
        1: 50 + 23
    },
    GAMETYPE_CUSTOM: {
        0: 50
    }
}
ULT_CHARGE_PRE_HEIGHT = {
    GAMETYPE_OWL: {
        0: 50,
        1: 50
    },
    GAMETYPE_CUSTOM: {
        0: 50
    }
}
ULT_CHARGE_PRE_GAP = {
    GAMETYPE_OWL: {
        0: 70,
        1: 70
    },
    GAMETYPE_CUSTOM: {
        0: 70
    }
}

ULT_CHARGE_PRE_WIDTH_OBSERVED = {
    GAMETYPE_OWL: {
        0: 65,
        1: 65
    },
    GAMETYPE_CUSTOM: {
        0: 65
    }
}
ULT_CHARGE_PRE_HEIGHT_OBSERVED = {
    GAMETYPE_OWL: {
        0: 50,
        1: 50
    },
    GAMETYPE_CUSTOM: {
        0: 50
    }
}

#  Region to read ultimate charge number, post-shear, 1st and 2nd number
ULT_CHARGE_X_MIN_LEFT = {
    GAMETYPE_OWL: {
        0: 15,
        1: 15
    },
    GAMETYPE_CUSTOM: {
        0: 15
    }
}
ULT_CHARGE_X_MIN_RIGHT = {
    GAMETYPE_OWL: {
        0: 4,
        1: 4
    },
    GAMETYPE_CUSTOM: {
        0: 4
    }
}
ULT_CHARGE_WIDTH = {
    GAMETYPE_OWL: {
        0: 23,
        1: 23 + 3
    },
    GAMETYPE_CUSTOM: {
        0: 23
    }
}
ULT_CHARGE_NUMBER_WIDTH = {
    GAMETYPE_OWL: {
        0: 8,
        1: 8
    },
    GAMETYPE_CUSTOM: {
        0: 8
    }
}
ULT_CHARGE_NUMBER_WIDTH_OBSERVED = {
    GAMETYPE_OWL: {
        0: 9,
        1: 9
    },
    GAMETYPE_CUSTOM: {
        0: 9
    }
}
ULT_CHARGE_NUMBER_COLOR_THRESHOLD = {
    GAMETYPE_OWL: {
        0: 0.6,
        1: 0.6
    },
    GAMETYPE_CUSTOM: {
        0: 0.6
    }
}
ULT_CHARGE_Y_MIN = {
    GAMETYPE_OWL: {
        0: 1,
        1: 1
    },
    GAMETYPE_CUSTOM: {
        0: 1
    }
}

ULT_CHARGE_HEIGHT = {
    GAMETYPE_OWL: {
        0: 25,
        1: 25
    },
    GAMETYPE_CUSTOM: {
        0: 25
    }
}
ULT_GAP_DEVIATION_LIMIT = {
    GAMETYPE_OWL: {
        0: 0.2,
        1: 0.2
    },
    GAMETYPE_CUSTOM: {
        0: 0.2
    }
}

# For img read-in
ULT_CHARGE_IMG_WIDTH = {
    GAMETYPE_OWL: {
        0: 6,
        1: 6
    },
    GAMETYPE_CUSTOM: {
        0: 6
    }
}
ULT_CHARGE_IMG_WIDTH_OBSERVED = {
    GAMETYPE_OWL: {
        0: 7,
        1: 7
    },
    GAMETYPE_CUSTOM: {
        0: 7
    }
}

ULT_CHARGE_IMG_HEIGHT = {
    GAMETYPE_OWL: {
        0: 16,
        1: 16
    },
    GAMETYPE_CUSTOM: {
        0: 16
    }
}
ULT_CHARGE_IMG_HEIGHT_OBSERVED = {
    GAMETYPE_OWL: {
        0: 18,
        1: 18
    },
    GAMETYPE_CUSTOM: {
        0: 18
    }
}

def get_tf_shear(index, gametype, version):
    if index < 6:
        return ULT_TF_SHEAR_LEFT[gametype][version]
    else:
        return ULT_TF_SHEAR_RIGHT[gametype][version]

def get_ult_charge_pre_pos(index, gametype, version):
    if index < 6:
        return [ULT_CHARGE_PRE_Y_MIN[gametype][version],
                ULT_CHARGE_PRE_HEIGHT[gametype][version],
                ULT_CHARGE_PRE_X_MIN_LEFT[gametype][version] + index * ULT_CHARGE_PRE_GAP[gametype][version],
                ULT_CHARGE_PRE_WIDTH[gametype][version]]
    else:
        return [ULT_CHARGE_PRE_Y_MIN[gametype][version],
                ULT_CHARGE_PRE_HEIGHT[gametype][version],
                ULT_CHARGE_PRE_X_MIN_RIGHT[gametype][version] + (index - 6) * ULT_CHARGE_PRE_GAP[gametype][version],
                ULT_CHARGE_PRE_WIDTH[gametype][version]]


def get_ult_charge_pos(index, gametype, version):
    if index < 6:
        return [ULT_CHARGE_Y_MIN[gametype][version],
                ULT_CHARGE_HEIGHT[gametype][version],
                ULT_CHARGE_X_MIN_LEFT[gametype][version],
                ULT_CHARGE_WIDTH[gametype][version]]
    else:
        return [ULT_CHARGE_Y_MIN[gametype][version],
                ULT_CHARGE_HEIGHT[gametype][version],
                ULT_CHARGE_X_MIN_RIGHT[gametype][version],
                ULT_CHARGE_WIDTH[gametype][version]]


def get_ult_charge_numbers_ref(gametype, version):
    if gametype == GAMETYPE_OWL:
        ult_charge_icons_ref_owl = []
        ult_charge_icons_observed_ref_owl = []
        for i in range(0, 10):
            img = ImageUtils.rgb_to_gray(
                ImageUtils.read("./images/ultimate/owl/" + str(i) + ".png"))
            ult_charge_icons_ref_owl.append(ImageUtils.resize(
                img,
                int(img.shape[1] * ULT_CHARGE_IMG_HEIGHT[gametype][version]/img.shape[0]),
                ULT_CHARGE_IMG_HEIGHT[gametype][version]
                ))
            ult_charge_icons_observed_ref_owl.append(ImageUtils.resize(
                img,
                int(img.shape[1] * ULT_CHARGE_IMG_HEIGHT_OBSERVED[gametype][version]/img.shape[0]),
                ULT_CHARGE_IMG_HEIGHT_OBSERVED[gametype][version]
                ))
        return {
            "observed": ult_charge_icons_observed_ref_owl,
            "normal": ult_charge_icons_ref_owl
        }
    else:
        return {
            "observed": [],
            "normal": []
        }


# **********************************************************
# ==========================================================
#               Topbar Avatar Position Defs
# ==========================================================
# **********************************************************

AVATAR_WIDTH_REF = {
    GAMETYPE_OWL: {
        0: 38,
        1: 38
    },
    GAMETYPE_CUSTOM: {
        0: 38
    }
}
AVATAR_HEIGHT_REF = {
    GAMETYPE_OWL: {
        0: 30,
        1: 30
    },
    GAMETYPE_CUSTOM: {
        0: 30
    }
}
AVATAR_X_MIN_LEFT = {
    GAMETYPE_OWL: {
        0: 62,
        1: 62 + 1
    },
    GAMETYPE_CUSTOM: {
        0: 62
    }
}
AVATAR_X_MIN_LEFT_OBSERVED = {
    GAMETYPE_OWL: {
        0: 62,
        1: 62 + 1
    },
    GAMETYPE_CUSTOM: {
        0: 62
    }
}
AVATAR_X_MIN_RIGHT = {
    GAMETYPE_OWL: {
        0: 857,
        1: 857 - 6
    },
    GAMETYPE_CUSTOM: {
        0: 857
    }
}
AVATAR_X_MIN_RIGHT_OBSERVED = {
    GAMETYPE_OWL: {
        0: 854,
        1: 854 - 6
    },
    GAMETYPE_CUSTOM: {
        0: 854
    }
}
AVATAR_WIDTH = {
    GAMETYPE_OWL: {
        0: 39,
        1: 39
    },
    GAMETYPE_CUSTOM: {
        0: 39
    }
}
AVATAR_WIDTH_OBSERVED = {
    GAMETYPE_OWL: {
        0: 45,
        1: 45
    },
    GAMETYPE_CUSTOM: {
        0: 45
    }
}
AVATAR_Y_MIN = {
    GAMETYPE_OWL: {
        0: 48,
        1: 48 + 27
    },
    GAMETYPE_CUSTOM: {
        0: 48
    }
}
AVATAR_Y_MIN_OBSERVED = {
    GAMETYPE_OWL: {
        0: 45,
        1: 45 + 27
    },
    GAMETYPE_CUSTOM: {
        0: 45
    }
}
AVATAR_HEIGHT = {
    GAMETYPE_OWL: {
        0: 26,
        1: 26
    },
    GAMETYPE_CUSTOM: {
        0: 26
    }
}
AVATAR_HEIGHT_OBSERVED = {
    GAMETYPE_OWL: {
        0: 30,
        1: 30
    },
    GAMETYPE_CUSTOM: {
        0: 30
    }
}
AVATAR_GAP = {
    GAMETYPE_OWL: {
        0: 71,
        1: 71
    },
    GAMETYPE_CUSTOM: {
        0: 71
    }
}
AVATAR_GAP_OBSERVED = {
    GAMETYPE_OWL: {
        0: 70,
        1: 70
    },
    GAMETYPE_CUSTOM: {
        0: 70
    }
}

# For telling difference between observed & non-observed avatars
AVATAR_DIFF_Y_MIN = {
    GAMETYPE_OWL: {
        0: 47,
        1: 47 + 27
    },
    GAMETYPE_CUSTOM: {
        0: 47
    }
}
AVATAR_DIFF_HIGHT = {
    GAMETYPE_OWL: {
        0: 4,
        1: 4
    },
    GAMETYPE_CUSTOM: {
        0: 4
    }
}
AVATAR_DIFF_WIDTH = {
    GAMETYPE_OWL: {
        0: 28,
        1: 28
    },
    GAMETYPE_CUSTOM: {
        0: 28
    }
}

def get_avatars_ref_observed(gametype, version):
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
        AVATAR_WIDTH_REF[gametype][version],
        AVATAR_HEIGHT_REF[gametype][version]) for chara in CHARACTER_LIST}


def get_avatar_pos(index, gametype, version):
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
        return [AVATAR_Y_MIN[gametype][version],
                AVATAR_HEIGHT[gametype][version],
                AVATAR_X_MIN_LEFT[gametype][version] + index * AVATAR_GAP[gametype][version],
                AVATAR_WIDTH[gametype][version]]
    else:
        return [AVATAR_Y_MIN[gametype][version],
                AVATAR_HEIGHT[gametype][version],
                AVATAR_X_MIN_RIGHT[gametype][version] + (index - 6) * AVATAR_GAP[gametype][version],
                AVATAR_WIDTH[gametype][version]]


def get_avatar_pos_observed(index, gametype, version):
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
        return [AVATAR_Y_MIN_OBSERVED[gametype][version],
                AVATAR_HEIGHT_OBSERVED[gametype][version],
                AVATAR_X_MIN_LEFT_OBSERVED[gametype][version] + index * AVATAR_GAP_OBSERVED[gametype][version],
                AVATAR_WIDTH_OBSERVED[gametype][version]]
    else:
        return [AVATAR_Y_MIN_OBSERVED[gametype][version],
                AVATAR_HEIGHT_OBSERVED[gametype][version],
                AVATAR_X_MIN_LEFT_OBSERVED[gametype][version] + (index - 6) * AVATAR_GAP_OBSERVED[gametype][version],
                AVATAR_WIDTH_OBSERVED[gametype][version]]

def get_avatar_diff_pos(index, gametype, version):
    """Get position of ROI of difference between observed/non-observed avatars

    Author:
        Appcell

    Args:
        index: index of player

    Returns:
        Pos array of ROI
    """
    if index < 6:
        return [AVATAR_DIFF_Y_MIN[gametype][version],
                AVATAR_DIFF_HIGHT[gametype][version],
                AVATAR_X_MIN_LEFT[gametype][version] + index * AVATAR_GAP[gametype][version] - AVATAR_DIFF_WIDTH[gametype][version],
                AVATAR_DIFF_WIDTH[gametype][version]]
    else:
        return [AVATAR_DIFF_Y_MIN[gametype][version],
                AVATAR_DIFF_HIGHT[gametype][version],
                AVATAR_X_MIN_RIGHT[gametype][version] + (index - 6) * AVATAR_GAP[gametype][version] - AVATAR_DIFF_WIDTH[gametype][version],
                AVATAR_DIFF_WIDTH[gametype][version]]


# **********************************************************
# ==========================================================
#                    Killfeed Row
# ==========================================================
# **********************************************************
KILLFEED_ICON_HEIGHT = {
    GAMETYPE_OWL: {
        0: 21,
        1: 21
    },
    GAMETYPE_CUSTOM: {
        0: 21
    }
}
KILLFEED_ICON_WIDTH = {
    GAMETYPE_OWL: {
        0: 31,
        1: 31
    },
    GAMETYPE_CUSTOM: {
        0: 31
    }
}

KILLFEED_ICON_EDGE_HEIGHT_RATIO_LEFT = {
    GAMETYPE_OWL: {
        0: 0.7,
        1: 0.7
    },
    GAMETYPE_CUSTOM: {
        0: 0.7
    }
}
KILLFEED_ICON_EDGE_HEIGHT_RATIO_RIGHT = {
    GAMETYPE_OWL: {
        0: 0.7,
        1: 0.7
    },
    GAMETYPE_CUSTOM: {
        0: 0.7
    }
}

KILLFEED_WIDTH = {
    GAMETYPE_OWL: {
        0: 320,
        1: 320
    },
    GAMETYPE_CUSTOM: {
        0: 320
    }
}
KILLFEED_RIGHT_WIDTH = {
    GAMETYPE_OWL: {
        0: 140,
        1: 140
    },
    GAMETYPE_CUSTOM: {
        0: 140
    }
}

KILLFEED_X_MIN = {
    GAMETYPE_OWL: {
        0: 963,
        1: 963 - 10
    },
    GAMETYPE_CUSTOM: {
        0: 963
    }
}
KILLFEED_Y_MIN = {
    GAMETYPE_OWL: {
        0: 114,
        1: 114 + 25
    },
    GAMETYPE_CUSTOM: {
        0: 114
    }
}
KILLFEED_WIDTH = {
    GAMETYPE_OWL: {
        0: 320,
        1: 320
    },
    GAMETYPE_CUSTOM: {
        0: 320
    }
}
KILLFEED_HEIGHT = {
    GAMETYPE_OWL: {
        0: 27,
        1: 27
    },
    GAMETYPE_CUSTOM: {
        0: 27
    }
}
KILLFEED_GAP = {
    GAMETYPE_OWL: {
        0: 35,
        1: 35
    },
    GAMETYPE_CUSTOM: {
        0: 35
    }
}

KILLFEED_MAX_PROB = {
    GAMETYPE_OWL: {
        0: 0.6,
        1: 0.6
    },
    GAMETYPE_CUSTOM: {
        0: 0.6
    }
}
KILLFEED_SSIM_THRESHOLD = {
    GAMETYPE_OWL: {
        0: 0.35,
        1: 0.35
    },
    GAMETYPE_CUSTOM: {
        0: 0.35
    }
}
KILLFEED_MAX_COLOR_DISTANCE = {
    GAMETYPE_OWL: {
        0: 120,
        1: 120
    },
    GAMETYPE_CUSTOM: {
        0: 120
    }
}

KILLFEED_TEAM_COLOR_POS_Y = {
    GAMETYPE_OWL: {
        0: 2,
        1: 3
    },
    GAMETYPE_CUSTOM: {
        0: 2
    }
}

KILLFEED_TEAM_COLOR_POS_X_LEFT = {
    GAMETYPE_OWL: {
        0: -10,
        1: -10
    },
    GAMETYPE_CUSTOM: {
        0: -10
    }
}
KILLFEED_TEAM_COLOR_POS_X_RIGHT = {
    GAMETYPE_OWL: {
        0: 10,
        1: 10
    },
    GAMETYPE_CUSTOM: {
        0: 10
    }
}
def get_killfeed_icons_ref(gametype, version):
    """Read all reference killfeed avatars, then write into dict

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of all reference killfeed icons
    """
    return {chara: ImageUtils.resize(
            ImageUtils.read("./images/icons/" + chara + ".png"),
            KILLFEED_ICON_WIDTH[gametype][version],
            KILLFEED_ICON_HEIGHT[gametype][version]) \
            for chara in KILLFEED_OBJECT_LIST}


def get_assist_icons_ref(gametype, version):
    """Read all reference killfeed assist avatars, then write into dict

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of all reference killfeed assist avatars
    """
    return {chara: ImageUtils.resize(
            ImageUtils.read("./images/assists/" + chara + ".png"),
            ASSIST_ICON_WIDTH[gametype][version], ASSIST_ICON_HEIGHT[gametype][version]) \
            for chara in ASSIST_CHARACTER_LIST}


def get_killfeed_team_color_pos(pos_x, position, gametype, version):
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
        return [KILLFEED_TEAM_COLOR_POS_Y[gametype][version], 
                pos_x + KILLFEED_TEAM_COLOR_POS_X_LEFT[gametype][version]]
    else:
        return [KILLFEED_TEAM_COLOR_POS_Y[gametype][version], 
                pos_x + KILLFEED_TEAM_COLOR_POS_X_RIGHT[gametype][version] + KILLFEED_ICON_WIDTH[gametype][version]]


def get_killfeed_pos(index, gametype, version):
    """Get position of one killfeed row in one frame, given row index.

    Author:
        Appcell

    Args:
        index: index of killfeed row

    Returns:
        pos array of this killfeed row
    """
    return [KILLFEED_Y_MIN[gametype][version] + index * KILLFEED_GAP[gametype][version],
            KILLFEED_HEIGHT[gametype][version],
            KILLFEED_X_MIN[gametype][version],
            KILLFEED_WIDTH[gametype][version]]


def get_killfeed_with_gap_pos(index, gametype, version):
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
    return [KILLFEED_Y_MIN[gametype][version] + index * KILLFEED_GAP[gametype][version],
            KILLFEED_GAP[gametype][version],
            KILLFEED_X_MIN[gametype][version],
            KILLFEED_WIDTH[gametype][version]]


# **********************************************************
# ==========================================================
#                     Ability Code
# ==========================================================
# **********************************************************
ABILITY_ICON_WIDTH = {
    GAMETYPE_OWL: {
        0: 26,
        1: 26
    },
    GAMETYPE_CUSTOM: {
        0: 26
    }
}
ABILITY_ICON_HEIGHT = {
    GAMETYPE_OWL: {
        0: 26,
        1: 26
    },
    GAMETYPE_CUSTOM: {
        0: 26
    }
}

ABILITY_ICON_REF_WIDTH = {
    GAMETYPE_OWL: {
        0: 22,
        1: 22
    },
    GAMETYPE_CUSTOM: {
        0: 22
    }
}
ABILITY_ICON_REF_HEIGHT = {
    GAMETYPE_OWL: {
        0: 22,
        1: 22
    },
    GAMETYPE_CUSTOM: {
        0: 22
    }
}

ABILITY_ICON_COLOR_FILTER_THRESHOLD = {
    GAMETYPE_OWL: {
        0: 70,
        1: 70
    },
    GAMETYPE_CUSTOM: {
        0: 70
    }
}

ABILITY_GAP_ICON = {
    GAMETYPE_OWL: {
        0: 26,
        1: 26
    },
    GAMETYPE_CUSTOM: {
        0: 26
    }
}
ABILITY_GAP_NORMAL = {
    GAMETYPE_OWL: {
        0: 30,
        1: 30
    },
    GAMETYPE_CUSTOM: {
        0: 30
    }
}

ASSIST_ICON_Y_MIN = {
    GAMETYPE_OWL: {
        0: 6,
        1: 6
    },
    GAMETYPE_CUSTOM: {
        0: 6
    }
}
ABILITY_ICON_Y_MIN = {
    GAMETYPE_OWL: {
        0: 2,
        1: 2
    },
    GAMETYPE_CUSTOM: {
        0: 2
    }
}

ABILITY_ICON_X_MIN = {
    GAMETYPE_OWL: {
        0: -23,
        1: -23
    },
    GAMETYPE_CUSTOM: {
        0: -23
    }
}

def get_ability_icons_ref(gametype, version):
    """Read in all ability icons.

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of all ability icons, with chara names as keys and list of all
        abilities of this chara as values.
    """
    res = {}
    for (chara, ability_list) in ABILITY_LIST.items():
        icons_list = []
        for i in ability_list:
            icon = ImageUtils.rgb_to_gray(ImageUtils.read(
                "./images/abilities/" + chara + "/" + str(i) + ".png"))
            icons_list.append(ImageUtils.resize(
                icon,
                ABILITY_ICON_WIDTH[gametype][version],
                ABILITY_ICON_HEIGHT[gametype][version]
            ))
        res[chara] = icons_list

    return res

def get_ability_icon_pos(pos_right, gametype, version):
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
    return [ABILITY_ICON_Y_MIN[gametype][version],
            ABILITY_ICON_HEIGHT[gametype][version],
            ABILITY_ICON_X_MIN[gametype][version] + pos_right - ABILITY_ICON_WIDTH[gametype][version],
            ABILITY_ICON_WIDTH[gametype][version]]


# Not really sure about this
ASSIST_GAP = {
    GAMETYPE_OWL: {
        0: 18,
        1: 18
    },
    GAMETYPE_CUSTOM: {
        0: 18
    }
}

ASSIST_ICON_HEIGHT = {
    GAMETYPE_OWL: {
        0: 18,
        1: 18
    },
    GAMETYPE_CUSTOM: {
        0: 18
    }
}
ASSIST_ICON_WIDTH = {
    GAMETYPE_OWL: {
        0: 12,
        1: 12
    },
    GAMETYPE_CUSTOM: {
        0: 12
    }
}

ASSIST_ICON_X_OFFSET = {
    GAMETYPE_OWL: {
        0: 8,
        1: 8
    },
    GAMETYPE_CUSTOM: {
        0: 8
    }
}

def get_assist_icon_pos(pos_x, assist_index, gametype, version):
    return [ASSIST_ICON_Y_MIN[gametype][version],
            ASSIST_ICON_HEIGHT[gametype][version],
            ASSIST_ICON_X_OFFSET[gametype][version] + pos_x \
            + assist_index * ASSIST_GAP[gametype][version] + KILLFEED_ICON_WIDTH[gametype][version],
            ASSIST_ICON_WIDTH[gametype][version]]
# **********************************************************
# ==========================================================
#                   Frame Validation
# ==========================================================
# **********************************************************
FRAME_VALIDATION_POS = {
    GAMETYPE_OWL: {
        0: [0, 15, 0, 70],
        1: [37, 15, 0, 70]
    },
    GAMETYPE_CUSTOM: {
        0: [0, 15, 0, 70]
    }
}

def get_frame_validation_pos(gametype, version):
    return FRAME_VALIDATION_POS[gametype][version]

FRAME_VALIDATION_COLOR_MEAN = {
    GAMETYPE_OWL: {
        0: 230,
        1: 230
    },
    GAMETYPE_CUSTOM: {
        0: 230
    }
}
FRAME_VALIDATION_COLOR_STD = {
    GAMETYPE_OWL: {
        0: 10,
        1: 10
    },
    GAMETYPE_CUSTOM: {
        0: 3
    }
}
FRAME_VALIDATION_EFFECT_TIME = {
    GAMETYPE_OWL: {
        0: 2.0,
        1: 2.0
    },
    GAMETYPE_CUSTOM: {
        0: 2.0
    }
}
FRAME_VALIDATION_REPLAY_PROB = {
    GAMETYPE_OWL: {
        0: 0.5,
        1: 0.5
    },
    GAMETYPE_CUSTOM: {
        0: 0.5
    }
}

REPLAY_ICON_POS = {
    GAMETYPE_OWL: {
        0: [109, 66, 64, 74],
        1: [149, 66, 64, 74]
    },
    GAMETYPE_CUSTOM: {
        0: [111, 64, 64, 74]
    }
}

REPLAY_ICON_POS_PRESEASON = {
    GAMETYPE_OWL: {
        0: [109, 66, 23, 74],
        1: [109, 66, 23, 74]
    },
    GAMETYPE_CUSTOM: {
        0: [109, 66, 23, 74]
    }
}
def get_replay_icon_pos(gametype, version):
    return REPLAY_ICON_POS[gametype][version]

def get_replay_icon_preseason_pos(gametype, version):
    return REPLAY_ICON_POS_PRESEASON[gametype][version]


def get_replay_icon_ref(gametype, version):
    """Read in relay icon.

    Author:
        Appcell

    Args:
        None

    Returns:
        A dict of replay icons. Actually this is only for OWL games.
    """

    return ImageUtils.read("./images/replay.png")
