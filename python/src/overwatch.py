"""
@Author: Xiaochen (leavebody) Li 
"""
import image

#: A list of all characters in overwatch.
CHARACTER_LIST = ["ana", "bastion", "doomfist", "dva", "genji", "hanzo", "junkrat",
                  "lucio", "mccree", "mei", "mercy", "moira", "orisa", "pharah",
                  "reaper", "reinhardt", "roadhog", "soldier76", "sombra",
                  "symmetra", "torbjon", "tracer", "widowmaker", "winston", "zarya",
                  "zenyatta"]
#: A list of all non-character objects in the killfeed.
NON_CHARACTER_OBJECT_LIST = ["riptire", "meka", "shield", "supercharger", "teleporter", "turret"]

#: All possible object in the killfeed.
KILLFEED_OBJECT_LIST = CHARACTER_LIST + NON_CHARACTER_OBJECT_LIST

#: The dictionary that maps the name of object to its image in killfeed.
ICON_KILLFEED_DICT = {obj: image.read_img("./../../images/icons/" + obj + ".png") for obj in KILLFEED_OBJECT_LIST}


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
