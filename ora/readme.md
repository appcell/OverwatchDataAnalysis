# ORA (Python) Structure Conventions

__If you desire to contribute to ORA or modify ORA code for your own usage, you might need to know about our code.__

__CURRENTLY UNDER CONSTRUCTION!!!___

## Directory & file structure

```
.
|-- ora                  # directory of all source codes
|---- __init__.py        # entry point, with version info etc.
|---- ora.py             # main process of video analysis, retrieves each frame then analyzes with a loop
|---- chara.py           # analyzer for a player bar
|---- frame.py           # analyzer for a frame of the gameplay
|---- killfeed.py        # ananlyzer for a killfeed item
|---- overwatchui.py     # class OverwatchUI
|---- gamedata.py        # class GameData
|---- overwatch.py       # info, data, and classes about the game itself
|---- util.py
|---- main.py            # the test code to analyze a full video
```

## Code structure

### class `CharacterAnalyzer`

Location: `ora/chara.py`

Class `CharacterAnalyzer` is for retrieving data from top player bar.
It retrieves info of ONE player in ONE frame,
and stores the info into a `overwatch.Chara` instance.
The info includes:

* Name of player
* Name of character
* Name of the team player belongs to
* Status of ultimate ability (ready or not)
* Status of character (dead or alive)
* (future work) Ultimate ability charging status
* (future work) Character health point
* Other info which can be extracted from top player bar

---

### class `KillfeedAnalyzer`

Location: `ora/killfeed.py`

Class `KillfeedAnalyzer` is for retrieving data from ONE killfeed (top-right corner of one frame)
 in ONE frame.
 It only contains NEW killfeeds in one frame. For each row,
 a new `overwatch.Killfeed` object is created, which contains:

* Name of eliminator/resurrector character (if exists)
* Name of eliminated/resurrected character
* Name of the team of eliminator character (if exists)
* Name of the team of eliminated character
* List of names of assisting characters (if exists)
* Name of the ability used for elimination (if exists)

A `KillfeedAnalyzer` object contains 0-6 `Killfeed` objects,
with methods cutting off the loop of killfeed analysis when required
(e.g. when current killfeed row was repeated in previous frame).

---

### class `FrameAnalyzer`

Location: `ora/frame.py`

Class `FrameAnalyzer` is for retrieving info in ONE FRAME,
and storing the info into a `overwatch.Frame` instance,
which contains:

* 12 Chara objects
* 0-6 Killfeed object
* A flag indicating if current frame is valid

With get/set methods and another method for writing all info into a GameData object.

---

### class `GameData`

Location: `ora/gamedata.py`

Class `GameData` contains all info retrieved from the video and user input, including:

* Names of both teams
* Names of all 12 players
* Output of all `Frame` objects generated during analysis

And a method for outputting all info to JSON/Excel in file system.

---

### class `OverwatchUI`

Location: `ora/overwatchui.py`

Class `OverwatchUI` contains all UI-related info needed for analysis.
It's hard to write the full list down, but in general,
it records all pre-set coordinates and reference images of all supported Overwatch UI versions.
Also, it has corresponding `get` methods for each piece of UI info ever needed in other classes.
