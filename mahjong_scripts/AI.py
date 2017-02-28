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

""" AI.py:
Contains all of the AI classes. An AI class has the ability to take information
about the current status of an in-progress game of mahjong, and, when asked,
can make intelligent decisions and actions in response to this status.

"""

#Import major libraries
import random

#Import the mahjong rulebase
from mahjong_rulebase import *

#Some globals
SUITNUM = 3
TOTALSUITNUM = 5

class NoneAI(object):
    """ Base AI object. Merely discards the first tile in its hand, and never
    calls when prompted.

    """
    def __init__(self, gameScreen, playerID):
        """ Create a new AI, attached to the game playing on gameScreen.
        Constructor: NoneAI(MenuScreen, int)

        gameScreen is the screen containing this AI.
        playerID is the ID of the player who this AI represents.

        """
        self._gameScreen = gameScreen
        self._playerID = playerID
        self._updatePlayer()

    def _updatePlayer(self):
        """ Reload the player info from the screen. Should be run before every
        new check.

        _updatePlayer() -> None

        """
        self._player = self._gameScreen.getPlayer(self._playerID)

    def checkDiscard(self):
        """ Asks which tile should be discarded from the AI player's hand.

        checkDiscard() -> int
        The returned integer refers to the index of the tile in the hand.

        """
        return 0

    def checkPon(self, tile):
        """ Asks whether the AI will pon the given tile.

        checkPon(Tile) -> Boolean

        """
        return False

    def checkChi(self, tile, poss):
        """ Asks which tile the AI will chi from the given possibilities and
        the tile, and returns False if none.

        checkChi(Tile, list of tuple tile hand indexes) -> Boolean

        """
        return False

    def checkKanOpen(self, tile):
        """ Asks whether the AI will open kan the given tile.

        checkKanOpen(Tile) -> Boolean

        """
        return False

    def checkKanClosed(self, tile):
        """ Asks whether the AI will closed kan the given tile.

        checkKanClosed(Tile) -> Boolean

        """
        return False

    def checkKanLate(self, tile):
        """ Asks whether the AI will late kan the given tile.

        checkKanLate(Tile) -> Boolean

        """
        return False

    def checkRon(self, tile):
        """ Asks whether the AI will ron the given tile.

        checkRon(Tile) -> Boolean

        """
        return False

    def checkTsumo(self):
        """ Asks whether the AI will tsumo.

        checkTsumo() -> Boolean

        """
        return False

    def checkRiichi(self):
        """ Asks whether the AI will riichi.

        checkRiichi() -> Boolean

        """
        return False

    def checkRiichiDiscard(self, poss):
        """ Asks which tile the Ai will discard when declaring riichi.

        checkDiscard(list) -> int
        poss is a list of all tile indexes in the hand which can be discarded.
        The returned integer refers to the index of the tile in the hand.

        """
        return poss[0]

class GeoffAI(NoneAI):
    """ Randomised AI object. Always calls and discards any old random tile in
    its hand. Essentially, imitates a blind idiot player.

    """
    def __init__(self, gameScreen, playerID):
        """ Create a new GeoffAI, attached to the game playing on gameScreen.
        Constructor: GeoffAI(MenuScreen, int)

        gameScreen is the screen containing this AI.
        playerID is the ID of the player who this AI represents.

        """
        NoneAI.__init__(self, gameScreen, playerID)

    def checkDiscard(self):
        """ Asks which tile should be discarded from the AI player's hand.

        checkDiscard() -> int
        The returned integer refers to the index of the tile in the hand.

        """
        self._updatePlayer()
        num = len(self._player.getMutable())
        dis = random.randint(0, num - 1)
        return dis

    def checkPon(self, tile):
        """ Asks whether the AI will pon the given tile.

        checkPon(Tile) -> Boolean

        """
        return True

    def checkChi(self, tile, poss):
        """ Asks which tile the AI will chi from the given possibilities and
        the tile, and returns False if none.

        checkChi(Tile, list of tuple tile hand indexes) -> Boolean

        """
        return poss[0]

    def checkKanOpen(self, tile):
        """ Asks whether the AI will open kan the given tile.

        checkKanOpen(Tile) -> Boolean

        """
        return True

    def checkKanClosed(self, tile):
        """ Asks whether the AI will closed kan the given tile.

        checkKanClosed(Tile) -> Boolean

        """
        return True

    def checkKanLate(self, tile):
        """ Asks whether the AI will late kan the given tile.

        checkKanLate(Tile) -> Boolean

        """
        return True

    def checkRon(self, tile):
        """ Asks whether the AI will ron the given tile.

        checkRon(Tile) -> Boolean

        """
        return True

    def checkTsumo(self):
        """ Asks whether the AI will tsumo.

        checkTsumo() -> Boolean

        """
        return True

    def checkRiichi(self):
        """ Asks whether the AI will riichi.

        checkRiichi() -> Boolean

        """
        return True

    def checkRiichiDiscard(self, poss):
        """ Asks which tile the Ai will discard when declaring riichi.

        checkDiscard(list) -> int
        poss is a list of all tile indexes in the hand which can be discarded.
        The returned integer refers to the index of the tile in the hand.

        """
        dis = random.choice(poss)
        return dis

