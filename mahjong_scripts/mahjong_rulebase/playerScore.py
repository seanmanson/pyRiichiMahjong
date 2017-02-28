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

""" playerScore.py:
Contains PlayerScore, a subclass of Player with extra functionality, such as
detecting yaku and scoring hands. This is central to the way the game works.

"""

#Import major libraries
import math

#Import mahjong libraries
from player import *
from selfio import *
from wall import *
from tile import *
from yaku import *

#Misc. global variables
GREENTILES = [Tile(41), Tile(12), Tile(13), Tile(14), Tile(16), Tile(18)]

class PlayerScore(Player):
    """ Extension of the Player class, containing functions and attributes
    relating to the current player's score and state of the game.
    This is done to make the scoring portion of the game more modular.
    
    """
    def __init__(self, handsize, suitnum, totalsuitnum, name, score,
                 seatWind=Tile(51), loadData=False):
        """ Creates a new PlayerScore.
        Constructor: PlayerScore(int, int, string, int, Tile, object)
        
        handsize refers to maximum hand size.
        suitnum refers to the amount of numbered suits.
        totalsuitnum refers to the total number of suits, including honours.
        name is the player's name.
        score refers to the player's current score.
        seatWind is a tile representing the current seating, North by default.
        loadData is an optional file location string containing the data that
        this player should load.
            (Note that if loadData exists, then there is no need to have the
             other values defined properly, as they will just be loaded from
             this file)
            
        """
        if loadData:
            self.loadData(loadData)
            self._scoreDiff = 0
        else:
            Player.__init__(self, handsize, suitnum, totalsuitnum, name)
            self._score = score
            self._scoreDiff = 0
            self._seatWind = seatWind
            self._riichi = False #whether they have currently declared riichi
            self._doubleriichi = False
            self._riichiturns = -1
            self._riichiPos = -1 #Where the sideways tile should be in the discards
            self._riichiWait = [] #The tiles they are waiting for after riichi
                #Used to save time
            self._canTenhou = True
            self._canChiihou = True
            self._showHand = False
            self._amountOfWins = 0

    def __repr__(self):
        return 'PlayerScore(' + self.__str__() + ')'

    def resetPlayer(self):
        """ Resets all values back to their defaults. """
        Player.resetPlayer(self)
        self._riichi = False
        self._doubleriichi = False
        self._riichiturns = -1
        self._riichiPos = -1
        self._riichiWait = []
        self._canTenhou = True
        self._canChiihou = True
        self._showHand = False

    def discard(self, tilepos=-1):
        """ Discards the tile at index tilepos from the hand.
        If tilepos is not specified, discards the last tile.
        Returns the discarded tile.
        Sets the correct flags for Tenhou and Chihou yakuman.

        discard(int) -> Tile
        
        """
        self._canTenhou = False
        self._canChiihou = False
        return Player.discard(self, tilepos)

    def setScoreDiff(self, amount):
        """ Sets the current score difference to the given amount. """
        self._scoreDiff = amount

    def setDealer(self, isDealer):
        """ Given whether or not they are dealer, sets the Tenhou/Chiihou flags
        accordingly.

        """
        if isDealer:
            self._canChiihou = False
        else:
            self._canTenhou = False

    def setSeatWind(self, newSeatWind):
        """ Sets the new seat wind for the player. """
        self._seatWind = newSeatWind

    def showHand(self):
        """ Sets whether the player should show their hand. """
        self._showHand = True

    def getSeatWind(self):
        return self._seatWind

    def getScore(self):
        return self._score

    def getScoreDiff(self):
        return self._scoreDiff

    def getAmountOfWins(self):
        return self._amountOfWins

    def getShowHand(self):
        return self._showHand

    def addScore(self, amount):
        """ Instantly adds the given amount of score. """
        self._score += amount

    def updateScoreDiff(self, step):
        """ Updates the score using the known score difference by step amount.
        Returns True if scoreDiff is now 0, otherwise False.

        """
        if self._scoreDiff > 0:
            self._score += step
            self._scoreDiff -= step
            if self._scoreDiff < 0:
                self._score += self._scoreDiff
                self._scoreDiff = 0
            return False
        elif self._scoreDiff < 0:
            self._score -= step
            self._scoreDiff += step
            if self._scoreDiff > 0:
                self._score -= self._scoreDiff
                self._scoreDiff = 0
            return False
        else:
            return True

    def finScoreDiff(self):
        """ Instantly apply the current score difference. """
        self._score += self._scoreDiff

    def addScoreDiff(self, amount):
        """ Add a certain amount to the current score difference. """
        self._scoreDiff += amount

    def riichi(self, listOfTiles, double):
        """ Declares riichi, finding out the wait using listOfTiles.
        double is used to see if this is a double riichi.

        """
        self._riichi = True
        self._score -= 1000 
        self._doubleriichi = double
        self._riichiturns = 0
        self._riichiPos = self.countDiscardPile() - 1
        self._riichiWait = self.isTenpaiPoss(listOfTiles)

    def isRiichi(self):
        """ Are we riichi? """
        return self._riichi

    def addRiichiTurns(self, num):
        """ Add the given amount on to the amount of turns since riichi. """
        self._riichiturns += num
        self._canTenhou = False
        self._canChiihou = False

    def getRiichiWait(self):
        """ Get which tiles we're waiting on. """
        return self._riichiWait

    def addWin(self):
        """ Add one to the amount of wins we have. """
        self._amountOfWins += 1

    def saveData(self, saveLocation):
        """ Save all the variables for this PlayerScore into saveLocation. """
        playerFile = open(saveLocation, "w")
        infoStore = []
        infoStore.append('self._mutable')
        infoStore.append('self._immutable')
        infoStore.append('self._discardPile')
        infoStore.append('self._handsize')
        infoStore.append('self._suitnum')
        infoStore.append('self._totalsuitnum')
        infoStore.append('self._name')
        infoStore.append('self._closed')
        infoStore.append('self._score')
        infoStore.append('self._seatWind')
        infoStore.append('self._riichi')
        infoStore.append('self._doubleriichi')
        infoStore.append('self._riichiturns')
        infoStore.append('self._riichiPos')
        infoStore.append('self._riichiWait')
        infoStore.append('self._canTenhou')
        infoStore.append('self._canChiihou')
        infoStore.append('self._showHand')
        infoStore.append('self._amountOfWins')
        for info in infoStore:
            playerFile.write(self._getRunnableLine(info))
            playerFile.write('\n')
        playerFile.close()

    def _getRunnableLine(self, varName):
        """ As for _getRunnableLine in gameScreen.py. """
        value = eval(varName)
        value = repr(value)
        return varName + ' = ' + value

    def loadData(self, saveLocation):
        """ Load all the variables for this PlayerScore from saveLocation. """
        playerFile = open(saveLocation, "rU")
        for line in playerFile:
            exec(line)
        playerFile.close()
        

    def isSpecialHand(self):
        """ Used for adding validity exceptions for chiitoitsu and
        kokushi musou hands. """
        if self.isChiitoitsu(): #Check for chiitoitsu
            return True
        if self.isKokushi(): #Check for kokushi
            return True
        return False

    def canTsumo(self, roundWind, yakuFile, gameYakuList):
        """ Can we declare tsumo?

        canTsumo(Tile, string, list) -> None

        roundWind is the tile for the current round wind.
        yakuFile is the file location for the list of yaku information.
        gameYakuList is a list of all applicable gameYaku for this hand.
        
        """
        selfDrawn = True
        curArrange = self.isValid()
        if curArrange:
            if curArrange == -1: #Special hands
                return True
            return self.testYaku(roundWind, curArrange, yakuFile, gameYakuList,
                selfDrawn)
        else:
            return False

    def canRon(self, newTile, roundWind, yakuFile, gameYakuList):
        """ Can we declare ron?
        Requires a hand with handsize-1 tiles.

        canTsumo(Tile, Tile, string, list) -> None

        newTile is the tile to check.
        roundWind is the tile for the current round wind.
        yakuFile is the file location for the list of yaku information.
        gameYakuList is a list of all applicable gameYaku for this hand.
        
        """
        selfDrawn = False
        if newTile == False: #False in the base case
            return False
        if newTile in self._discardPile: #Basic furiten case
            return False
        #If it still works after the above, test it for reals, then bulletproof
        self._mutable.append(newTile)
        curArrange = self.isValid()
        if curArrange:
            self._mutable.pop()
            if not self.testYaku(roundWind, curArrange, yakuFile, gameYakuList,
                    selfDrawn):
                return False
        else:
            self._mutable.pop()
            return False
        for disTile in self._discardPile: #Test all furiten case
            self._mutable.append(disTile)
            if self.isValid():
                self._mutable.pop()
                return False
            self._mutable.pop()
        return True

    def testYaku(self, roundWind, curArrange, yakuFile, gameYakuList,
            selfDrawn):
        """ Given the roundWind, arrangements, yakuFile, gameYakuList and
        whether or not something is selfDrawn, determines whether or not there
        is enough yaku to declare a game won.

        """
        curFu = self.getFu(roundWind, curArrange, selfDrawn)
        curYaku = self.getHandYaku(roundWind, curArrange, curFu, selfDrawn,
            yakuFile)
        curYaku += gameYakuList
        if len(curYaku) < 1:
            return False
        else:
            return True

    def scoreHand(self, currentYaku, currentFu, doraAmount):
        """ Gives the current hand score for the current hand, as well as the
        name for this score, if it is a limit.
        Is not rounded.

        Note that these values are HARDCODED based on official rules.
        Those wishing to write their own variants of this should write their
        own variant of this function.

        scoreHand(Tile) -> tuple(int, string)

        roundWind is a Tile for the current round wind.
            
        """
        if len(currentYaku) < 1: #must have at least one yaku
            return 0
        handClosed = self.isClosed()
            #Whether or not the hand is closed

        currentHan = 2 + doraAmount
        if handClosed:
            for yaku in currentYaku:
                if yaku.getScoreClosed() == -1: #if yakuman
                    currentHan = -1
                    break
                else:
                    currentHan += yaku.getScoreClosed()  
        else:
            for yaku in currentYaku:
                if yaku.getScoreOpen() == -1: #if yakuman
                    currentHan = -1
                    break
                else:
                    currentHan += yaku.getScoreOpen()
        if currentHan == -1: #if yakuman
            curNum = len(currentYaku)
            return (curNum*8000, 'Yakuman')
        else: #if normal hand
            basicPoints = float(currentFu)*2**(currentHan)
            if basicPoints > 2000: #if we pass the limit, just go by han
                if currentHan <= 7:
                    return (2000, 'Mangan')
                elif currentHan <= 9:
                    return (3000, 'Haneman')
                elif currentHan <= 12:
                    return (4000, 'Baiman')
                elif currentHan <= 14:
                    return (6000, 'Sanbaiman')
                else:
                    return (8000, 'Counted Yakuman') #yakuman, woohoo!
            else:
                return (int(basicPoints), None)

    def getRiichiPos(self):
        """ Gets the position of the declared riichi tile. """
        return self._riichiPos

    def getFu(self, roundWind, handArrange, selfDrawn):
        """ Gives the current fu score for the current hand.
        Assumes that the hand is valid.
        Note that these values are HARDCODED based on official rules.
        Those wishing to write their own variants of this should write their
        own variant of this function.

        getFu(Tile, list of TileCollections) -> int

        roundWind is a Tile for the current round wind.
        handArrange is a list of TileCollections which the hand has been broken
        down into, through the use of the isValid() function.
        selfDrawn is a Boolean on whether the last tile was self drawn or taken
        from someone else.
            
        """
        if handArrange == -1:
            return 25 #in case of chiitoitsu, which should always be 25 fu.

        score = 20 #base score is always 20, should NEVER be changed
        lastTile = self._mutable[-1]

        if len(self._immutable) == 0 and not selfDrawn:
            score += 10 #if ron with no called melds, 10 points
        for tileColl in handArrange:
            if tileColl.getType() == 'pair':
                if tileColl.getMainTile() == self._seatWind:
                    score += 2 #bonus for seat wind pair
                if tileColl.getMainTile() == roundWind:
                    score += 2 #bonus for seat wind pair
                if tileColl.getMainTile().getSuitID() == 4:
                    score += 2 #bonus for dragon tiles
                if tileColl.getMainTile() == lastTile:
                    score += 2 #ready score for completing the pair
            elif tileColl.getType() == 'pon':
                temp = 2
                curTile = tileColl.getMainTile()
                if curTile.isSpecial(self._suitnum):
                    temp *= 2 #bonus for special pon
                if tileColl.getSide() == -1:
                    temp *= 2 #bonus for closed pon
                score += temp
            elif tileColl.getType() == 'kan_op':
                curTile = tileColl.getMainTile()
                if curTile.isSpecial(self._suitnum):
                    score += 8
                else:
                    score += 16
            elif tileColl.getType() == 'kan_cl':
                curTile = tileColl.getMainTile()
                if curTile.isSpecial(self._suitnum):
                    score += 16
                else:
                    score += 32
            elif tileColl.getType() == 'chi': #Checking for ready scores
                tile1 = tileColl.getMainTile()
                tile2 = Tile(tile1.getUniqueID() + 1)
                tile3 = Tile(tile1.getUniqueID() + 2)

                if lastTile == tile1:
                    if lastTile.getTileID() == 7:
                        score += 2 #ready score for being on the left edge
                if lastTile == tile3:
                    if lastTile.getTileID() == 3:
                        score += 2 #ready score for being on the right edge
                if lastTile == tile2:
                    score += 2 #ready score for being in the middle
        if selfDrawn:
            if score != 20: #If not pinfu
                score += 2
        if score == 20 and len(self._immutable) != 0: #If the hand is open pinfu
            score += 2

        revScore = float(score)/10 #round up to the nearest 10
        return int(math.ceil(revScore)*10)
        

    def getHandYaku(self, roundWind, currentArrange, currentFu, selfDrawn,
            yakuFile):
        """ Get a list of yaku that apply to the current hand.
        Assumes that the hand is valid.
        Does not take into account non-hand yaku like rinshan kaihou, tsumo etc.

        getYaku(Tile, list of TileCollections, int) -> list of Yaku

        roundWind is a Tile for the current round wind.
        currentArrange is a list of TileCollections which the hand has been
        broken down into, through the use of the isValid() function.
        currentFu is the current amount of fu in the hand.
        selfDrawn is whether the current player drew the last tile
        yakuFile is the location of the info file about the yaku and their
        names.
            
        """
        temp = []

        if currentArrange == []: #if invalid hand, return nothing
            return []
        elif currentArrange != -1:
            currentArrange += self._immutable

        #First, check all the basic yaku
        temp += self.getYakupai(roundWind, yakuFile)
        if self.isClosed() and selfDrawn:
            temp.append(Yaku('tsumo', yakuFile))
        if self._riichi:
            temp.append(Yaku('riichi', yakuFile))
        if self._doubleriichi:
            temp.append(Yaku('riichidb', yakuFile))
        if self._riichiturns < 4 and self._riichi:
            temp.append(Yaku('ippatsu', yakuFile))
        if self.isPinfu(currentFu, selfDrawn):
            temp.append(Yaku('pinfu', yakuFile))
        if self.isTanyao():
            temp.append(Yaku('tanyao', yakuFile))
        if self.isIipeikou(currentArrange):
            temp.append(Yaku('iipeikou', yakuFile))
        if self.isItsuu(currentArrange):
            temp.append(Yaku('itsuu', yakuFile))
        if self.isChanta(currentArrange):
            temp.append(Yaku('chanta', yakuFile))
        if self.isSanshoku(currentArrange):
            temp.append(Yaku('sanshoku', yakuFile))
        if self.isSanshokuAlt(currentArrange):
            temp.append(Yaku('sanshokualt', yakuFile))
        if currentFu == 25:
            temp.append(Yaku('chiitoitsu', yakuFile))
        if self.isToitoi(currentArrange):
            temp.append(Yaku('toitoi', yakuFile))
        if self.isSanankou(currentArrange):
            temp.append(Yaku('sanankou', yakuFile))
        if self.isSankantsu(currentArrange):
            temp.append(Yaku('sankantsu', yakuFile))
        if self.isHonitsu():
            temp.append(Yaku('honitsu', yakuFile))
        if self.isJunchan(currentArrange):
            temp.append(Yaku('junchan', yakuFile))
        if self.isRyanpeikou(currentArrange):
            temp.append(Yaku('ryanpeikou', yakuFile))
        if self.isShousangen() and currentFu != 25: #chiitoitsu not allowed
            temp.append(Yaku('shousangen', yakuFile))
        if self.isHonroutou():
            if currentFu == 25: #different han for seven pairs hand.
                temp.append(Yaku('honroutouPairs', yakuFile))
            else:
                temp.append(Yaku('honroutou', yakuFile))
        if self.isChinitsu():
            temp.append(Yaku('chinitsu', yakuFile))

        #Yakuman hands
        yakuman = []
        if self.isDaisangen():
            yakuman.append(Yaku('daisangen', yakuFile))
        if self.isSuuankou(currentArrange):
            yakuman.append(Yaku('suuankou', yakuFile))
        if self.isTsuiisou():
            yakuman.append(Yaku('tsuiisou', yakuFile))
        if self.isChinroutou():
            yakuman.append(Yaku('chinroutou', yakuFile))
        if self.isRyuuiisou():
            yakuman.append(Yaku('ryuuiisou', yakuFile))
        if self.isChuuren():
            yakuman.append(Yaku('chuuren', yakuFile))
        if self.isKokushi():
            yakuman.append(Yaku('kokushi', yakuFile))
        if self._canTenhou:
            yakuman.append(Yaku('tenhou', yakuFile))
        if self._canChiihou:
            yakuman.append(Yaku('chiihou', yakuFile))

        if yakuman: #yakuman override previous yaku
            temp = yakuman
        else:
            for yaku in temp:
                for invalidYaku in yaku.getInvalid():
                    testYaku = Yaku(invalidYaku, yakuFile)
                    if testYaku in temp:
                        temp.remove(testYaku)
        return temp

