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

""" player.py:
Contains the definition of the Player class, and the methods associated with
dealing with tiles and mutability.

"""

#Import major libraries
import math
import copy

#Import mahjong libraries
from selfio import *
from wall import *
from tile import *
from yaku import *


class Player(object):
    """ Stores info and functions related to a player's hand, except for
    gameplay stats. In other words, has lists of tiles, sorting, kan info etc,
    but no score-based functions.

    'mutable' refers to non-called, discardable tiles (ie. those not in kans
    etc), while 'immutable' is the list of TileCollections containing these
    tiles.

    """
    def __init__(self, handsize, suitnum, totalsuitnum, name):
        """ A general class used for player hands.
        Constructor: Player(int, int, int, string)

        handsize refers to maximum hand size.
        suitnum refers to the amount of numbered suits.
        totalsuitnum refers to the total number of suits, including honours.
        score refers to the player's current score.
        name is the player's name.

        """
        self._mutable = []
        self._immutable = []
        self._discardPile = []
        self._handsize = handsize
        self._suitnum = suitnum
        self._totalsuitnum = totalsuitnum
        self._name = name
        self._closed = True

    def __str__(self):
        return (self._name + ', ' + str(self._mutable) + ', ' +
            str(self._immutable))
        
    def __repr__(self):
        return 'Player(' + self.__str__() + ')'

    def resetPlayer(self):
        """ Sets the tiles in the player's hand back to the defaults. """
        self._mutable = []
        self._immutable = []
        self._discardPile = []
        self._closed = True

    def returnTiles(self):
        """ Returns a list of all tiles in the hand.

        returnTiles() -> list
        
        """
        temp = list(self._mutable)
        for item in self._immutable:
            temp += item.getTileList()
        return temp

    def sort(self):
        """ Sorts the tiles in readable order by suit then tile number.
        Requires a special function to avoid just going alphabetically.

        sort() -> None

        """
        self._mutable.sort(key = lambda x: x.getUniqueID())

    def count(self):
        """ Returns a dictionary count of the amounts of each tile.

        count() -> dict
        
        """
        num = {}
        for x in self._mutable:
            num[x] = num.get(x, 0) + 1
        return num

    def countTile(self, tile):
        """ Returns a count of how many of the given tile there are.

        countTile(Tile) -> int
        
        """
        count = self._mutable.count(tile)
        for item in self._immutable:
            count += item.getTileList().count(tile)
        return count

    def countID(self, tile):
        """ Returns a count of how many tiles of the given ID there are.

        countID(int) -> int
        
        """
        if tile < 10:
            return 0
        else:
            searchTile = Tile(tile)
            return self.countTile(searchTile)

    def countMutID(self, tile):
        """ Returns a count of how many tiles of the given ID there are in the
        mutable potion of the hand

        countID(int) -> int
        
        """
        if tile < 10:
            return 0
        else:
            searchTile = Tile(tile)
            return self._mutable.count(searchTile)

    def countDiscardPile(self):
        """ Returns the amount of tiles in the discard pile. """
        return len(self._discardPile)

    def countSuitTiles(self, suitID):
        """ Returns a count of how many tiles there are in the given suitID.

        countSuitTiles(int) -> int
        
        """
        count = 0
        for tile in self._mutable:
            if tile.getSuitID() == suitID:
                count += 1
        for tileColl in self._immutable:
            if tileColl.getSuitID() == suitID:
                count += 1
        return count

    def getName(self):
        return self._name

    def getMutable(self):
        return self._mutable

    def getImmutable(self):
        return self._immutable

    def getDiscardPile(self):
        return self._discardPile

    def getHandsize(self):
        return self._handsize

    def getTileNum(self):
        """ Returns how many tiles are in the hand.
        Counts kans as threes.

        getTileNum() -> int
        
        """
        return len(self._mutable) + 3*len(self._immutable)

    def getIndexFromTile(self, tile):
        """ Returns a tuple containing all indicies in _mutable for tile.

        getIndexFromTile(Tile) -> tuple
        
        """
        ind = []
        for i, x in enumerate(self._mutable):
            if x == tile:
                ind.append(i)
        return tuple(ind)

    def getFirstIndexFromID(self, tileID):
        """ Returns the first index of a tile given the tile's id.
        Returns -1 if not found.

        getFirstIndexFromID(int) -> int
        
        """
        ind = -1
        curTile = Tile(tileID)
        for i, x in enumerate(self._mutable):
            if x == curTile:
                ind = i
                break
        return ind

    def getTileFromIndex(self, index):
        """ Returns a Tile given the index of it in _mutable

        getTileFromIndex(int) -> Tile
        
        """
        return self._mutable[index]

    def getTileCollection(self, collectType, mainTile):
        """ Returns the first TileCollection in _immutable, given a type and
        main tile.
        Returns False otherwise.
    
        getTileCollectionIndex(string, Tile) -> int

        """
        for item in self._immutable:
            if item.getMainTile() == mainTile and item.getType() == collectType:
                return item
        return False

    def getTileCollectionIndex(self, collectType, mainTile):
        """ Returns the index of the first TileCollection in _immutable, given
        a type and main tile.
        Returns False otherwise.
    
        getTileCollectionIndex(string, Tile) -> int
        
        """
        for i, item in enumerate(self._immutable):
            if item.getMainTile() == mainTile and item.getType() == collectType:
                return i
        return False

    def loadTileNames(self, settingsFile):
        """ Looks up and loads the names for all tiles in the hand from
        the given settingsFile.

        loadTileNames(Settings) -> None
        
        """
        for item in self._mutable:
            item.setName(settingsFile.getTileName(item))

    def draw(self, tile):
        """ Adds the given tile to the end of the hand.

        draw(Tile) -> None
        
        """
        if self.getTileNum() < self._handsize:
            self.sort()
            self._mutable.append(tile)
        else:
            raise GameRunningException('Too many tiles in hand.')

    def discard(self, tilepos=-1):
        """ Discards the tile at index tilepos from the hand.
        If tilepos is not specified, discards the last tile.
        Returns the discarded tile.

        discard(int) -> Tile
        
        """
        if len(self._mutable) > 0:
            tempTile = self._mutable.pop(tilepos)
            self._discardPile.append(tempTile)
            self.sort()
            return tempTile
        else:
            raise GameRunningException('No tiles to discard')

    def removeDiscard(self):
        """ Deletes the last tile in the discard pile. """
        self._discardPile.pop()

    def reset(self):
        """ Resets the hand back to its default state.

        reset() -> None

        """
        if len(self._mutable) > 0:
            return self._mutable.pop(tilepos)
        else:
            raise GameRunningException('No tiles to discard')

    def canPon(self, tile):
        """ Checks to see if a three of a kind is possible with the given tile.

        canPon(Tile) -> Boolean
        
        """
        numInHand = self._mutable.count(tile)
        if numInHand > 1 and numInHand < 5:
            return True
        else:
            return False

    def pon(self, tile, side):
        """ Makes a three of a kind of the given tile from a discarded tile.
        Places these tiles as a TileCollection into _immutable.
        Naturally, requires there to be two of a kind already in the hand.

        pon(Tile, int) -> None

        side refers to which tile is horizontal, 0, 1 or 2.
        
        """
        if self.canPon(tile):
            self._immutable.append(TileCollection('pon', tile, side))
            self._mutable.remove(tile)
            self._mutable.remove(tile)
            self._closed = False
        else:
            raise GameRunningException('Incorrect Pon Attempt')

    def canChi(self, tile):
        """ Checks to see if a three straight is possible with the given tile.
        Returns a list of 2-tuples with the relevant positions of the other two
        tiles in the hand.

        canChi(Tile) -> list of 2-tuples
        
        """
        temp = []
        curID = tile.getUniqueID()
        if (tile.isHonour(self._suitnum)):
            return temp
        if (self.countMutID(curID + 1)) and (self.countMutID(curID + 2)):
            tile1Ind = self.getFirstIndexFromID(curID + 1)
            tile2Ind = self.getFirstIndexFromID(curID + 2)
            temp.append((tile1Ind, tile2Ind))
        if (self.countMutID(curID - 1)) and (self.countMutID(curID + 1)):
            tile1Ind = self.getFirstIndexFromID(curID - 1)
            tile2Ind = self.getFirstIndexFromID(curID + 1)
            temp.append((tile1Ind, tile2Ind))
        if (self.countMutID(curID - 2)) and (self.countMutID(curID - 1)):
            tile1Ind = self.getFirstIndexFromID(curID - 2)
            tile2Ind = self.getFirstIndexFromID(curID - 1)
            temp.append((tile1Ind, tile2Ind))
        return temp
                

    def chi(self, tile, otherTwo):
        """ Makes a straight of three using the given tile.
        Places these tiles as a TileCollection into _immutable.

        chi(Tile, 2-tuple) -> None
        
        otherTwo refers to a 2-tuple with the indicies of the other tiles
        in the hand, usually found with canChi() above
        
        """
        if self.canChi(tile):
            #Find the actual other tiles
            other0 = self.getTileFromIndex(otherTwo[0])
            other1 = self.getTileFromIndex(otherTwo[1])
            #Find the lowest tile, get the side that the stolen tile is on
            tileList = [tile, other0, other1]
            tileList.sort(key = lambda x: x.getUniqueID())
            side = tileList.index(tile)
            #Make the tile collection
            self._immutable.append(TileCollection('chi', tileList[0], side))
            #Remove the other two from the hand
            self._mutable.remove(other0)
            self._mutable.remove(other1)
            self._closed = False
        else:
            raise GameRunningException('Incorrect Chi Attempt')

    def canKan(self, tile): #I love that name
        """ Checks to see if a four of a kind is possible with the given tile.

        canKan(Tile) -> Boolean
        
        """
        numInHand = self._mutable.count(tile)
        if numInHand == 3:
            return True
        else:
            return False

    def kan_op(self, tile, side):
        """ Makes a four of a kind of the given tile from a discarded tile.
        Places these tiles as a TileCollection into _immutable.
        Naturally, requires there to be three of a kind already in the hand.
            (Note that there should be a dead wall draw straight after this)
            
        kan_op(Tile) -> None
        
        side refers to which tile is horizontal, 0, 1 or 2.
        
        """
        if self.canKan(tile):
            self._immutable.append(TileCollection('kan_op', tile, side))
            self._mutable.remove(tile)
            self._mutable.remove(tile)
            self._mutable.remove(tile)
            self._closed = False
        else:
            raise GameRunningException('Incorrect Open Kan Attempt')

    def canKan_cl(self):
        """ Checks to see if a four of a kind is in your hand.
        Returns the tile that works for it, or False otherwise.

        canKan_cl() -> Tile or False
        
        """
        for tile in self._mutable:
            if self._mutable.count(tile) == 4:
                return tile
        return False

    def kan_cl(self):
        """ Declares a four of a kind from your hand.
        Places these tiles as a TileCollection into _immutable.
        Naturally, requires there to be four of a kind in the hand.
            (Note that there should be a dead wall draw straight after this)

        kan_ex() -> None
        
        """
        testTile = self.canKan_cl()
        if testTile:
            self._immutable.append(TileCollection('kan_cl', testTile, -1))
                #side is irrelevant in this case
            self._mutable.remove(testTile)
            self._mutable.remove(testTile)
            self._mutable.remove(testTile)
            self._mutable.remove(testTile)
        else:
            raise GameRunningException('Incorrect Closed Kan Attempt')

    def canKan_la(self):
        """ Checks to see if a three of a kind is already declared in the hand,
        as well as to whether there is another tile for this in your hand.
        Returns the first such tile.

        canKan_la() -> Boolean
        
        """
        for tile in self._mutable:
            if self.getTileCollection('pon', tile):
                return tile
        return False

    def kan_la(self):
        """ Makes a four of a kind using an already declared pon.
        Removes this pon and the tile from the hand.
        Requires there to be said tile and pon already existing.

        kan_la() -> None
        
        """
        testTile = self.canKan_la()
        if testTile:
            temp = self.getTileCollection('pon', testTile)
            self._immutable.append(TileCollection('kan_op', testTile,
                temp.getSide()))
            self._immutable.remove(temp)
            self._mutable.remove(testTile)
        else:
            raise GameRunningException('Incorrect Late Kan Attempt')

    def isValid(self):
        """ Checks to see whether the hand is a valid, scoring hand.
        This is hard-coded, based off the official riichi mahjong rules.
        Quite extensive.
        Returns a list of tile collections pertaining to the correct arrangement
        of pons/chis in the mutable part of the hand.
        Returns [] if the hand is not valid.
        Returns -1 if the hand is a unique style of hand:
            (i.e, 1 of each end, or 7 pairs.)

        isValid() -> object
        
        """
        if self.getTileNum() < self._handsize: #hand must be full
            return []
        if self.isSpecialHand(): #if the hand is a unique hand
            return -1
        
        tempMutable = sorted(self._mutable, key = lambda x: x.getUniqueID())
        finalArrange = []
        count = 0
        for setItem in self.splitSuits(tempMutable): #Find the arrangements
            if setItem:
                if count > 1: #more than one pair in the splits -> invalid
                    return []
                if setItem[0].isHonour(self._suitnum): #If it is an honour tile
                    numberList = self.countNumbers(setItem)
                    tileCount = -1
                    for number in numberList:
                        tileCount += number
                        curTile = setItem[tileCount]
                        if number == 2:
                            finalArrange.append(TileCollection('pair', curTile,
                                -1))
                            count += 1
                        elif number == 3:
                            finalArrange.append(TileCollection('pon', curTile,
                                -1))
                        else:
                            return []
                elif len(setItem)%3 == 2: #Has a pair
                    count += 1
                    curArrange = self.getValidArrangePair(setItem)
                    if not curArrange: #Check if the arrangements are correct
                        return []
                    else:
                        finalArrange += curArrange #Add them to the list
                elif len(setItem)%3 == 0: #Has no pair
                    curArrange = self.getValidArrange(setItem)
                    if not curArrange:
                        return []
                    else:
                        finalArrange += curArrange
                else: #Invalid if they have a number of tiles not div. by 3.
                    return []
        return finalArrange

    def splitSuits(self, tempList):
        """ Splits the given list of tiles up into a list of lists each
        containing individual suits of tiles.

        splitSuits(list) -> list of lists
        
        """
        temp = []
        for x in range(self._totalsuitnum):
            temp.append([])
        for tile in tempList:
            temp[tile.getSuitID() - 1].append(tile)
        return temp

    def countNumbers(self, tempList):
        """ Returns a count of all tiles as a list, index given by what 'order'
        they are in the list.

        countNumbers(list) -> list of integers
        
        """
        cur = None
        num = 0
        temp = []
        for tile in tempList:
            if cur == tile:
                temp[len(temp) - 1] += 1
            else:
                temp.append(1)
                cur = tile
        return temp

    def getValidArrange(self, tileSet):
        """ Given a list of tiles (multiple of three), returns the valid
        arrangements.
        Does not take pairs into account.

        getValidArrange(list) -> list of TileCollections
        
        """
        tileSet.sort(key = lambda x: x.getUniqueID())
        poss = []
        if len(tileSet)%3 == 0:
            while True:
                prevSet = list(tileSet)
                tile = tileSet[0]
                curID = tile.getUniqueID()
                curCount = tileSet.count(tile)
                if curCount != 3:
                    if (tileSet.count(Tile(curID+1)) and tileSet.count(Tile(curID+2))):
                        poss.append(TileCollection('chi', tile, -1))
                        tileSet.remove(tile)
                        tileSet.remove(Tile(curID+1))
                        tileSet.remove(Tile(curID+2))
                if curCount >= 3:
                    poss.append(TileCollection('pon', tile, -1))
                    tileSet.remove(tile)
                    tileSet.remove(tile)
                    tileSet.remove(tile)
                if tileSet == prevSet:
                    return []
                elif len(tileSet) == 0:
                    return poss
        return []

    def getValidArrangePair(self, tileSet):
        """ Given a list of tiles (multiple of three), returns the valid
        arrangements.
        Assumes there is one pair

        getValidArrange(list) -> list of list of TileCollections
        
        """
        tileSet.sort(key = lambda x: x.getUniqueID())
        poss = []
        if len(tileSet)%3 == 2:
            counter = 0
            while counter < len(tileSet):
                curCount = tileSet.count(tileSet[counter])
                if curCount > 1:
                    copySet = list(tileSet)
                    copySet.remove(tileSet[counter])
                    copySet.remove(tileSet[counter])
                    if len(copySet) == 0:
                        return [TileCollection('pair', tileSet[counter], -1)]
                    else:
                        curArrange = self.getValidArrange(copySet)
                        if curArrange:
                            curArrange.append(TileCollection('pair',
                                tileSet[counter], -1))
                            return curArrange
                counter += curCount
        return []

    def isSpecialHand(self):
        """ Whether or not the hand is a unique hand.
        This function exists for special hands which may be used in subclasses
        to this one.
        
        """
        return False

    def isClosed(self):
        """ Is the hand closed? """
        return self._closed

    def isTenpai(self, listOfTiles):
        """ Checks to see whether the hand is one tile away from being valid.
        Requires a hand with handsize-1 tiles.

        isTenpai(list of Tiles) -> Boolean

        listOfTiles is the list of all tiles it should look through for
        possibilities.
        
        """
        if self.getTileNum() < self._handsize - 1: #hand must be full
            return False
        for tile in listOfTiles:
            self._mutable.append(tile)
            if self.isValid():
                self._mutable.pop()
                return True
            self._mutable.pop()
        return False

    def isTenpaiFull(self, listOfTiles):
        """ Checks to see whether the hand is one tile away from being valid,
        by seeing what happens when tiles are discarded.
        Requires a hand with handsize tiles.

        isTenpaiFull(list of Tiles) -> Boolean

        listOfTiles is the list of all tiles it should look through for
        possibilities.

        """
        if self.getTileNum() < self._handsize: #hand must be full
            return False
        tempMutable = copy.deepcopy(self._mutable)
        for x in range(len(tempMutable)):
            self._mutable.pop(x)
            if self.isTenpai(listOfTiles):
                self._mutable = copy.deepcopy(tempMutable)
                return True
            self._mutable = copy.deepcopy(tempMutable)
        return False

    def isTenpaiPoss(self, listOfTiles):
        """ Checks to see whether the hand is one tile away from being valid.
        Requires a hand with handsize-1 tiles.
        Returns a list of all possible correct tiles.

        isTenpaiPoss(list of Tiles) -> Boolean
    
        listOfTiles is the list of all tiles it should look through for
        possibilities.

        """
        poss = []
        for tile in listOfTiles:
            self._mutable.append(tile)
            if self.isValid():
                poss.append(tile)
            self._mutable.pop()
        return poss

    def isTenpaiFullPoss(self, listOfTiles):
        """ Checks to see whether the hand is one tile away from being valid,
        by seeing what happens when tiles are discarded.
        Returns all possible indexes that allow this, in a list.
        Requires a hand with handsize tiles.

        isTenpaiFullPoss(list of Tiles) -> list
        
        listOfTiles is the list of all tiles it should look through for
        possibilities.

        """
        poss = []
        tempMutable = copy.deepcopy(self._mutable)
        for x in range(len(tempMutable)):
            self._mutable.pop(x)
            if self.isTenpai(listOfTiles):
                poss.append(x)
            self._mutable = copy.deepcopy(tempMutable)
        return poss
