# ORA (Python) Developer's Guide

__If you desire to contribute to or modify ORA code for your own usage, please read this before any further development.__

__CURRENTLY UNDER CONSTRUCTION!!!___


## Code style

ORA code follows [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) combined with PEP8 standard. 

For development, usage of [Pylint](https://www.pylint.org/) is recommended but not mandatory.

Notice: Author of any code pieces should be specified _IN FUNCTION COMMENTS_, not at the head of a file.

## Directory & file structure

```
.
|-- main.py              # entry point of ORA with GUI
|-- ora/                 # directory of all source codes
|---- __init__.py        # meta info of ORA package, with version info etc.
|---- frame.py           # class Frame, info retriever of one given frame
|---- game.py            # class Game
|---- gui.py             # gui
|---- killfeed.py        # class Killfeed, info retriever of a killfeed item
|---- overwatch.py       # info and fixed data about the game itself
|---- player.py          # class Player, info retriever from players bar
|---- utils/             # utilities used in other .py codes
|------ image.py         # image related util funcs
|------ video_loader.py  # video loader & frame extractor
|---- excel/             # code for outputting to Excel
```

## Code structure conventions

### class `Player`

Location: `ora/player.py`

Class `Player` is for retrieving data from top players bar.
It retrieves and stores info of ONE player in ONE frame, and stores in the `Player` instance itself.
 Info includes:

* Name of player
* Name of character
* Name of the team player belongs to
* Status of ultimate ability (ready or not)
* Status of character (dead or alive)
* (future work) Ultimate ability charging status
* (future work) Character health point
* Other info extractable from top player bar

For details, see comments in `ora/player.py`.

---

### class `Killfeed`

Location: `ora/killfeed.py`

Class `Killfeed` is for retrieving data from ONE killfeed row (top-right corner of one frame)
 in ONE frame.
 It contains only one _NEW_ killfeed row in one frame. Each `Killfeed` instance contains:

* Name of eliminator/resurrector character (if exists)
* Name of eliminated/resurrected character
* Name of the team of eliminator character (if exists)
* Name of the team of eliminated character
* List of assisting characters with name of player & name of team(if exists)
* Name of the ability used for elimination (if exists)

---

### class `Frame`

Location: `ora/frame.py`

Class `Frame` is for retrieving and storing info in ONE FRAME. Info contains:

* 12 Player objects (stored in `self.players`)
* 0-6 Killfeed object (stored in `self.killfeeds`)
* A flag `self.is_valid` indicating if current frame is valid

---

### class `Game`

Location: `ora/game.py`

Class `Game` contains all info retrieved from ONE video, including:

* Names of both teams
* Names of all 12 players
* A list of all `Frame` instances generated during analysis

And a method for outputting all info with JSON/Excel formatting to file system.

---

### class `OW`

Location: `ora/overwatch.py`

Class `OW` contains all UI-related info needed for analysis.
It's hard to write the full list down, but in general,
it records all pre-set coordinates and reference images of all supported Overwatch UI versions.
Also, it has corresponding `get` methods for each piece of UI info ever needed in other classes.
