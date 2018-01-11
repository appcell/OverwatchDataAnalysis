# ORA (Python) Structure Conventions

If you desire to contribute to ORA or modify ORA code for your own usage, you might need to know about our code.

## Directory & file structure

```
.

|-- src                  # directory of all source codes

|---- __init__.py        # entry point, with version info etc.

|---- core.py            # main process of video analysis, retrieving each frame and analyze with a loop

|---- chara.py           # class Chara

|---- frame.py           # class Frame

|---- gamedata.py        # class GameData

|---- killfeed.py        # class KillFeed

|---- overwatchui.py     # class OverwatchUI
```

## Code structure

Core of ORA(Python) consists of 5 classes: 

`Chara`, `Frame`, `Killfeed`, `OverwatchUI`, `GameData`

### class Chara

Location: `src/chara.py`

Class `Chara` is for storing and retrieving data from topbar. It contains info of ONE player in ONE frame, including:

* Name of player
* Name of character
* Name of the team player belongs to
* Status of ultimate ability (ready or not)
* Status of character (dead or alive)
* Other info which can be extracted from topbar

And corresponding `get`/`set` methods.

### class Killfeed

Location: `src/killfeed.py`

Class `Killfeed` is for storing and retrieving data from killfeed (top-right corner of one frame) in ONE frame. It only contains NEW killfeeds in one frame. For each row, a new `KillfeedRow` object is created, containing:

* Name of eliminator/resurrector character (if exists)
* Name of eliminated/resurrected character
* Name of the team of eliminator character (if exists)
* Name of the team of eliminated character
* List of names of assisting characters (if exists)
* Name of the ability used for elimination (if exists)

And corresponding `get`/`set` methods.

A `Killfeed` object contains 0-6 `KillfeedRow` objects, with methods cutting off the loop of killfeed analysis when required (e.g. when current killfeed row was repeated in previous frame).

### class `Frame`

Location: `src/frame.py`

Class `Frame` is for storing and outputting info in ONE FRAME. A `Frame` object contains:

* 12 Chara objects
* 1 Killfeed object
* A flag indicating if current frame is valid

With get/set methods and another method for writing all info into a GameData object.

### class `GameData`

Location: `src/gamedata.py`

Class `GameData` contains all info retrieved from the video and user input, including:

* Names of both teams
* Names of all 12 players
* Output of all `Frame` objects generated during analysis

And a method for outputting all info to JSON/Excel in file system.

### class `OverwatchUI`

Location: `src/overwatchui.py`

Class `OverwatchUI` contains all UI-related info needed for analysis. It's hard to write the full list down, but in general, it records all pre-set coordinates and reference images of all supported Overwatch UI versions. Also, it has corresponding `get` methods for each piece of UI info ever needed in other classes.