class HighHandAI(NoneAI):
    """ HighHandAI AI object. This AI chooses the numbered suit in its hand that
    it has the most of and discards all other non-special tiles, if it has any.
    Otherwise, it'll just discard whatever. Calls on these tiles if there's not
    many turns remaining.

    """
    def __init__(self, gameScreen, playerID):
        """ Create a new HighHandAI.
        Constructor: HighHandAI(MenuScreen, int)

        gameScreen is the screen containing this AI.
        playerID is the ID of the player who this AI represents.

        """
        NoneAI.__init__(self, gameScreen, playerID)

    def _updateGoal(self):
        """ Updates the current goal suit that this AI is heading for, as well
        as some other information that's useful for these methods.

        """
        self._updatePlayer()
        self._curSuit = 1
        self._curCount = 0
        for x in range(SUITNUM):
            thisCount = self._player.countSuitTiles(x+1)
            if thisCount > self._curCount:
                self._curSuit = x+1
                self._curCount = thisCount
        if self._gameScreen.getTilesRemaining() < 15:
            self._allowCalling = True
        else:
            self._allowCalling = False

    def checkDiscard(self):
        """ Asks which tile should be discarded from the AI player's hand.

        checkDiscard() -> int
        The returned integer refers to the index of the tile in the hand.

        """
        self._updateGoal()
        choice = -1
        honourTiles = []

        #Go through and discard any tiles that aren't in our goal suit and are
        #not honour tiles
        for i, tile in enumerate(self._player.getMutable()):
            if (tile.getSuitID() != self._curSuit and
                    not tile.isHonour(SUITNUM)):
                choice = i #Discard the first tile not in the needed suit
                break
            elif tile.isHonour(SUITNUM):
                honourTiles.append((i, tile))

        if choice == -1: #If there is no tile to discard
            for (index, tile) in honourTiles: #Discard extraneous honours
                if self._player.countTile(tile) == 1:
                    choice = index
                    break
                elif self._player.countTile(tile) == 4:
                    choice = index
                    break

        if choice == -1: #If there /still/ is no tile to discard
            #Discard whatever
            num = len(self._player.getMutable()) - len(honourTiles) - 1
            dis = random.randint(0, num - 1)
        else: #Otherwise, discard it
            dis = choice
        return dis

    def checkPon(self, tile):
        """ Asks whether the AI will pon the given tile.

        checkPon(Tile) -> Boolean

        """
        self._updateGoal()
        if self._allowCalling: #If we should be calling tiles
            if (tile.getSuitID() == self._curSuit or
                    tile.isHonour(SUITNUM)):
                return True
        return False

    def checkChi(self, tile, poss):
        """ Asks which tile the AI will chi from the given possibilities and
        the tile, and returns False if none.

        checkChi(Tile, list of tuple tile hand indexes) -> Boolean

        """
        self._updateGoal()
        if self._allowCalling: #If we should be calling tiles
            for indexPoss in poss:
                tile = self._player.getTileFromIndex(indexPoss[0])
                if tile.getSuitID() == self._curSuit:
                    return indexPoss
        return False

    def checkKanOpen(self, tile):
        """ Asks whether the AI will open kan the given tile.

        checkKanOpen(Tile) -> Boolean

        """
        self._updateGoal()
        if self._allowCalling: #If we should be calling tiles
            if tile.getSuitID() == self._curSuit:
                return True
        return False

    def checkKanClosed(self, tile):
        """ Asks whether the AI will closed kan the given tile.

        checkKanClosed(Tile) -> Boolean

        """
        self._updateGoal()
        if tile.getSuitID() == self._curSuit:
            return True
        return False

    def checkKanLate(self, tile):
        """ Asks whether the AI will late kan the given tile.

        checkKanLate(Tile) -> Boolean

        """
        self._updateGoal()
        if tile.getSuitID() == self._curSuit:
            return True
        return False

    def checkRon(self, tile):
        """ Asks whether the AI will ron the given tile.

        checkRon(Tile) -> Boolean

        """
        return True

    def checkTsumo(self):
        """ Asks whether the AI will tsumo.

        checkTsumo() -> Boolean

        """
        return True

    def checkRiichi(self):
        """ Asks whether the AI will riichi.

        checkRiichi() -> Boolean

        """
        return True

    def checkRiichiDiscard(self, poss):
        """ Asks which tile the Ai will discard when declaring riichi.

        checkDiscard(list) -> int
        poss is a list of all tile indexes in the hand which can be discarded.
        The returned integer refers to the index of the tile in the hand.

        """
        self._updateGoal()
        for index in poss:
            tile = self._player.getTileFromIndex(index)
            if tile.getSuitID() != self._curSuit:
                return index
        return random.choice(poss)

