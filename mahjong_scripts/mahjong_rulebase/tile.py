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

""" tile.py:
Contains definitions for 'what is a tile?' as well as those for collections of
multiple tiles (such as for pons or chis excetra).

"""

#Import mahjong libraries
from selfio import *
from selfexcept import *

#Define some global variables
DELIMITER = ";"
COMMENTIND = "#"

class Tile(object):
    """ A general class used for tiles.
    Stores info related to a single tile, ie. suit, name etc.
    Similar to tuples, but with more functions and methods

    """
    
    def __init__(self, a):
        """ Create a new Tile.
        Constructor: Tile(int)
        
        a is a two digit number for suitID, tileID
        
        """
        self._suitID = a/10
        self._tileID = a%10
        self._name = None

    def __str__(self):
        return str(self.getUniqueID())

    def __repr__(self):
        return "Tile(" + self.__str__() + ")"

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.getUniqueID() == other.getUniqueID())

    def __ne__(self, other):
        return not self.__eq__(other)

    def getSuitID(self):
        """ Gets suitID.

        getSuitID() -> int
        
        """
        return self._suitID

    def getTileID(self):
        """ Gets tileID.

        getTileID() -> int
        
        """
        return self._tileID

    def getUniqueID(self):
        """ Gets a unique id.

        getUniqueID() -> int
        
        """
        return int(str(self._suitID) + str(self._tileID))

    def getName(self):
        """ Returns the name of this tile.

        getName() -> string
        
        """
        return self._name

    def getNextTile(self, tileFile):
        """ Given the file with the list of tiles, finds the next logical tile
        in the suit after this one, looping around to the first tile if there
        is none.

        """
        newSuitID = self._suitID
        newTileID = self._tileID + 1
        tileSearcher = IOHelper(tileFile, DELIMITER, COMMENTIND)
        tileExists = (tileSearcher.getRowByTwoID(newSuitID, newTileID))
        if not tileExists:
            newTileID = 1
        uniqueID = int(str(newSuitID) + str(newTileID))
        return Tile(uniqueID)
        

    def setName(self, name):
        """ Set the name of this tile.

        setName(string) -> None
        
        """
        self._name = name

    def loadName(self, tileFile):
        """ Sets the name for the given tile info from the given info file.

        loadName(self, string) -> None
        
        """
        loadName = IOHelper(tileFile, DELIMITER, COMMENTIND)
        tempName = (loadName.getRowByTwoID(self._suitID, self._tileID))
        if tempName:
            self._name = tempName[2]
        else:
            self._name = "Unknown"

    def isHonour(self, suitNum):
        """ Returns whether the tile is an honour tile or not.

        isHonour(int) -> Boolean

        suitNum is the number of numbered suits in the game.

        """
        return (self._suitID > suitNum)

    def isTerminal(self, suitNum):
        """ Returns whether the tile is a terminal tile or not.

        isTerminal(int) -> Boolean

        suitNum is the number of numbered suits in the game.
        
        """
        return ((self._tileID == 1) or (self._tileID == 9)) and self._suitID <= suitNum

    def isSpecial(self, suitNum):
        """ Returns whether the tile is a honour/terminal tile or not.

        isTerminal(int) -> Boolean

        suitNum is the number of numbered suits in the game.
        
        """
        return (self.isHonour(suitNum)) or (self.isTerminal(suitNum))

class TileCollection(object):
    """ A general class used for melds.
    Stores info about pons, chis, kans etc.
    An extended list, essentially.

    """
    def __init__(self, setType, tileMain, side):
        """ Creates a new TileCollection.
        Constructor: TileCollection(string, list, int)

        setType refers to 'pon', 'chi', 'kan_ex' or 'kan_int', as well as a
        'pair' type, used for calculations.
        tileMain refers to the major tile in the set.
            Self-explanatory for pon/kan/pair.
            For chi, is the first tile.
        side refers to which tile is horizontal, 0, 1 or 2.
            Irrelevant for pair and closed kans.
            -1 is used for internal hands
            
        """
        self._setType = setType
        self._tileMain = tileMain
        self._side = side

    def __str__(self):
        return (repr(self._setType) + ',' + repr(self._tileMain) + ',' +
            repr(self._side))

    def __repr__(self):
        return "TileCollection(" + self.__str__() + ")"

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.getMainTile() == other.getMainTile() and
                self.getType() == other.getType())

    def __ne__(self, other):
        return not self.__eq__(other)

    def getType(self):
        return self._setType

    def getMainTile(self):
        return self._tileMain

    def getSide(self):
        return self._side

    def getTileList(self):
        """ Returns a list of the 3 or 4 tiles in the collection.

        getTileList() -> list
        
        """
        temp = []
        if self._setType == 'chi':
            getID = self._tileMain.getUniqueID()
            temp.append(self._tileMain)
            temp.append(Tile(getID+1))
            temp.append(Tile(getID+2))
        elif self._setType == 'pon':
            temp.append(self._tileMain)
            temp.append(self._tileMain)
            temp.append(self._tileMain)
        elif self._setType == 'pair':
            temp.append(self._tileMain)
            temp.append(self._tileMain)
        else:
            temp.append(self._tileMain)
            temp.append(self._tileMain)
            temp.append(self._tileMain)
            temp.append(self._tileMain)
        return temp

    def setType(self, typeToSet):
        """ Set the type to the given new type. """
        self._setType = typeToSet

    def setSuit(self, suitID):
        """ Changes the suit of this tileCollection to the given ID.

        setSuit(int) -> None
        
        """
        curID = self._tileMain.getTileID()
        self._tileMain = Tile(int(str(suitID)+str(curID)))

    def getSuitID(self):
        """ Get the suit of the tiles in this collection. """
        return self._tileMain.getSuitID()

    def getAmtSideways(self):
        """ Get the amount of tiles that are sideways. """
        if self._side == -1:
            return 0
        else:
            return 1

    def getAmtUpways(self):
        """ Get the amount of tiles that are upright. """
        if self._setType[:3] == 'kan':
            return 4 - self.getAmtSideways()
        else:
            return 3 - self.getAmtSideways()

    def getTextRepresentation(self):
        """ Return a textual representation of this tilecollection, used for
        testing and debug purposes.

        """
        s = "("
        if self._setType == 'pon':
            s += "Pon: "
            for x in range(3):
                s += str(self._tileMain)
                if x == self._side:
                    s += "(h)"
                if x != 2:
                    s += ","
        elif self._setType == 'chi':
            getID = self._tileMain.getUniqueID()
            s += "Chi: "
            for x in range(3):
                s += str(Tile(getID+x))
                if x == self._side:
                    s += "(h)"
                if x != 2:
                    s += ","
        elif self._setType == 'kan_op':
            s += "Open Kan: "
            for x in range(4):
                s += str(self._tileMain)
                if x == self._side:
                    s += "(h)"
                if x != 3:
                    s += ","
        elif self._setType == 'kan_cl':
            s += "Closed Kan: "
            s += str(self._tileMain)
            s += ","
            s += str(self._tileMain)
            s += "(f)"
            s += ","
            s += str(self._tileMain)
            s += "(f)"
            s += ","
            s += str(self._tileMain)
        elif self._setType == 'pair':
            s += "Pair: "
            s += str(self._tileMain)
            s += ","
            s += str(self._tileMain)
        return s + ")"
