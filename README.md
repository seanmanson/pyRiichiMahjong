pyRiichiMahjong
===============

*Note:* The code in this repository was created for my 2013
CSSE1001 course for UQ, created as my major project for the
last assignment. It has not been altered since then. I was a
novice programmer at the time, and so the approach I took is
not representative of my ability at this point in time.



Installation
------------

This game does not require any prior installation on the
behalf of the user before running. Simply extract the zip
file to any location you wish, ensuring that you keep the
original directory structure intact.


Requirements, Libraries and Compatibility
-----------------------------------------

This program was developed using an official build of 
python 2.7.3 on 64-bit Windows 7, along with the following
set of external libraries:

  -  pygame-1.9.2
  -  PIL-1.1.7

The latest builds and releases of pygame can be found at:
   http://www.pygame.org/
and PIL at:
   http://www.pythonware.com/products/pil/

As a requirement, this program MUST have pygame and PIL,
though it may not neccessarily require these specific
versions of these libraries. Compatibility with older and
newer versions of python and these libraries has NOT been
tested, however, so attempt it at your own risk.


Running the Game
----------------

To run the program, simply execute the file 'main.pyw' in 
the root directory of the game, taking care to leave all 
resources and other python modules in their associated 
directories.

main.pyw does not need to be passed any arguments or
command line options on startup.

Note that many of the submodules for this program are
constructed using relative paths, and so attempting to run
this game from an outside directory will result in errors
when the program is unable to find the required files. To
avoid this, please change directories into the root game
directory before execution if running the game from the
command line.


Uninstallation
--------------

To delete this game, merely delete the folder extracted
from the zip file containing the game. This program does 
not create or keep any files outside of its root directory
and subdirectories, so this will remove all traces of the
game from your system.


Help? What is this? What's a 'riichi'?
--------------------------------------

If you're completely new to the world of competitive
mahjong, I recommend that you take a look at some official
documentation and guides as to how the game plays and to
immerse yourself into the rules before jumping right in
and playing around. A good guide to how to play can be
found online at:
   http://www.japanesemahjong.com/

There are several other ports of this form of mahjong, in
several different mediums. A model flash version for this
program can be found at:
   http://www.gamedesign.jp/flash/mahjong/mahjong_e.html


Save Game Notes
---------------

The save directory for this program is under:
   ./resources/savefolder/
All of the files contained in it are necessary.
This game only has one save slot for the last game saved.
If you wish to keep your saves and 'savescum', so to
speak, you are free to do so by copying the save directory
to an external location, and replacing them when
necessary. Note, however, that you MUST leave the save
folder where it is otherwise the game will act irregularly
when attempting to save.


Config File Notes
-----------------

There are two means through which users may make changes to the
base settings of this game. 

The first of these is to edit the config files located at:
   ./resources/[FILENAME].txt
Each of these config files can be edited to change settings in
the game. For example, new yaku can be defined by adding new lines
to yaku.txt. It should be noted, however, that some changes may
require internal methods to be changed to accommodate for them.
This is usually the case if we change the amount of tiles per
hand or alter the amount of tiles in the wall, which would require
an internal change of the rules to work.

The second is through editing global variables located in:
   ./mahjong_scripts/mahjongGlobals.py
These variables tend to be less flexible for editing, though you
can change some of them freely, such as those refering to image
locations and the like.


Mahjong Package Notes
---------------------

There is a mahjong package contained in this game release under:
   ./mahjong_scripts/mahjong_rulebase/
All of the modules and classes contained in this package do NOT
require any of the other files outside of it, and can be used
separately. Classes included here vary from helper classes for
loading from config files, to definitions of what a Player or a
Tile actually is, which is very useful if you want to make your
own programs related to mahjong. Because this package is
independent, you are free to copy it out of here and use in your
own programs with no consequence.