class AttackAI(NoneAI):
    """ AttackAI AI object. This AI always attempts to go for quick, cheap hands
    like toitoi and tanyao, opening up the hand at the first oppotunity. Does
    not check to see whether other player's discards.

    """
    def __init__(self, gameScreen, playerID):
        """ Create a new AttackAI.
        Constructor: AttackAI(MenuScreen, int)

        gameScreen is the screen containing this AI.
        playerID is the ID of the player who this AI represents.

        """
        NoneAI.__init__(self, gameScreen, playerID)

    def _updateGoal(self):
        """ Determines whether we're trying to go for toitoi or pinfu.

        """
        self._updatePlayer()
        self._curGoal = 'toitoi'
        for tileColl in self._player.getImmutable():
            if tileColl.getType() == 'chi':
                self._curGoal = 'pinfu'
                break

    def checkDiscard(self):
        """ Asks which tile should be discarded from the AI player's hand.

        checkDiscard() -> int
        The returned integer refers to the index of the tile in the hand.

        """
        self._updateGoal()
        playerMutable = self._player.getMutable()
        playerImmutable = self._player.getImmutable()
        suits = self._player.splitSuits(playerMutable)
        curSetItem = None
        choice = -1
        
        #If we are going toitoi, we shouldn't care about tanyao too much
        #Conversely, if we aren't or aren't sure, discard the first terminal
        if not ((self._curGoal == 'toitoi') and (len(playerImmutable) > 0)):
            for i, tile in enumerate(playerMutable):
                #Remove terminals and honours first
                if tile.isSpecial(SUITNUM):
                    return i
        
        #Discard straggler tiles
        for setItem in suits: 
            if len(setItem)%3 == 1:
                curSetItem = setItem
                break
        if curSetItem: #If there is a straggler tile
            curTile = random.choice(curSetItem)
            choice = self._player.getIndexFromTile(curTile)[0]
        elif self._curGoal == 'toitoi': #If toitoi, get rid of the first single
            for i, tile in enumerate(playerMutable):
                if self._player.countTile(tile) == 1:
                    choice = i
                    break

        #If there /still/ is no tile to discard
        if choice == -1: #Just discard anything
            num = len(playerMutable) - 1
            dis = random.randint(0, num - 1)
        else: #Otherwise, discard our choice
            dis = choice
        return dis

    def checkPon(self, tile):
        """ Asks whether the AI will pon the given tile.

        checkPon(Tile) -> Boolean

        """
        self._updateGoal()
        if self._curGoal == 'toitoi': #If we should be calling tiles
            return True
        return False

    def checkChi(self, tile, poss):
        """ Asks which tile the AI will chi from the given possibilities and
        the tile, and returns False if none.

        checkChi(Tile, list of tuple tile hand indexes) -> Boolean

        """
        self._updateGoal()
        if tile.isTerminal(SUITNUM):
            return False
        if (len(self._player.getImmutable()) == 0 or
                self._curGoal == 'pinfu'): #If we should be calling tiles
            self._curGoal = 'pinfu'
            return poss[0]
        return False

    def checkKanOpen(self, tile):
        """ Asks whether the AI will open kan the given tile.

        checkKanOpen(Tile) -> Boolean

        """
        self._updateGoal()
        if self._curGoal == 'toitoi': #If we should be calling tiles
            return True
        return False

    def checkKanClosed(self, tile):
        """ Asks whether the AI will closed kan the given tile.

        checkKanClosed(Tile) -> Boolean

        """
        self._updateGoal()
        if self._curGoal == 'toitoi': #If we should be calling tiles
            return True
        return False

    def checkKanLate(self, tile):
        """ Asks whether the AI will late kan the given tile.

        checkKanLate(Tile) -> Boolean

        """
        self._updateGoal()
        if self._curGoal == 'toitoi': #If we should be calling tiles
            return True
        return False

    def checkRon(self, tile):
        """ Asks whether the AI will ron the given tile.

        checkRon(Tile) -> Boolean

        """
        return True

    def checkTsumo(self):
        """ Asks whether the AI will tsumo.

        checkTsumo() -> Boolean

        """
        return True