###YAKU CHECKERS###
#Separated because this is longwinded.
#In the same order as in the yaku.txt file
    def getYakupai(self, roundWind, yakuFile):
        """ Checks for applicable yakupai, given a round wind.
        Returns a list of yakupai, or [] if none.

        getYakupai(Tile) -> Boolean
        
        """
        temp = []
        if self.countTile(Tile(41)) > 2:
            temp.append(Yaku('yakupaiGD', yakuFile))
        if self.countTile(Tile(42)) > 2:
            temp.append(Yaku('yakupaiRD', yakuFile))
        if self.countTile(Tile(43)) > 2:
            temp.append(Yaku('yakupaiWD', yakuFile))
        if self.countTile(self._seatWind) > 2:
            temp.append(Yaku('yakupaiSeatWind', yakuFile))
        if self.countTile(roundWind) > 2:
            temp.append(Yaku('yakupaiRoundWind', yakuFile))
        return temp

    def isPinfu(self, currentFu, selfDrawn):
        """ Checks to see whether the hand is pinfu. (no bonus fu)

        isPinfu(int) -> Boolean

        currentFu: an integer representing the amount of fu in the hand.
        selfDrawn is a Boolean on whether the last tile was self drawn or taken
        from someone else.
        
        """
        if not self._closed:
            return False #must be closed
        if currentFu == 20 and selfDrawn:
            return True #No bonus fu for tsumo
        elif currentFu == 30 and not selfDrawn:
            return True #No bonus fu for ron
        else:
            return False

    def isTanyao(self):
        """ Checks to see whether the hand is tanyao. (no special tiles)

        isTanyao() -> Boolean
        
        """
        tempHand = self.returnTiles()
        for item in tempHand:
            if item.isSpecial(self._suitnum):
                return False #Need all tiles to not be special
        return True

    def isIipeikou(self, currentArrange):
        """ Checks to see whether the hand has an iipeikou. (two of the same
        sequence)

        isIipeikou(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
            
        """
        if not self._closed:
            return False #must be closed
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        for tileColl in currentArrange:
            if currentArrange.count(tileColl) > 1 and tileColl.getType() == 'chi':
                return True
        return False

    def isItsuu(self, currentArrange):
        """ Checks to see whether the hand has an itsuu (melds of 123, 456, 789
        in a suit).

        isItsuu(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
            
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        for x in range(self._suitnum):
            tile1 = Tile(int(str(x+1) + str(1)))
            tile4 = Tile(int(str(x+1) + str(4)))
            tile7 = Tile(int(str(x+1) + str(7)))
            if ((currentArrange.count(TileCollection('chi', tile1, -1))) and
                (currentArrange.count(TileCollection('chi', tile4, -1))) and
                (currentArrange.count(TileCollection('chi', tile7, -1)))):
                return True
        return False

    def isChanta(self, currentArrange):
        """ Checks to see whether the hand is chanta (contains a
        terminal/honour in each meld)

        isChanta(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        if len(currentArrange) == 0:
            return False
        for tileColl in currentArrange:
            if not self.arrangeSearchTileColl(tileColl, 'special'):
                return False
        return True

    def arrangeSearchTileColl(self, tileColl, typeSearch):
        """ Given a TileCollection, sees whether there is a terminal/honour
        tile and returns True or False accordingly.
        Helper function for isChanta() and isJunchan().
        
        typeSearch: either 'special' or 'terminal'     
            
        """
        tileList = tileColl.getTileList()
        specialTile = False
        for tile in tileList: #There must be a special tile in the meld
            if typeSearch == 'special':
                if tile.isSpecial(self._suitnum):
                    specialTile = True
            elif typeSearch == 'terminal':
                if tile.isTerminal(self._suitnum):
                    specialTile = True
        return specialTile

    def isSanshoku(self, currentArrange):
        """ Checks to see whether the hand is sanshoku (3 of the same sequence
        in different suits)

        isSanshoku(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        for tileColl in currentArrange:
            if tileColl.getType() == 'chi':
                temp = TileCollection('chi', tileColl.getMainTile(), -1)
                curCount = 0
                for x in range(self._suitnum):
                    temp.setSuit(x+1)
                    if currentArrange.count(temp) != 0:
                        curCount += 1
                if curCount == 3:
                    return True
        return False

    def isSanshokuAlt(self, currentArrange):
        """ Checks to see whether the hand is sanshoku doukou (3 of the same
        3 of a kind in different suits)

        isSanshokuAlt(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        if len(currentArrange) == 0:
            return False
        for tileColl in currentArrange:
            curType = tileColl.getType()
            if curType == 'pon' or curType == 'kan_cl' or curType == 'kan_op':
                temp = TileCollection('pon', tileColl.getMainTile(), -1)
                curCount = 0
                for x in range(self._suitnum):
                    for y in ['pon', 'kan_cl', 'kan_op']:
                        temp.setSuit(x+1)
                        temp.setType(y)
                        if currentArrange.count(temp) != 0:
                            curCount += 1
                if curCount == 3:
                    return True
        return False

    def isChiitoitsu(self):
        """ Checks to see whether the hand is a chiitoitsu. (must have seven
        pairs, with no double-ups)

        isChiitoitsu() -> Boolean
        
        """
        tempMutable = sorted(self._mutable, key = lambda x: x.getUniqueID())
        if len(tempMutable) < 14: #Need 14 tiles for this
            return False
        if not (tempMutable.count(tempMutable[0]) == 2 and
                tempMutable.count(tempMutable[2]) == 2 and
                tempMutable.count(tempMutable[4]) == 2 and
                tempMutable.count(tempMutable[6]) == 2 and
                tempMutable.count(tempMutable[8]) == 2 and
                tempMutable.count(tempMutable[10]) == 2 and
                tempMutable.count(tempMutable[12]) == 2):
            return False #Need seven pairs (should be in order)
        return True

    def isToitoi(self, currentArrange):
        """ Checks to see whether the hand is toitoi (no sequences).

        isToitoi(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        if len(currentArrange) == 0:
            return False
        for tileColl in currentArrange:
            curType = tileColl.getType()
            if curType == 'chi':
                return False
        return True

    def isSanankou(self, currentArrange):
        """ Checks to see whether the hand is sanankou (3 or more closed 3/4 of
        a kinds)

        isSanankou(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        curCount = 0
        for tileColl in currentArrange:
            curType = tileColl.getType()
            if curType == 'pon' or curType == 'kan_cl' or curType == 'kan_op':
                if tileColl.getSide() == -1:
                    curCount += 1
        return curCount >= 3

    def isSankantsu(self, currentArrange):
        """ Checks to see whether the hand is sankantsu (3 or more 4 of a kinds)

        isSankantsu(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        curCount = 0
        for tileColl in currentArrange:
            curType = tileColl.getType()
            if curType == 'kan_cl' or curType == 'kan_op':
                curCount += 1
        return curCount >= 3

    def isHonitsu(self):
        """ Checks to see whether the hand is honitsu (All tiles are either in
        the same numeric suit, or an honour tile (ie. two suits are absent).
        There must be an honour tile in the hand.)

        isHonitsu() -> Boolean
        
        """
        tileList = self.returnTiles()
        honour = False
        curSuit = -1
        for tile in tileList:
            if not tile.isHonour(self._suitnum):
                if curSuit == -1:
                    curSuit = tile.getSuitID()
                elif curSuit != tile.getSuitID():
                    return False
            else:
                honour = True
        return honour

    def isJunchan(self, currentArrange):
        """ Checks to see whether the hand is junchan (contains a terminal in
        each meld)
        
        isJunchan(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        if len(currentArrange) == 0:
            return False
        for tileColl in currentArrange:
            if not self.arrangeSearchTileColl(tileColl, 'terminal'):
                return False
        return True

    def isRyanpeikou(self, currentArrange):
        """ Checks to see whether the hand has a ryanpeikou. (two iipeikous)

        isRyanpeikou(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())
        """
        if not self._closed:
            return False #must be closed
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        for tileColl in currentArrange:
            if currentArrange.count(tileColl) > 1 and tileColl.getType() == 'chi':
                splitArrange = list(currentArrange)
                splitArrange.remove(tileColl)
                splitArrange.remove(tileColl)
                return self.isIipeikou(splitArrange)
        return False

    def isShousangen(self):
        """ Checks to see whether the hand is shousangen. (Two three/four of a
        kinds and a pair of the dragons.)

        isShousangen() -> Boolean

        currentArrange: a list of the current TileCollections the hand can be
        split up into. (the output of isValid())

        PROOF:
        If our hand is valid, we can only have one pair.
        Thus, if we have more than one tile of each dragon,
        we MUST have (at least) 2 three of a kinds.
        Assuming no chiitoitsu, of course.
        """
        if (self.countTile(Tile(41)) > 1 and
            self.countTile(Tile(42)) > 1 and
            self.countTile(Tile(43)) > 1):
                return True
        else:
            return False

    def isHonroutou(self):
        """ Checks to see whether the hand is honroutou. (All tiles are
        terminals or honours)

        isHonroutou() -> Boolean
        
        """
        tempHand = self.returnTiles()
        for item in tempHand:
            if not item.isSpecial(self._suitnum):
                return False #Need all tiles to be terminal
        return True

    def isChinitsu(self):
        """ Checks to see whether the hand is chinitsu. (All tiles are in the
        same numeric suit)

        isChinitsu() -> Boolean
        
        """
        tileList = self.returnTiles()
        curSuit = -1
        for tile in tileList:
            if curSuit == -1:
                curSuit = tile.getSuitID()
            elif curSuit != tile.getSuitID():
                return False
        return True


#YAKUMAN HANDS
    def isDaisangen(self):
        """ Checks to see whether the hand is daisangen. (Three three/four of a
        kinds of the dragons.)

        isDaisangen() -> Boolean
        
        """
        if (self.countTile(Tile(41)) > 2 and
            self.countTile(Tile(42)) > 2 and
            self.countTile(Tile(43)) > 2):
                return True
        else:
            return False

    def isSuuankou(self, currentArrange):
        """ Checks to see whether the hand is suuankou. (Four closed 3/4 of a
        kinds.)
           
        isSuuankou(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand
        can be split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        curCount = 0
        for tileColl in currentArrange:
            curType = tileColl.getType()
            if curType == 'pon' or curType == 'kan_cl' or curType == 'kan_op':
                if tileColl.getSide() == -1:
                    curCount += 1
        return curCount == 4

    def isSuukantsu(self, currentArrange):
        """ Checks to see whether the hand is suukantsu (four 4 of a kinds)

        isSankantsu(list of TileCollections) -> Boolean

        currentArrange: a list of the current TileCollections the hand
        can be split up into. (the output of isValid())
        
        """
        if currentArrange == -1:
            return False #Chiitoitsu consideration
        curCount = 0
        for tileColl in currentArrange:
            curType = tileColl.getType()
            if curType == 'kan_cl' or curType == 'kan_op':
                curCount += 1
        return curCount == 4

    def isTsuiisou(self):
        """ Checks to see whether the hand is tsuiisou. (All tiles are honours)

        isTsuiisou() -> Boolean
        
        """
        tempHand = self.returnTiles()
        for item in tempHand:
            if not item.isHonour(self._suitnum):
                return False #Need all tiles to be honour
        return True

    def isChinroutou(self):
        """ Checks to see whether the hand is chinroutou. (All tiles are
        terminals)

        isChinroutou() -> Boolean
        
        """
        tempHand = self.returnTiles()
        for item in tempHand:
            if not item.isTerminal(self._suitnum):
                return False #Need all tiles to be terminal
        return True

    def isRyuuiisou(self):
        """ Checks to see whether the hand is 'all green'. (All tiles are GD
        or 2, 3, 4, 6, 8 sou)

        isRyuuiisou() -> Boolean
        
        """
        tempHand = self.returnTiles()
            #Yes, this is hardcoded. List of green tiles.
        for item in tempHand:
            if not item in GREENTILES:
                return False #Need all tiles to be green
        return True

    def isChuuren(self):
        """ Checks to see whether the given hand is nine gates. (must have
        1112345678999 in any suit)

        isChuuren() -> Boolean
        
        """
        tempHand = self.returnTiles()
        if len(tempHand) < 14: #Need 14 tiles for this
            return False
        for x in range(self._suitnum): #For each suit
            if not (tempHand.count(Tile(int(str(x+1) + "1"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "1"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "1"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "2"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "3"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "4"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "5"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "6"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "7"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "8"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "9"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "9"))) > 0 and
                    tempHand.count(Tile(int(str(x+1) + "9"))) > 0):
                continue #Need one of each in the first thirteen
            for item in tempHand:
                if not item.getSuitID == x:
                    continue #Need all tiles to be in that suit
            return True #This can only be reached if the 'continue' is not run
        return False
    
    
    def isKokushi(self):
        """ Checks to see whether the given hand is a kokushi musou. (must have
        one of every terminal and honor, with one pair)

        isKokushi() -> Boolean
            
        """
        tempMutable = self._mutable
        if len(tempMutable) < 14: #Need 14 tiles for this
            return False
        if not (tempMutable.count(Tile(11)) > 0 and
                tempMutable.count(Tile(19)) > 0 and
                tempMutable.count(Tile(21)) > 0 and
                tempMutable.count(Tile(29)) > 0 and
                tempMutable.count(Tile(31)) > 0 and
                tempMutable.count(Tile(39)) > 0 and
                tempMutable.count(Tile(41)) > 0 and
                tempMutable.count(Tile(42)) > 0 and
                tempMutable.count(Tile(43)) > 0 and
                tempMutable.count(Tile(51)) > 0 and
                tempMutable.count(Tile(52)) > 0 and
                tempMutable.count(Tile(53)) > 0 and
                tempMutable.count(Tile(54)) > 0):
            return False #Need one of each in the first thirteen
        for item in tempMutable:
            if not item.isSpecial(self._suitnum):
                return False #Need all tiles to be special
        return True
