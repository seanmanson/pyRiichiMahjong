################################################################################
# Copyright (c) 2013, Sean Manson.
# Part of CSSE1001 Major Project (Assignment 3).
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################

""" wall.py:
Contains the definition and functions related to the wall class and how it is
structured and the methods and properties it contains.

"""

#Import major libraries
import random

#Import mahjong libraries
from player import *
from tile import *
from selfio import *
from selfexcept import *
from yaku import *

#Set default globals
DELIMITER = ";"
COMMENTIND = "#"

class Wall(object):
    """ Info structure class.
    Contains the list of all tiles, automatically breaking them down into
    two layers and their dora indicators and the like.
    Basically the wall is counted from the bottom right of the dealer's
    position, starting from the first tile that isn't part of the dead wall.
    The dead wall tiles are the last few tiles in the list.
    Every second tile is skipped over, for the most part.
    Goes clockwise in spite of players going anticlockwise, just to confuse you.
    
    """

    def __init__(self, repeat, suitnum, tileFileLoc, loadData=False):
        """ Create a new wall.
        Constructor: Wall(int, int, string, string)

        repeat is the amount of each individual tile there is in the game.
        suitnum is the amount of numbered suits there are.
        tileFileLoc is the location of the tile infomation file.
        loadData is an optional file location string containing the data that
        this wall should load.
            (Note that if loadData exists, then there is no need to have the
             other values defined properly, as they will just be loaded from
             this file)
        
        """
        if loadData:
            self.loadData(loadData)
        else:
            self._repeat = repeat
            self._suitnum = suitnum
            self._deadStart = 0
            self._deadEnd = 0 #non-inclusive
            self._curPos = 10
            self._doraInd = []
            self._ura = []
            self._tileFileLoc = tileFileLoc
            self.fillWall(tileFileLoc)

    def __getitem__(self, key):
        return self._wall[key]

    def fillWall(self, tileFileLoc):
        """ Loads up the initial tiles in the wall, using self._repeat of each
        defined tile.
    
        fillWall(string) -> None

        tileFileLoc is the location of the tile infomation file.
        
        """
        tileFile = IOHelper(tileFileLoc, DELIMITER, COMMENTIND)
        
        tileInfo = tileFile.getAllRows()
        temp = [Tile(tileFile.concatInt(row[0], row[1])) for row in tileInfo]

        self._uniwall = temp #used for tenpai checking
        self._wall = self._repeat * temp
        random.shuffle(self._wall)

    def saveData(self, saveLocation):
        """ Save all the variables for this Wall into saveLocation. """
        wallFile = open(saveLocation, "w")
        infoStore = []
        infoStore.append('self._repeat')
        infoStore.append('self._suitnum')
        infoStore.append('self._deadStart')
        infoStore.append('self._deadEnd')
        infoStore.append('self._curPos')
        infoStore.append('self._doraInd')
        infoStore.append('self._ura')
        infoStore.append('self._tileFileLoc')
        infoStore.append('self._uniwall')
        infoStore.append('self._wall')
        for info in infoStore:
            wallFile.write(self._getRunnableLine(info))
            wallFile.write('\n')
        wallFile.close()

    def _getRunnableLine(self, varName):
        """ As for _getRunnableLine in gameScreen.py. """
        value = eval(varName)
        value = repr(value)
        return varName + ' = ' + value

    def loadData(self, saveLocation):
        """ Load all the variables for this Wall from saveLocation. """
        wallFile = open(saveLocation, "rU")
        for line in wallFile:
            exec(line)
        wallFile.close()

    def getUnique(self):
        """ Return all unique tiles. """
        return self._uniwall

    def setDealerBreak(self, diedist, breakdist):
        """ Given the distance that the dice roll around the wall, work out
        the start position for the break and the dead wall and get it ready
        to rumble.

        setDealerBreak(int, int) -> None

        diedist is the total of the two die rolled.
        breakdist is how many times the die goes around the wall, starting from
        in front of the user.

        """
        actdist = (4-breakdist)%4 #Flip sides of the break thingo
        self._deadEnd = diedist*2 + actdist*34
        self._curPos = self._deadEnd
        self._deadStart = self._deadEnd-14
        if self._deadStart < 0:
            self._deadStart += len(self._wall)
        self.openDoraInd()

    #DORA RELATED FUNCTIONS
    def openDoraInd(self):
        """ Open up a dora indicator and add it to the lists. """
        doraIndPos = self._deadEnd - 6 - 2*len(self._doraInd)
        self._doraInd.append(doraIndPos)
        self._ura.append(doraIndPos+1)

    def deadWallDraw(self):
        """ Draws a tile from the dead wall, flipping up a new indicator and
        returning this tile, if it can. Returns False if it can't.

        """
        self.openDoraInd()
        if len(self._doraInd) == 2:
            tileToDraw = self._deadEnd-2
        elif len(self._doraInd) == 3:
            tileToDraw = self._deadEnd-1
        elif len(self._doraInd) == 4:
            tileToDraw = self._deadEnd-4
        elif len(self._doraInd) == 5:
            tileToDraw = self._deadEnd-3
        else:
            return False
        tempTile = self._wall[tileToDraw]
        self._wall[tileToDraw] = None
        self._deadStart -= 1
        if self._deadStart < 0:
            self._deadStart += len(self._wall)
        return tempTile

    def indexIsDoraInd(self, index):
        """ Returns True if the given index is a dora indicator, False
        otherwise.

        """
        if index in self._doraInd:
            return True
        else:
            return False
        
    #GETTER FUNCTIONS
    def getDoraList(self):
        """ Returns the list of actual dora. """
        temp = []
        for doraInd in self._doraInd:
            doraIndTile = self._wall[doraInd]
            temp.append(doraIndTile.getNextTile(self._tileFileLoc))
        return temp

    def getUraList(self):
        """ Returns the list of actual ura dora. """
        temp = []
        for doraInd in self._ura:
            doraIndTile = self._wall[doraInd]
            temp.append(doraIndTile.getNextTile(self._tileFileLoc))
        return temp
            
    def getWholeWall(self):
        """ Returns all tiles in the wall.
    
        getWholeWall() -> list
        
        """
        return self._wall

    def getDeadWall(self):
        """ Returns the dead wall, accounting for the final corner. """
        if self._deadStart > self._deadEnd:
            return self._wall[self._deadStart:] + self._wall[:self._deadEnd]
        return self._wall[self._deadStart:self._deadEnd]

    def getDeadStart(self):
        return self._deadStart

    def getDeadEnd(self):
        return self._deadEnd

    def getWallPart(self, side):
        """ Gives the start and end index of each wall part
    
        getWholeWall() -> list

        side refers to 'top', 'bottom' etc.
        
        """
        if side == 'bottom':
            return (0,len(self._wall)/4)
        elif side == 'left':
            return (len(self._wall)/4,len(self._wall)/2)
        elif side == 'top':
            return (len(self._wall)/2,len(self._wall)/2 + len(self._wall)/4)
        elif side == 'right':
            return (len(self._wall)/2 + len(self._wall)/4,len(self._wall))
        else:
            return (False, False)

    def getTilesRemaining(self):
        """ Returns the amount of tiles remaining to draw. """
        if self._deadStart <= self._curPos < self._deadEnd:
            return 0
        elif self._curPos > self._deadStart:
            return self._deadStart + len(self._wall) - self._curPos
        else:
            return self._deadStart - self._curPos

    def indexInDead(self, index):
        """ Returns whether the given index is in the dead wall."""
        if self._deadStart > self._deadEnd:
            return (self._deadStart <= index) or (index < self._deadEnd)
        return self._deadStart <= index < self._deadEnd

    def sideHasDead(self, side):
        """ Returns whether the given side has the dead wall in it. """
        (start, end) = self.getWallPart(side)
        if not start: #If they entered an invalid side.
            return False
        if (start <= self._deadStart < end) or (start <= self._deadEnd < end):
            return True
        else:
            return False

    def drawFromWall(self):
        """ Takes a tile from the wall.
    
        drawFromWall() -> Tile
        
        """
        tempTile = self._wall[self._curPos]
        self._wall[self._curPos] = None
        self._curPos += 1
        if self._curPos >= len(self._wall):
            self._curPos = 0
        return tempTile