class DefendAI(NoneAI):
    """ DefendAI AI object. This AI never really goes for hands, instead opting
    to avoid ever dealing into the hands of others by checking the discard piles
    of others. Basically, bails whenever possible, wins only in very unique
    circumstances.

    """
    def __init__(self, gameScreen, playerID):
        """ Create a new DefendAI.
        Constructor: DefendAI(MenuScreen, int)

        gameScreen is the screen containing this AI.
        playerID is the ID of the player who this AI represents.

        """
        NoneAI.__init__(self, gameScreen, playerID)

    def _updateGoodList(self):
        """ Determines a list of what tiles we can discard, from most to least
        safe.

        """
        self._updatePlayer()
        goodList1 = []
        goodList2 = []
        goodList3 = []
        goodList4 = []
        goodList5 = []
        goodList6 = []

        #First, get a collection of all discard piles and called melds.
        allDiscards = self._gameScreen.getAllDiscards()
        allMelds = self._gameScreen.getAllMelds()
        allVisible = allDiscards + allMelds
        safeWinds = self._gameScreen.getNonRoundWinds()
        roundWind = self._gameScreen.getRoundWind()

        for i, tile in enumerate(self._player.getMutable()):
            #This is done in the order which saves the most processing time.
            #A tile in our hand is good if:
            #Best - There are 3 of it in the discard pile and called melds.
            if allVisible.count(tile) >= 3:
                goodList1.append(i)
                continue
            #Second Best - It is a non-round wind.
            if tile in safeWinds:
                goodList2.append(i)
                continue
            #Third Best- It is in someone's discard pile.
            if tile in allDiscards:
                goodList3.append(i)
                continue
            #Fourth Best - It is a terminal.
            if tile.isTerminal(SUITNUM):
                goodList4.append(i)
                continue
            #Worst - It is a honour tile or round wind.
            if tile.isHonour(SUITNUM) or tile == roundWind:
                goodList6.append(i)
                continue
            #Second Worst - It is anything else.
            goodList5.append(i)

        random.shuffle(goodList5) #Shuffle this to do it randomly.

        self._goodList = (goodList1 + goodList2 + goodList3 + goodList4 +
                          goodList5 + goodList6)

    def checkDiscard(self):
        """ Asks which tile should be discarded from the AI player's hand.

        checkDiscard() -> int
        The returned integer refers to the index of the tile in the hand.

        """
        self._updateGoodList()
        return self._goodList[0]

    def checkKanClosed(self, tile):
        """ Asks whether the AI will closed kan the given tile.

        checkKanClosed(Tile) -> Boolean

        """
        return True

    def checkKanLate(self, tile):
        """ Asks whether the AI will late kan the given tile.

        checkKanLate(Tile) -> Boolean

        """
        return True

    def checkRon(self, tile):
        """ Asks whether the AI will ron the given tile.

        checkRon(Tile) -> Boolean

        """
        return True

    def checkTsumo(self):
        """ Asks whether the AI will tsumo.

        checkTsumo() -> Boolean

        """
        return True
