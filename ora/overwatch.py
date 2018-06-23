from .utils import image as ImageUtils
import os
import math
import numpy as np
from os import listdir
from os.path import isfile, join
import json


# **********************************************************
# ==========================================================
#                  Read-in config files
# ==========================================================
# **********************************************************
GAMETYPE_OWL = 0
GAMETYPE_CUSTOM = 1
custom_config_files = [join("./ora/configs/custom", f) for f in listdir("./ora/configs/custom") if isfile(join("./ora/configs/custom", f))]
owl_config_files = [join("./ora/configs/owl", f) for f in listdir("./ora/configs/owl") if isfile(join("./ora/configs/owl", f))]

VERSION_NUM = {
    GAMETYPE_OWL: len(owl_config_files),
    GAMETYPE_CUSTOM: len(custom_config_files)
}
configs = {
    GAMETYPE_OWL: [],
    GAMETYPE_CUSTOM: []
}

for file_path in custom_config_files:
    with open(file_path, encoding='utf-8-sig') as json_file:
        json_data = json.load(json_file)
        configs[GAMETYPE_CUSTOM].append(json_data)

for file_path in owl_config_files:
    with open(file_path, encoding='utf-8-sig') as json_file:
        json_data = json.load(json_file)
        configs[GAMETYPE_OWL].append(json_data)

def get_ui_variable(name, gametype, version):
    if name in configs[gametype][version]:
        if name == "TEAM_COLORS_DEFAULT":
            res = []
            for color in configs[gametype][version][name]:
                res.append(np.array(color))
            return res
        else:
            return configs[gametype][version][name]
    else:
        return 0

# **********************************************************
# ==========================================================
#                       Meta Macros
# ==========================================================
# **********************************************************
ANALYZER_FPS = 2
DEFAULT_SCREEN_WIDTH = 1280
DEFAULT_SCREEN_HEIGHT = 720
MIN_RESPAWN_TIME = 10

# Time frame For making sure of chara switching, ult usage etc
MIN_SEARCH_TIME_FRAME = 1
# **********************************************************
# ==========================================================
#                       Name Codes
# ==========================================================
# **********************************************************
TEAM_LEFT = 0
TEAM_RIGHT = 1
LEFT = 0
RIGHT = 1
# **********************************************************
# ==========================================================
#               Chara & Non-chara Objects List
# ==========================================================
# **********************************************************
ANA = "ana"
BASTION = "bastion"
BRIGITTE = "brigitte"
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
CHARACTER_LIST = [ANA, BASTION, BRIGITTE, DOOMFIST, DVA, GENJI, HANZO, JUNKRAT,
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
# For those abilities with version changes
ABILITY_E2 = 7 # e.g. Hanzo

ABILITY_LIST = {
    ANA: [1, 2],
    BASTION: [3],
    BRIGITTE: [1, 5],
    DOOMFIST: [1, 2, 3, 5],
    DVA: [1, 2, 3, 4],
    GENJI: [1, 3],
    HANZO: [1, 2, 3, 7],
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

# D.Va status
IS_WITH_MEKA = 0
IS_WITHOUT_MEKA = 1
IS_NOT_DVA = 2

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


def get_team_color_pick_pos(gametype, version):
    return [get_ui_variable("TEAM_COLOR_PICK_POS_LEFT", gametype, version), 
            get_ui_variable("TEAM_COLOR_PICK_POS_RIGHT", gametype, version)]


def get_ult_icon_pos(index, gametype, version):
    if index < 6:
        return [round(get_ui_variable("ULT_ICON_Y_MIN", gametype, version)),
                round(get_ui_variable("ULT_ICON_HEIGHT", gametype, version)),
                round(get_ui_variable("ULT_ICON_X_MIN_LEFT", gametype, version) + index * get_ui_variable("ULT_ICON_GAP", gametype, version)),
                round(get_ui_variable("ULT_ICON_WIDTH", gametype, version))]
    else:
        return [round(get_ui_variable("ULT_ICON_Y_MIN", gametype, version)),
                round(get_ui_variable("ULT_ICON_HEIGHT", gametype, version)),
                round(get_ui_variable("ULT_ICON_X_MIN_RIGHT", gametype, version) + (index - 6) * get_ui_variable("ULT_ICON_GAP", gametype, version)),
                round(get_ui_variable("ULT_ICON_WIDTH", gametype, version))]


def get_ult_icon_ref(index, gametype, version):
    if gametype == GAMETYPE_OWL:
        if index < 6:
            return ImageUtils.read("./images/ultimate/awayUlt.png")
        else:
            return ImageUtils.read("./images/ultimate/homeUlt.png")
    if gametype == GAMETYPE_CUSTOM:
        if index < 6:
            return ImageUtils.read("./images/ultimate/awayUlt.png")
        else:
            return ImageUtils.read("./images/ultimate/awayUlt.png")

def get_tf_shear(index, gametype, version):
    if index < 6:
        return get_ui_variable("ULT_TF_SHEAR_LEFT", gametype, version)
    else:
        return get_ui_variable("ULT_TF_SHEAR_RIGHT", gametype, version)

def get_ult_charge_pre_pos(index, gametype, version):
    if index < 6:
        return [math.floor(get_ui_variable("ULT_CHARGE_PRE_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_PRE_HEIGHT", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_PRE_X_MIN_LEFT", gametype, version) \
                    + index * get_ui_variable("ULT_CHARGE_PRE_GAP", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_PRE_WIDTH", gametype, version))]
    else:
        return [math.floor(get_ui_variable("ULT_CHARGE_PRE_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_PRE_HEIGHT", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_PRE_X_MIN_RIGHT", gametype, version) \
                    + (index - 6) * get_ui_variable("ULT_CHARGE_PRE_GAP", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_PRE_WIDTH", gametype, version))]


def get_ult_charge_pos(index, gametype, version):
    if index < 6:
        return [math.floor(get_ui_variable("ULT_CHARGE_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_HEIGHT", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_X_MIN_LEFT", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_WIDTH", gametype, version))]
    else:
        return [math.floor(get_ui_variable("ULT_CHARGE_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_HEIGHT", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_X_MIN_RIGHT", gametype, version)),
                math.floor(get_ui_variable("ULT_CHARGE_WIDTH", gametype, version))]


def get_ult_charge_numbers_ref(gametype, version):
    if gametype == GAMETYPE_OWL:
        ult_charge_icons_ref_owl = []
        ult_charge_icons_observed_ref_owl = []
        for i in range(0, 10):
            img = ImageUtils.rgb_to_gray(
                ImageUtils.read("./images/ultimate/owl/" + str(i) + ".png"))
            ult_charge_icons_ref_owl.append(ImageUtils.resize(
                img,
                int(img.shape[1] * get_ui_variable("ULT_CHARGE_IMG_HEIGHT", gametype, version)/img.shape[0]),
                get_ui_variable("ULT_CHARGE_IMG_HEIGHT", gametype, version)
                ))
            ult_charge_icons_observed_ref_owl.append(ImageUtils.resize(
                img,
                int(img.shape[1] * get_ui_variable("ULT_CHARGE_IMG_HEIGHT_OBSERVED", gametype, version)/img.shape[0]),
                get_ui_variable("ULT_CHARGE_IMG_HEIGHT_OBSERVED", gametype, version)
                ))
        return {
            "observed": ult_charge_icons_observed_ref_owl,
            "normal": ult_charge_icons_ref_owl
        }
    else:
        ult_charge_icons_ref_owl = []
        ult_charge_icons_observed_ref_owl = []
        for i in range(0, 10):
            img = ImageUtils.rgb_to_gray(
                ImageUtils.read("./images/ultimate/owl/" + str(i) + ".png"))
            ult_charge_icons_ref_owl.append(ImageUtils.resize(
                img,
                int(img.shape[1] * get_ui_variable("ULT_CHARGE_IMG_HEIGHT", gametype, version)/img.shape[0]),
                get_ui_variable("ULT_CHARGE_IMG_HEIGHT", gametype, version)
                ))
            ult_charge_icons_observed_ref_owl.append(ImageUtils.resize(
                img,
                int(img.shape[1] * get_ui_variable("ULT_CHARGE_IMG_HEIGHT_OBSERVED", gametype, version)/img.shape[0]),
                get_ui_variable("ULT_CHARGE_IMG_HEIGHT_OBSERVED", gametype, version)
                ))
        return {
            "observed": ult_charge_icons_observed_ref_owl,
            "normal": ult_charge_icons_ref_owl
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
        get_ui_variable("AVATAR_WIDTH_REF", gametype, version),
        get_ui_variable("AVATAR_HEIGHT_REF", gametype, version)) for chara in CHARACTER_LIST}


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
        return [math.floor(get_ui_variable("AVATAR_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("AVATAR_HEIGHT", gametype, version)),
                math.floor(get_ui_variable("AVATAR_X_MIN_LEFT", gametype, version) + index * get_ui_variable("AVATAR_GAP", gametype, version)),
                math.floor(get_ui_variable("AVATAR_WIDTH", gametype, version))]
    else:
        return [math.floor(get_ui_variable("AVATAR_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("AVATAR_HEIGHT", gametype, version)),
                math.floor(get_ui_variable("AVATAR_X_MIN_RIGHT", gametype, version) + (index - 6) * get_ui_variable("AVATAR_GAP", gametype, version)),
                math.floor(get_ui_variable("AVATAR_WIDTH", gametype, version))]


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
        return [math.floor(get_ui_variable("AVATAR_Y_MIN_OBSERVED", gametype, version)),
                math.floor(get_ui_variable("AVATAR_HEIGHT_OBSERVED", gametype, version)),
                math.floor(get_ui_variable("AVATAR_X_MIN_LEFT_OBSERVED", gametype, version) + index * get_ui_variable("AVATAR_GAP_OBSERVED", gametype, version)),
                math.floor(get_ui_variable("AVATAR_WIDTH_OBSERVED", gametype, version))]
    else:
        return [math.floor(get_ui_variable("AVATAR_Y_MIN_OBSERVED", gametype, version)),
                math.floor(get_ui_variable("AVATAR_HEIGHT_OBSERVED", gametype, version)),
                math.floor(get_ui_variable("AVATAR_X_MIN_LEFT_OBSERVED", gametype, version) + (index - 6) * get_ui_variable("AVATAR_GAP_OBSERVED", gametype, version)),
                math.floor(get_ui_variable("AVATAR_WIDTH_OBSERVED", gametype, version))]

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
        return [math.floor(get_ui_variable("AVATAR_DIFF_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("AVATAR_DIFF_HIGHT", gametype, version)),
                math.floor(get_ui_variable("AVATAR_X_MIN_LEFT", gametype, version) + index * get_ui_variable("AVATAR_GAP", gametype, version) - get_ui_variable("AVATAR_DIFF_WIDTH", gametype, version)),
                math.floor(get_ui_variable("AVATAR_DIFF_WIDTH", gametype, version))]
    else:
        return [math.floor(get_ui_variable("AVATAR_DIFF_Y_MIN", gametype, version)),
                math.floor(get_ui_variable("AVATAR_DIFF_HIGHT", gametype, version)),
                math.floor(get_ui_variable("AVATAR_X_MIN_RIGHT", gametype, version) + (index - 6) * get_ui_variable("AVATAR_GAP", gametype, version) - get_ui_variable("AVATAR_DIFF_WIDTH", gametype, version)),
                math.floor(get_ui_variable("AVATAR_DIFF_WIDTH", gametype, version))]


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
            get_ui_variable("KILLFEED_ICON_WIDTH", gametype, version),
            get_ui_variable("KILLFEED_ICON_HEIGHT", gametype, version)) \
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
            get_ui_variable("ASSIST_ICON_WIDTH", gametype, version), get_ui_variable("ASSIST_ICON_HEIGHT", gametype, version)) \
            for chara in ASSIST_CHARACTER_LIST}


def get_killfeed_team_color_pos(pos_x, position, gametype, version):
    """Get pixel position from which to get team color from killfeed

    Author:
        Appcell

    Args:
        pox_x: x-axis coordinate of killfeed avatar
        position: on which side the avatar lies, LEFT or OW.RIGHT

    Returns:
        Pos array of this pixel
    """

    if position == LEFT:
        return [get_ui_variable("KILLFEED_TEAM_COLOR_POS_Y", gametype, version), 
                pos_x + get_ui_variable("KILLFEED_TEAM_COLOR_POS_X_LEFT", gametype, version)]
    else:
        return [get_ui_variable("KILLFEED_TEAM_COLOR_POS_Y", gametype, version), 
                pos_x + get_ui_variable("KILLFEED_TEAM_COLOR_POS_X_RIGHT", gametype, version) + get_ui_variable("KILLFEED_ICON_WIDTH", gametype, version)]


def get_killfeed_pos(index, gametype, version):
    """Get position of one killfeed row in one frame, given row index.

    Author:
        Appcell

    Args:
        index: index of killfeed row

    Returns:
        pos array of this killfeed row
    """
    return [math.floor(get_ui_variable("KILLFEED_Y_MIN", gametype, version) + index * get_ui_variable("KILLFEED_GAP", gametype, version)),
            math.floor(get_ui_variable("KILLFEED_HEIGHT", gametype, version)),
            math.floor(get_ui_variable("KILLFEED_X_MIN", gametype, version)),
            math.floor(get_ui_variable("KILLFEED_WIDTH", gametype, version))]


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
    return [math.floor(get_ui_variable("KILLFEED_Y_MIN", gametype, version) + index * get_ui_variable("KILLFEED_GAP", gametype, version) \
                - (get_ui_variable("KILLFEED_GAP", gametype, version) - get_ui_variable("KILLFEED_HEIGHT", gametype, version))/2),
            math.floor(get_ui_variable("KILLFEED_GAP", gametype, version)),
            math.floor(get_ui_variable("KILLFEED_X_MIN", gametype, version)),
            math.floor(get_ui_variable("KILLFEED_WIDTH", gametype, version))]



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
                get_ui_variable("ABILITY_ICON_WIDTH", gametype, version),
                get_ui_variable("ABILITY_ICON_HEIGHT", gametype, version)
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
    return [get_ui_variable("ABILITY_ICON_Y_MIN", gametype, version),
            get_ui_variable("ABILITY_ICON_HEIGHT", gametype, version),
            get_ui_variable("ABILITY_ICON_X_MIN", gametype, version) + pos_right - get_ui_variable("ABILITY_ICON_WIDTH", gametype, version),
            get_ui_variable("ABILITY_ICON_WIDTH", gametype, version) + 5]



def get_assist_icon_pos(pos_x, assist_index, gametype, version):
    return [math.floor(get_ui_variable("ASSIST_ICON_Y_MIN", gametype, version)),
            math.floor(get_ui_variable("ASSIST_ICON_HEIGHT", gametype, version)),
            math.floor(get_ui_variable("ASSIST_ICON_X_OFFSET", gametype, version) + pos_x \
            + assist_index * get_ui_variable("ASSIST_GAP", gametype, version) + get_ui_variable("KILLFEED_ICON_WIDTH", gametype, version)),
            math.floor(get_ui_variable("ASSIST_ICON_WIDTH", gametype, version))]

def get_frame_validation_pos(gametype, version):
    return get_ui_variable("FRAME_VALIDATION_POS", gametype, version)

def get_replay_icon_pos(gametype, version):
    return get_ui_variable("REPLAY_ICON_POS", gametype, version)

def get_replay_icon_preseason_pos(gametype, version):
    return get_ui_variable("REPLAY_ICON_POS_PRESEASON", gametype, version)

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
