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

""" gameScreen.py:
Contains the main game screen, which is made up of three parts:
    - The backend rules and functions relating to gameplay.
    - The constantly running update function, which reloads the game constantly.
    - The surface portion, which draws all the game elements to the screen.
This is effectively the main part of the game.

"""

#Import major libraries
import pygame
from pygame.locals import *
from os import listdir
from os.path import isfile, join

#Import other mahjong modules
import mahjongGlobals
from AI import *
from mahjong_rulebase import *
from menuItems import *

class GameScreen(MenuScreen):
    """ The GameScreen object, a subclass of MenuScreen. Is made up of three
    main parts, described at the top of this file.

    """
    def __init__(self, master, startingValues):
        """ Create a new GameScreen.
        Constructor: GameScreen(RiichiMahjongApp, list)

        master is the main app window which this screen should be placed on.
        startingValues is a list of values which are passed to this constructor
        to determine how the game should start up:
            startingValues[0] - Boolean flag on whether to load a game or not.
            startingValues[1] - String containing the user player's name.
            startingValues[2] - Integer containing the starting score.
            startingValues[3] - Which AI player number 1 is.
            startingValues[4] - Which AI player number 2 is.
            startingValues[5] - Which AI player number 3 is.
            startingValues[6] - Boolean flag on whether the game is just the
                                East round or both East and South.
            startingValues[7] - String for which colour the background is,
                                one of 'Blue', 'Red' or 'Green'.

        """
        #Load sprites and define default variables
        self._loadStandardInfo(master)
        
        if startingValues[0] == True: #If they chose to load a game
            self.loadGame()
            bgImg = pygame.image.load(self._bgImgLoc).convert()
            MenuScreen.__init__(self, master, bgImg)
        else: #If this is a new game
            #Get starting values from the options they gave
            self._playerName = startingValues[1]
            self._startingScore = startingValues[2]
            self._p1ai = startingValues[3]
            self._p2ai = startingValues[4]
            self._p3ai = startingValues[5]
            self._isJustEastRound = startingValues[6]
            self._backColour = startingValues[7]
            if self._backColour == 'Blue':
                self._bgImgLoc = mahjongGlobals.MAINBACKBLUEIMG
            elif self._backColour == 'Red':
                self._bgImgLoc = mahjongGlobals.MAINBACKREDIMG
            else:
                self._bgImgLoc = mahjongGlobals.MAINBACKGREENIMG
            bgImg = pygame.image.load(self._bgImgLoc).convert()
            MenuScreen.__init__(self, master, bgImg)

            #Other starting values
            self._curStage = 'roundstart1'
            self._curRound = ('East', 1, 0)
            self._riichiStore = 0 #Holds leftover riichi from previous rounds
            self._bonusStore = 0 #Holds leftover bonus sticks from prev. rounds
            self._curDealer = 0 #Current dealer
            self._winTable = [[], [], [], [], []]
                #Table of scores for the game over screen
            
            #Players
                #Note that [0] is the user, and the others are the AI players
                #The index here goes anticlockwise around the game board
            self._players = []
            self._players.append(PlayerScore(self._handsize, self._suitnum,
                self._totalsuitnum, self._playerName, self._startingScore))
            self._players.append(PlayerScore(self._handsize, self._suitnum,
                self._totalsuitnum, 'CPU Player 1', self._startingScore))
            self._players.append(PlayerScore(self._handsize, self._suitnum,
                self._totalsuitnum, 'CPU Player 2', self._startingScore))
            self._players.append(PlayerScore(self._handsize, self._suitnum,
                self._totalsuitnum, 'CPU Player 3', self._startingScore))

            #AI
            exec('ai1 = ' + self._p1ai + '(self, 1)')
            exec('ai2 = ' + self._p2ai + '(self, 2)')
            exec('ai3 = ' + self._p3ai + '(self, 3)')
            self._ai = [ai1, ai2, ai3]

            #Setup the round begin variables
            self._resetVars()

    def _loadStandardInfo(self, master):
        """ Setup the default variables and load all sprite images and buttons.

        _loadStandardInfo(RiichiMahjongApp) -> None

        master is the main app window which this screen should be placed on.

        """
        self._noDraw = (-1,-1) #Which tile should be flashing
        self._animation = False #Are we waiting on some animation?
        self._curStageTimer = 0 #Timer, used for animation counting
        
        #Load game settings from file
        settingsLoad = IOHelper(mahjongGlobals.GAMESETTINGSLOC,
            mahjongGlobals.DELIMITER, mahjongGlobals.COMMENTIND)
        self._handsize = int(settingsLoad.getRowByOneID('handsize')[1])
        self._suitnum = int(settingsLoad.getRowByOneID('suitnum')[1])
        self._totalsuitnum = int(settingsLoad.getRowByOneID('totalsuitnum')[1])
        self._repeat = int(settingsLoad.getRowByOneID('repeat')[1])
        self._tileFile = settingsLoad.getRowByOneID('tilefile')[1]
        self._yakuFile = settingsLoad.getRowByOneID('yakufile')[1]

        #Sprites and surfaces
        #Remember to call convert() to get them all in the fastest blitting
        #format!
        self._riichiImg = pygame.image.load(mahjongGlobals.RIICHIIMG).convert()
        self._riichiVertImg = pygame.transform.rotate(self._riichiImg, 90)
        self._riichiTinyImg = pygame.image.load(mahjongGlobals.RIICHITINYIMG)
        self._riichiTinyImg = pygame.transform.scale(self._riichiTinyImg,
            (40, 40))
        self._bonusTinyImg = pygame.image.load(mahjongGlobals.BONUSTINYIMG)
        self._bonusTinyImg = pygame.transform.scale(self._bonusTinyImg,
            (40, 40))
        self._hudSepImg = pygame.image.load(mahjongGlobals.HUDSEPIMG).convert()
        self._hudMiniSepImg = pygame.image.load(
            mahjongGlobals.HUDMINISEPIMG).convert()
        self._hudMiniSepVertImg = pygame.image.load(
            mahjongGlobals.HUDMINISEPVERTIMG).convert()
        self._hudGameInfoImg = pygame.image.load(
            mahjongGlobals.HUDGAMEINFOIMG).convert()
        self._hudHandBackImg = pygame.image.load(
            mahjongGlobals.HUDHANDBACKIMG).convert()
        self._hudRightImg = pygame.image.load(
            mahjongGlobals.HUDRIGHTIMG).convert()
        self._hudRightLightImg = pygame.image.load(
            mahjongGlobals.HUDRIGHTLIGHTIMG).convert()
        self._hudRightSepImg = pygame.image.load(
            mahjongGlobals.HUDRIGHTSEPIMG).convert()

        #Tile sprites
        mypath = mahjongGlobals.TILEIMGLOC
        self._tileImgDict = {}
        for f in listdir(mypath):
            #Load a dictionary list of all tile Surfaces in the tilesprites
            #folder into _tileImgDict, with the keys being given by the image
            #name.
            if isfile(join(mypath,f)): #If this is a file, not a folder
                self._tileImgDict[f] = pygame.image.load(join(mypath,
                    f)).convert()

        #Dice sprites
        mypath = mahjongGlobals.DICEIMGLOC
        self._diceImgDict = {}
        for f in listdir(mypath):
            #Load a dictionary list of all tile Surfaces in the dicesprites
            #folder into _diceImgDict, with the keys being given by the image
            #name.
            if isfile(join(mypath,f)): #If this is a file, not a folder
                self._diceImgDict[f] = pygame.image.load(join(mypath,
                    f)).convert()

        #Buttons
        self._hudMenuButton = ButtonImgText(master,889,671,"Menu",
            mahjongGlobals.WHITE,mahjongGlobals.REDDISH,
            mahjongGlobals.CURRENTFONT,16,(135,29),self._buttMenu,
            mahjongGlobals.BUTTONIMG,mahjongGlobals.BUTTONDOWNIMG,
            mahjongGlobals.BUTTONHOVERIMG)
        self._hudPonButton = ButtonImgText(master,887,704,"Pon",
            mahjongGlobals.WHITE,mahjongGlobals.REDDISH,
            mahjongGlobals.CURRENTFONT,16,(67,31),self._buttPon,
            mahjongGlobals.BUTTONIMG,mahjongGlobals.BUTTONDOWNIMG,
            mahjongGlobals.BUTTONHOVERIMG)
        self._hudChiButton = ButtonImgText(master,887,737,"Chi",
            mahjongGlobals.WHITE,mahjongGlobals.REDDISH,
            mahjongGlobals.CURRENTFONT,16,(67,31),self._buttChi,
            mahjongGlobals.BUTTONIMG,mahjongGlobals.BUTTONDOWNIMG,
            mahjongGlobals.BUTTONHOVERIMG)
        self._hudKanButton = ButtonImgText(master,957,704,"Kan",
            mahjongGlobals.WHITE,mahjongGlobals.REDDISH,
            mahjongGlobals.CURRENTFONT,16,(67,31),self._buttKan,
            mahjongGlobals.BUTTONIMG,mahjongGlobals.BUTTONDOWNIMG,
            mahjongGlobals.BUTTONHOVERIMG)
        self._hudCallButton = ButtonImgText(master,957,737,"Call",
            mahjongGlobals.WHITE,mahjongGlobals.REDDISH,
            mahjongGlobals.CURRENTFONT,16,(67,31),self._buttCall,
            mahjongGlobals.BUTTONREDIMG,mahjongGlobals.BUTTONREDDOWNIMG,
            mahjongGlobals.BUTTONREDHOVERIMG)
        self._invisCancelButton = ButtonInvis(master,0,0,(884,768),
            self._buttMenu)
        self._skipScoreButton = ButtonInvis(master,0,0,(884,768),self._buttSkip)

        #No tile buttons should be there to start with
        self._hudTileButtons = [] 

        #Disable all side menu buttons
        self._hudMenuButton.disable()
        self._hudPonButton.disable()
        self._hudChiButton.disable()
        self._hudKanButton.disable()
        self._hudCallButton.disable()
        self._invisCancelButton.disable()
        self._skipScoreButton.disable()

        #Used for highlighted choices when declaring chi.
        self._curChiChoices = []
        self._highlightTiles = [] 

        #Animated Text
        self._aniText = []
        self._aniBack = []

        #Load all yaku
        self._yakuRinshan = Yaku('rinshan', self._yakuFile)
        self._yakuHaitei = Yaku('haitei', self._yakuFile)
        self._yakuHoutei = Yaku('houtei', self._yakuFile)
        self._yakuTenhou = Yaku('itsuu', self._yakuFile)
        self._yakuChiihou = Yaku('chanta', self._yakuFile)

    #ROUND LOGIC METHODS:
    def update(self):
        """ Updates the current logic status of the game. Should be run before
        redrawing the surface of this screen, once per frame.

        update() -> None

        """
        self._curStageTimer += 1
        if self._animation: #If animating, do that instead of game logic
            self._animate(self._animation)
        else: #Do something based off which stage we're at
            if self._curStage == 'roundstart1':
                #Very first stage, roll dice and display name
                self._roundStart1()
                self._curStage = 'roundstart2'
            elif self._curStage == 'roundstart2':
                #Get dealer and player seating, pause for a bit
                self._roundStart2()
                self._curStage = 'roundstart3'
            elif self._curStage == 'roundstart3':
                #Finished pausing, roll dice again
                self._startAnimate('dice', None)
                self._curStage = 'roundstart4'
            elif self._curStage == 'roundstart4':
                #Break the wall and set up the dora and dead wall
                self._roundStart4()
                self._curStage = 'drawtiles'
            elif self._curStage == 'drawtiles':
                #Do the beginning draw of 4 tiles each for all players
                self._drawTiles()
            elif self._curStage == 'turnstartcheck':
                #Check to see whether the player can call on the last tile
                self._curStage = 'turnstartcheck2'
                self._turnStartCheck()
            elif self._curStage == 'turnstartcheck2':
                #After getting the player's response, check to see who actually
                #gets the tile, assuming that a player has called on it
                self._turnStartCheck2('none')
            elif self._curStage == 'turnstart':
                #If it's in a drawing condition, draw; end the game
                #Else, let the current player take a tile from the wall
                self._turnStart()
            elif self._curStage == 'turnmid':
                #Depending on what state the player's in:
                    #Check to see if they can tsumo/kan/riichi
                    #If they decline or can't, make them discard if in riichi
                    #Otherwise, if it's the user, wait for them to respond
                    #Otherwise, get the AI's response
                if (self._tsumoCheck() or
                    self._lateKanCheck() or
                    self._closedKanCheck() or
                    self._riichiCheck()):
                    pass #Wait for next loop
                elif self._players[self._playerTurn].isRiichi():
                    self._riichiWaitCheck()
                elif self._playerTurn == 0:
                    self._userCanDiscard = True
                    self._hudMenuButton.enable()
                    self._curStage = 'playerresponse'
                else:
                    toDiscard = self._ai[self._playerTurn-1].checkDiscard()
                    self._playerDiscardAni(self._playerTurn, toDiscard)
                    self._curStage = 'turnend'
            elif self._curStage == 'turnend':
                #Reset all the current turn flags, then rotate the players
                self._turnEndReset()
                self._curStage = 'turnstartcheck'
            elif self._curStage == 'roundend':
                #Popup the round end dialog, get the scores ready to change
                self._curStage = 'scorechange'
                self._roundEnd()
            elif self._curStage == 'scorechange':
                #Repeatedly move the scores into position
                self._scoreChange()
            elif self._curStage == 'playerresponse':
                pass #Do nothing while waiting for the user to click/press

    def _roundStart1(self):
        """ Very start of a round. Popup the round name and roll the dice.

        _roundStart1() -> None

        """
        self._drawTextMid(self._getRoundName())
        self._startAnimate('dice', None)

    def _roundStart2(self):
        """ Find the dealer from the dice, allocate the seat winds and then
        pause for 30 frames.

        _roundStart2() -> None

        """
        dealer = random.randint(0, 3)
        dealer = (dealer + self._die1 + self._die2)%4
        self._curDealer = dealer
        for i, player in enumerate(self._players):
            player.setDealer(self._curDealer == i)
        self._allocateSeatWinds(dealer)
        self._startAnimate('pause', 30)

    def _roundStart4(self):
        """ Break the wall and set up the dora using the dice.

        _roundStart4() -> None

        """
        diedist = self._die1 + self._die2
        breakdist = (diedist)%4
        self._curWall.setDealerBreak(diedist, breakdist)

    def _drawTiles(self):
        """ Step-by-step function for drawing 4 tiles at a time at the beginning
        of a round for each player.

        _drawTiles() -> None

        """
        for x in range(4):
            self._playerDraw(x)
        self._startAnimate('pause', 5)
        if self._handsize - self._players[3].getTileNum() < 3:
            for y in range(4):
                self._playerDraw(y)
            self._playerTurn = self._curDealer
            self._curStage = 'turnstart'
                    
    def _turnStartCheck(self):
        """ Check to see whether the user can call on the last tile discarded in
        any way, and if they can, enable the buttons to do so.

        _turnStartCheck() -> None

        """
        if self._playerTurn == 1:
            return False #User can't call on the tile they just discarded
        if self._players[0].canRon(self._lastTile, self.getRoundWind(),
                self._yakuFile, self.getGameYaku(0, 'ron')): #If they can ron
            self._hudCallButton.enable()
            self._hudCallButton.changeText("Ron")
            self._curStage = 'playerresponse'
            if self._players[0].isRiichi():
                #Needed, as they can't call chi/pon etc. after declaring riichi
                self._enableCancelButtons()
                return
        elif self._players[0].isRiichi(): #Riichi locks out other options
            return
        if self._players[0].canKan(self._lastTile): #If they can kan
            self._hudKanButton.enable()
            self._curStage = 'playerresponse'
        if self._players[0].canPon(self._lastTile): #If they can pon
            self._hudPonButton.enable()
            self._curStage = 'playerresponse'
        if self._playerTurn == 0: 
            #This is done to not waste processing time for the other players
            self._curChiChoices = self._players[0].canChi(self._lastTile)
            if self._curChiChoices: #If they can chi
                self._hudChiButton.enable()
                self._curStage = 'playerresponse'
        if self._curStage == 'playerresponse': #If a button is enabled
            self._enableCancelButtons()

    def _turnStartCheck2(self, playerChoice):
        """ Goes through each non-discarding player in an anti-clockwise
        direction and sees whether they want to call on the last tile, letting
        pon override chi and similar; all the while taking into account the
        choice of the user.

        _turnStartCheck2(string) -> None

        playerChoice is a string ('pon', or 'chi' etc) which is passed to this
        function when clicking one of the buttons enabled through
        _turnStartCheck above.

        """
        orderedPlayers = self._playerOrder(self._playerTurn)
        prevPlayer = orderedPlayers[-1]
        curOrder = orderedPlayers[:-1]
            #This is three elements long, ignoring the player that just went
        if self._checkRon(curOrder, playerChoice, prevPlayer):
            self._players[prevPlayer].removeDiscard()
            return #If someone rons, don't bother about the rest anymore
        elif self._checkKan(curOrder, playerChoice):
            self._curStage = 'turnmid'
        elif self._checkPon(curOrder, playerChoice):
            self._curStage = 'turnmid'
        elif self._checkChi(playerChoice): 
            self._curStage = 'turnmid'
        else:
            self._curStage = 'turnstart'
        if self._curStage == 'turnmid':
            self._highlightTiles = []
                #Reset this in the case that they called chi
            self._players[prevPlayer].removeDiscard()

    def _riichiWaitCheck(self):
        """ If a player is in riichi, there's no need to give them options to
        discard or anything anymore. Either the tile they draw is part of their
        waiting tiles list and they tsumo, or it's not and they discard it.

        _riichiWaitCheck() -> None

        """
        curWait = self._players[self._playerTurn].getRiichiWait()
        curMutable = self._players[self._playerTurn].getMutable()
        curLen = len(self._players[self._playerTurn].returnTiles())
        if (curLen == self._handsize) and (curMutable[-1] in curWait):
            #curMutable[-1] should be their last drawn tile
            self._tsumo(self._playerTurn)
        else:
            toDiscard = -1
            self._playerDiscardAni(self._playerTurn, toDiscard)
            self._curStage = 'turnend'

    def _turnStart(self):
        """ First checks to see whether the game is going to end in a draw. If
        not, then makes the current player draw a tile. Damn, that terminology
        is confusing.

        _turnStart() -> None

        """
        allRiichi = True
        for player in self._players:
            if not player.isRiichi():
                allRiichi = False
        if self._curWall.getTilesRemaining() <= 0:
            self._drawTextFinal('Draw -- No More Tiles')
            self._startAnimate('pause', 100)
            self._curStage = 'roundend'
            self._endRoundType = 'nomoretiles'
        elif len(self._curWall.getDoraList()) >= 5:
            self._drawTextFinal('Draw -- Four Kans Declared')
            self._startAnimate('pause', 100)
            self._curStage = 'roundend'
            self._endRoundType = 'fourkans'
        elif allRiichi:
            self._drawTextFinal('Draw -- All Players Riichi')
            self._startAnimate('pause', 100)
            self._curStage = 'roundend'
            self._endRoundType = 'allriichi'
        else:
            self._playerDraw(self._playerTurn)
            self._curStage = 'turnmid'

    def _turnEndReset(self):
        """ Resets some of the starting turn flags, increments the turn counter
        and then moves the players around anticlockwise.

        _turnEndReset() -> None

        """
        self._optionsDeny = False
        self._lastDrawWasDead = False
        self._hudMenuButton.disable()
        self._curTurn += 1
        for player in self._players:
            player.addRiichiTurns(1)
        self._playerTurn += 1
        if self._playerTurn > 3:
            self._playerTurn = 0

    def _roundEnd(self):
        """ First, sees how exactly the current game is ending, and forms a
        list of data to pass to the popup dialog explaining this. Then, find
        the scores for each player and get ready to apply them, taking into
        account factors such as dora, riichi, bonus sticks etc. Finally, popup
        the window for a round ending.

        _roundEnd() -> None

        """
        roundInfo = [self._endRoundType]
        if self._endRoundType == 'ron' or self._endRoundType == 'tsumo':
            #If a player has won by ron or tsumo
            winningPlayer = self._players[self._playerWon]
            winningPlayer.addWin()
            otherPlayers = self._playerOrder(self._playerWon)[1:]
            winningPlayer.showHand()
            if self._endRoundType == 'ron':
                selfDrawn = False
            else:
                selfDrawn = True
            handArrange = winningPlayer.isValid()
            handFu = winningPlayer.getFu(self.getRoundWind(), handArrange,
                selfDrawn)
            handYaku = winningPlayer.getHandYaku(self.getRoundWind(),
                handArrange, handFu, selfDrawn, self._yakuFile)
            gameYaku = self.getGameYaku(self._playerWon, self._endRoundType)
            totalYaku = handYaku + gameYaku
            doraList = self.getDoraList(self._playerWon)
            if winningPlayer.isRiichi():
                uraList = self.getUraList(self._playerWon)
            else:
                uraList = []
            (handScore, scoreWord) = winningPlayer.scoreHand(totalYaku, handFu,
                    len(doraList) + len(uraList))

            #Append info about the scores and the round
            if winningPlayer.isRiichi():
                totalUraList = self._curWall.getUraList()
            else:
                totalUraList = []
            roundInfo += [winningPlayer, handFu, totalYaku, len(doraList)
                + len(uraList), self._curWall.getDoraList(), totalUraList,
                handScore, scoreWord]

            #Prepare the changes in scores
            if self._endRoundType == 'ron':
                if (self._playerWon == self._curDealer or
                        self._playerLost == self._curDealer):
                    curAmount = int(round(handScore*6,-2))
                else:
                    curAmount = int(round(handScore*4,-2))
                winningPlayer.setScoreDiff(curAmount)
                self._players[self._playerLost].setScoreDiff(-curAmount)
            elif self._playerWon == self._curDealer:
                for playerID in otherPlayers:
                    player = self._players[playerID]
                    player.setScoreDiff(int(round(-handScore*2,-2)))
                winningPlayer.setScoreDiff(int(round(handScore*6,-2)))
            else:
                for playerID in otherPlayers:
                    player = self._players[playerID]
                    if playerID == self._playerWon:
                        curAmount = int(round(-handScore*2,-2))
                        self._players[playerID].setScoreDiff(curAmount)
                    else:
                        curAmount = int(round(-handScore,-2))
                        self._players[playerID].setScoreDiff(curAmount)
                winningPlayer.setScoreDiff(int(round(handScore*4,-2)))
    
            #Riichi sticks
            riichiBonus = self._riichiStore
            for player in self._players:
                if player.isRiichi():
                    riichiBonus += 1000
            winningPlayer.addScoreDiff(riichiBonus)
            self._riichiStore = 0

            #Bonus Dealer ante
            if self._playerWon == self._curDealer:
                bonus = 0
                anteAmount = self._bonusStore + self._curRound[2]
                for i, player in enumerate(self._players):
                    if i != self._curDealer:
                        player.addScoreDiff(-anteAmount*100)
                    else:
                        player.addScoreDiff(anteAmount*300)
                self._bonusStore = 0
            else:
                self._players[self._curDealer].addScoreDiff(
                    100*self._curRound[2])
        else:
            #Scores for the no more tiles draw
            if self._endRoundType == 'nomoretiles':
                tenpaiList = []
                notList = []
                for i, player in enumerate(self._players):
                    uniqueTiles = self._curWall.getUnique()
                    if player.isTenpai(uniqueTiles):
                        player.showHand()
                        tenpaiList.append(i)
                    else:
                        notList.append(i)
                if tenpaiList:
                    curAmount1 = 3000/len(tenpaiList)
                    curAmount2 = 3000/len(notList)
                    for i in tenpaiList:
                        self._players[i].setScoreDiff(curAmount1)
                    for i in notList:
                        self._players[i].setScoreDiff(-curAmount2)
            riichiCount = 0
            for player in self._players:
                if player.isRiichi():
                    riichiCount += 1
            self._riichiStore += riichiCount
            self._bonusStore += self._curRound[2]
        
        #Update the winning table scores
        self._winTable[0].append(self._getRoundName())
        self._winTable[0].append('(+- change)')
        for i, player in enumerate(self._players):
            self._winTable[i+1].append(player.getScore())
            self._winTable[i+1].append(player.getScoreDiff())

        #Popup the winning dialog
        self.popupDialog('WindowRoundEnd', roundInfo)
        self._skipScoreButton.enable()
        self._curStageTimer = 0
        
    def _scoreChange(self):
        """ Step-by-step function for adding/subtracting the score bit by bit.

        _scoreChange() -> None

        """
        if self._curStageTimer%5 == 0: #Intermittently repeat the score sound
            self._master.playButtonSound('scoreSound')
        end = True
        for player in self._players:
            if not player.updateScoreDiff(100):
                end = False
        if end: #Wait for the user to continue
            self._skipScoreButton.disable()
            self._invisCancelButton.enable()
            self._hudMenuButton.changeText('Continue')
            self._hudMenuButton.enable()
            self._curStage = 'playerresponse'

    def _roundFinalise(self):
        """ Increments the rounds, and checks to see whether the game should end
        yet. If not, resets all the variables necessary and gets it all ready
        to rumble. If so, runs _gameEnd().

        _roundFinalise() -> None

        """
        for player in self._players: #If a player goes below 0, end the game
            if player.getScore() < 0:
                self._gameEnd()
                return
        if self._playerWon != self._curDealer:
            if not self._incrRound(): #If we can't go to the next round, end
                self._gameEnd()
                return
            self._curDealer += 1
            if self._curDealer > 3:
                self._curDealer = 0
        else:
            self._incrBonusRound() #Bonus rounds for dealers
        for player in self._players:
            player.resetPlayer() #Reset the player hands
        for i, player in enumerate(self._players):
            player.setDealer(self._curDealer == i)
        self._allocateSeatWinds(self._curDealer)
        self._resetVars()
        self._drawTextMid(self._getRoundName())
        self._curStage = 'roundstart3'

    def _gameEnd(self):
        """ Determines which player won, and then popups a display
        congratulating them and that whole shabang, before taking them back to
        the main menu.

        _gameEnd() -> None

        """
        winningPlayer = None
        winningScore = 0
        self._winTable[0].append('Final Total')
        for i, player in enumerate(self._players):
            self._winTable[i+1].append(player.getScore())
            if player.getScore() > winningScore:
                winningPlayer = player
                winningScore = player.getScore()
        self.popupDialog('WindowGameEnd', [winningPlayer, self._players,
            self._winTable])
        self.changeScreen('MainMenu',None)

    #BEFORE TURN CHECKERS
    def _checkRon(self, curOrder, playerChoice, prevPlayer):
        """ Goes through each player in an anticlockwise direction and sees if
        they want to ron the last tile, lets them do so and returns True if yes,
        returning False if no.

        _checkRon(list of integers, string, integer) -> Boolean

        curOrder is a list containing the three playersID's to check in order.
        playerChoice is a string containing which button the player pressed.
        prevPlayer is the ID of the player who discarded the tile

        """
        for playerID in curOrder: #RON CHECK
            if self._players[playerID].canRon(self._lastTile,
                    self.getRoundWind(), self._yakuFile,
                    self.getGameYaku(self._playerTurn, 'ron')):
                if playerID == 0: #Separated to avoid a strange bug
                    if playerChoice == 'ron':
                        self._ron(0, prevPlayer)
                        return True
                elif self._ai[playerID-1].checkRon(self._lastTile):
                    self._ron(playerID, prevPlayer)
                    return True
        return False
                
    def _checkKan(self, curOrder, playerChoice):
        """ Goes through each player in an anticlockwise direction and sees if
        they want to kan the last tile, lets them do so and returns True if yes,
        returning False if no.

        _checkKan(list of integers, string) -> Boolean

        curOrder is a list containing the three playersID's to check in order.
        playerChoice is a string containing which button the player pressed.

        """
        for playerID in curOrder: #KAN CHECK
            if self._players[playerID].isRiichi():
                return False
            if self._players[playerID].canKan(self._lastTile):
                if playerID == 0: #Separated to avoid a strange bug
                    if playerChoice == 'kan':
                        self._kan(0)
                        return True
                elif self._ai[playerID-1].checkKanOpen(self._lastTile):
                    self._kan(playerID)
                    return True
        return False
                
    def _checkPon(self, curOrder, playerChoice):
        """ Goes through each player in an anticlockwise direction and sees if
        they want to pon the last tile, lets them do so and returns True if yes,
        returning False if no.

        _checkPon(list of integers, string) -> Boolean

        curOrder is a list containing the three playersID's to check in order.
        playerChoice is a string containing which button the player pressed.

        """
        for playerID in curOrder: #PON CHECK
            if self._players[playerID].isRiichi():
                return False
            if self._players[playerID].canPon(self._lastTile):
                if playerID == 0: #Separated to avoid a strange bug
                    if playerChoice == 'pon':
                        self._pon(playerID)
                        return True
                elif self._ai[playerID-1].checkPon(self._lastTile):
                    self._pon(playerID)
                    return True
        return False
                
    def _checkChi(self, playerChoice):
        """ Asks the current player if they want to chi the last tile, lets them
        do so and returns True if yes, returning False if no.
        If the user is the current player, then it takes their choice of tiles
        into account.

        _checkPon(string) -> Boolean

        playerChoice is a string containing which button the player pressed.

        """
        playerID = self._playerTurn
        if self._players[playerID].isRiichi():
            return False
        if playerChoice == 'chi' and playerID == 0:
            self._chi(0, self._highlightTiles)
            return True
        elif playerID != 0:
            choices = self._players[playerID].canChi(self._lastTile)
            if choices: #If they can call chi
                aiChoices = self._ai[playerID-1].checkChi(self._lastTile,
                    choices)
                if aiChoices: #If they will call chi
                    self._chi(playerID, aiChoices)
                    return True
        return False
    
    #DURING TURN CHECKERS
    def _tsumoCheck(self):
        """ Asks the current player if they want to tsumo, lets them do so and
        returns True if yes, returning False if no.

        _tsumoCheck() -> Boolean

        """
        if self._optionsDeny: #If they chose 'cancel' this turn
            return False
        if self._players[self._playerTurn].canTsumo(self.getRoundWind(),
                self._yakuFile, self.getGameYaku(self._playerTurn, 'tsumo')):
            if self._playerTurn == 0:
                self._hudCallButton.enable()
                self._hudCallButton.changeText("Tsumo")
                self._enableCancelButtons()
                self._curStage = 'playerresponse'
            else: #If this is an AI player
                if self._ai[self._playerTurn-1].checkTsumo():
                    self._tsumo(self._playerTurn)
                else:
                    return False
            return True
        else:
            return False

    def _lateKanCheck(self):
        """ Asks the current player if they want to late kan, lets them do so
        and returns True if yes, returning False if no.

        _lateKanCheck() -> Boolean

        """
        if self._players[self._playerTurn].isRiichi(): #Can't kan with riichi
            return False
        if self._optionsDeny: #If they chose 'cancel' this turn
            return False
        kanTile = self._players[self._playerTurn].canKan_la()
        if kanTile: #If we can late an
            if self._playerTurn == 0:
                self._hudKanButton.enable()
                self._hudKanButton.changeText("Late Kan")
                self._enableCancelButtons()
                self._curStage = 'playerresponse'
            else: #If this is an AI player
                if self._ai[self._playerTurn-1].checkKanLate(kanTile):
                    self._kan_la(self._playerTurn)
                else:
                    return False
            return True
        else:
            return False

    def _closedKanCheck(self):
        """ Asks the current player if they want to closed kan, lets them do so
        and returns True if yes, returning False if no.

        _closedKanCheck() -> Boolean

        """
        if self._players[self._playerTurn].isRiichi(): #Can't kan with riichi
            return False
        if self._optionsDeny: #If they chose 'cancel' this turn
            return False
        kanTile = self._players[self._playerTurn].canKan_cl()
        if kanTile: #If we can closed kan
            if self._playerTurn == 0:
                self._hudKanButton.enable()
                self._hudKanButton.changeText("Clos. Kan")
                self._enableCancelButtons()
                self._curStage = 'playerresponse'
            else: #If this is an AI player
                if self._ai[self._playerTurn-1].checkKanClosed(kanTile):
                    self._kan_cl(self._playerTurn)
                else:
                    return False
            return True
        else:
            return False

    def _riichiCheck(self):
        """ Asks the current player if they want to riichi, lets them do so
        and returns True if yes, returning False if no.

        _riichiCheck() -> Boolean

        """
        if self._players[self._playerTurn].isRiichi(): #Obviously, can't riichi
            return False
        if self._optionsDeny: #If they chose 'cancel' this turn
            return False
        if not self._players[self._playerTurn].isClosed():
            return False
        uniqueTiles = self._curWall.getUnique()
        curPlayerID = self._playerTurn
        curPlayer = self._players[curPlayerID]
        if self._players[curPlayerID].isTenpaiFull(uniqueTiles):
            if self._playerTurn == 0:
                self._hudChiButton.enable()
                self._hudChiButton.changeText("Riichi")
                self._enableCancelButtons()
                self._curStage = 'playerresponse'
            else: #If this is an AI player
                curAI = self._ai[self._playerTurn-1]
                if curAI.checkRiichi():
                    self._riichiAI(self._playerTurn, curAI)
                else:
                    return False
            return True
        else:
            return False

    #GAMEPLAY FUNCTIONS
    def _playerDraw(self, playerID):
        """ Lets the given player draw from the wall, and plays the sound.

        _playerDraw(int) -> None

        playerID is the ID of the player who should draw.

        """
        self._players[playerID].draw(self._curWall.drawFromWall())
        self._master.playButtonSound('drawSound')

    def _playerDiscardAni(self, playerID, tileID):
        """ Flash a tile for a few seconds, then discard it from the hand.

        _playerDiscardAni(int, int) -> None

        playerID is the ID of the player who should discard.
        tileID is the index of the tile in the player's hand which should be
        discarded.

        """
        self._startAnimate('flashTile', (playerID, tileID))

    def _playerDiscardEnd(self):
        """ After the flashing of a tile is done, get the tile and discard it.

        _playerDiscardEnd() -> None

        """
        playerID = self._animationInfo[0]
        tileID = self._animationInfo[1]
        self._playerDiscard(playerID, tileID)

    def _playerDiscardEndRiichi(self):
        """ Similar to _playerDiscardEnd, but also declares riichi afterwards.

        _playerDiscardEndRiichi() -> None

        """
        self._playerDiscardEnd()
        uniqueTiles = self._curWall.getUnique()
        self._players[playerID].riichi(uniqueTiles, self._isDouble())

    def _playerDiscard(self, playerID, tileID):
        """ Discards a given tile index from a given player's hand, playing the
        appropriate sound.

        _playerDiscard(int, int) -> None

        playerID is the ID of the player who should discard.
        tileID is the index of the tile in the player's hand which should be
        discarded.

        """
        curPlayer = self._players[playerID]
        self._lastTile = curPlayer.discard(tileID)
        self._master.playButtonSound('discardSound')

    #HIGHLIGHT BUTTON RESPONSES
    def _getChiResponse(self):
        """ Highlights tiles and waits for them to be pressed when the player
        clicks 'chi'. Changes its response depending on how many tiles they've
        chosen.

        _getChiResponse() -> None

        """
        for tileButton in self._hudTileButtons:
            tileButton.unHighlight() #Unhighlight all previous tiles
        if len(self._highlightTiles) == 2:
            #After they click two tiles, try calling chi
            self._turnStartCheck2('chi')
        elif len(self._highlightTiles) == 1:
            #After they click one tile, highlight the remaining choices
            firstChoice = self._highlightTiles[0]
            for choice in self._curChiChoices:
                if choice[0] == firstChoice:
                    self._hudTileButtons[choice[1]].highlight('Chi')
                elif choice[1] == firstChoice:
                    self._hudTileButtons[choice[0]].highlight('Chi')
        else:
            #Before clicking a tile, highlight all related tiles
            for choice in self._curChiChoices:
                for tileInd in choice:
                    self._hudTileButtons[tileInd].highlight('Chi')

    def _getRiichiResponse(self):
        """ Highlights tiles and waits for them to be pressed when the player
        clicks 'riichi'. Changes its response depending on how many tiles
        they've chosen.

        _getRiichiResponse() -> None

        """
        for tileButton in self._hudTileButtons:
            tileButton.unHighlight() #Unhighlight all previous tiles
        if len(self._highlightTiles) == 1:
            #After they click one tile, declare riichi
            self._riichi(0, self._highlightTiles[0])
            self._highlightTiles = []
        else:
            #Before clicking a tile, highlight all related tiles
            uniqueTiles = self._curWall.getUnique()
            possibleTiles = self._players[0].isTenpaiFullPoss(uniqueTiles)
            for tileInd in possibleTiles:
                self._hudTileButtons[tileInd].highlight('Riichi')

    #SUPPORT FUNCTIONS
    def _resetVars(self):
        """ Reset all round-based variables to their initial values.

        _resetVars() -> None

        """
        self._die1 = 1
        self._die2 = 6
        self._curTurn = 1
        self._playerTurn = -1
        self._lastTile = None
        self._playerWon = None #Which player just won
        self._playerLost = None #Which player just lost
        self._endRoundType = 'none'
        self._canDouble = True #Is it possible to double riichi?
        self._optionsDeny = False #Used for cancelling riichi and closed kans
        self._lastDrawWasDead = False
        self._userCanDiscard = False #Can only discard when waiting for input
        self._curWall = Wall(self._repeat, self._suitnum, self._tileFile)

    def _playerOrder(self, startingID):
        """ Given a playerID to start with, returns a list containing the other
        playerID's in anticlockwise order after it.

        _playerOrder(int) -> list of integers

        startingID is the playerID to start this list off with.

        """
        idList = [0,1,2,3]
        return idList[startingID:] + idList[:startingID]

    def _allocateSeatWinds(self, dealerNum):
        """ Given the current dealerID, sets the correct seat winds for all
        players in an anticlockwise direction.

        _allocateSeatWinds(int) -> None

        dealerNum is the ID of the player who is the current dealer.

        """
        windList = [Tile(52), Tile(51), Tile(54), Tile(53)]
        for i, playerID in enumerate(self._playerOrder(dealerNum)):
            self._players[playerID].setSeatWind(windList[i])

    def _getRoundName(self):
        """ Gets the name of the current round, as text.

        _getRoundName() -> string

        """
        roundText = self._curRound[0]
        if self._curRound[1] == 1: roundText += " First Round"
        if self._curRound[1] == 2: roundText += " Second Round"
        if self._curRound[1] == 3: roundText += " Third Round"
        if self._curRound[1] == 4: roundText += " Fourth Round"
        if self._curRound[2] > 0:
            roundText += " -- Bonus " + str(self._curRound[2])
        return roundText

    def _determineSide(self, testPlayer):
        """ Given a playerID, finds which side the last player who discarded is
        on around the table, relative to this player. This side is given as 0
        for 'on the left', 1 for 'in the middle' and 2 for 'on the right'.

        _determineSide(int) -> int

        testPlayer is the playerID from whose perspective we're looking at.

        """
        playerList = self._playerOrder(self._playerTurn)
        lastPlayer = playerList[-1]
        if testPlayer < lastPlayer:
            testPlayer += 4
        return testPlayer - lastPlayer - 1

    def _enableCancelButtons(self):
        """ Enables all the buttons needed to cancel menu buttons.

        _enableCancelButtons() -> None

        """
        self._hudMenuButton.enable()
        self._invisCancelButton.enable()
        self._hudMenuButton.changeText("Cancel")

    def _disableButtons(self):
        """ Disables all menu buttons.

        _disableButtons() -> None

        """
        self._hudPonButton.disable()
        self._hudChiButton.changeText('Chi')
        self._hudChiButton.disable()
        self._hudKanButton.changeText('Kan')
        self._hudKanButton.disable()
        self._hudPonButton.disable()
        self._hudMenuButton.changeText('Menu')
        self._hudMenuButton.disable()
        self._hudCallButton.changeText('Call')
        self._hudCallButton.disable()
        self._invisCancelButton.disable()

    def _deadWallDraw(self):
        """ Draws from the dead wall, returning the tile and playing a sound.

        _deadWallDraw() -> Tile

        """
        self._lastDrawWasDead = True
        self._hudTileButtons = [] #Force this to update
        self._master.playButtonSound('drawSound')
        return self._curWall.deadWallDraw()

    def _isDouble(self):
        """ Returns whether or not the player can double riichi.

        _isDouble() -> Boolean

        """
        return (self._curTurn <= 4) and self._canDouble

    def _deactSpecialYaku(self):
        """ Deactivates ippatsu and double riichi for all players.

        _deactSpecialYaku() -> None

        """
        self._canDouble = False
        for player in self._players:
            player.addRiichiTurns(10) #Should be enough to ensure no ippatsu

    def _incrRound(self):
        """ Increments the current round, returning False if this is the last
        round and true otherwise.

        _incrRound() -> Boolean

        """
        if self._curRound[1] == 4:
            if self._curRound[0] == 'East':
                if self._isJustEastRound:
                    return False
                else:
                    nextName = 'South'
            else:
                return False
            nextNum = 1
        else:
            nextName = self._curRound[0]
            nextNum = self._curRound[1] + 1
        self._curRound = (nextName, nextNum, 0)
        return True

    def _incrBonusRound(self):
        """ Increments the current bonus round, taking the dealer ante score
        with it.

        _incrBonusRound() -> None

        """
        nextBonus = self._curRound[2] + 1
        self._curRound = (self._curRound[0], self._curRound[1], nextBonus)
        self._players[self._curDealer].addScore(-100)

    def _pon(self, playerID):
        """ Declares pon on the last tile for the given playerID, playing sound
        and displaying the related text.

        _pon(int) -> None

        playerID is the ID of the player who is declaring pon.

        """
        self._deactSpecialYaku()
        self._drawTextShort('Pon')
        self._master.playVoiceSound('ponSound')
        side = self._determineSide(playerID)
        self._players[playerID].pon(self._lastTile, side)
        self._playerTurn = playerID
        self._startAnimate('pause', 10)

    def _chi(self, playerID, chosenTiles):
        """ Declares chi on the last tile for the given playerID, playing sound
        and displaying the related text.

        _chi(int, list of tile indexes) -> None

        playerID is the ID of the player who is declaring chi.
        chosenTiles is a list of the tile indexes in the hand which will be
        used for declaring the sequence.

        """
        self._deactSpecialYaku()
        self._drawTextShort('Chi')
        self._master.playVoiceSound('chiSound')
        self._players[playerID].chi(self._lastTile, chosenTiles)
        self._playerTurn = playerID
        self._startAnimate('pause', 10)

    def _kan(self, playerID):
        """ Declares an open kan on the last tile for the given playerID,
        playing sound and displaying the related text.

        _kan(int) -> None

        playerID is the ID of the player who is declaring kan.

        """
        self._deactSpecialYaku()
        self._drawTextShort('Kan')
        self._master.playVoiceSound('kanSound')
        side = self._determineSide(playerID)
        self._players[playerID].kan_op(self._lastTile, side)
        self._players[playerID].draw(self._deadWallDraw())
        self._playerTurn = playerID
        self._startAnimate('pause', 15)

    def _kan_cl(self, playerID):
        """ Declares a closed kan on the last tile for the given playerID,
        playing sound and displaying the related text.

        _kan_cl(int) -> None

        playerID is the ID of the player who is declaring kan.

        """
        self._deactSpecialYaku()
        self._drawTextShort('Kan')
        self._master.playVoiceSound('kanSound')
        self._players[playerID].kan_cl()
        self._players[playerID].draw(self._deadWallDraw())
        self._startAnimate('pause', 15)

    def _kan_la(self, playerID):
        """ Declares a late kan on the last tile for the given playerID,
        playing sound and displaying the related text.

        _kan_la(int) -> None

        playerID is the ID of the player who is declaring kan.

        """
        self._deactSpecialYaku()
        self._drawTextShort('Kan')
        self._master.playVoiceSound('kanSound')
        self._players[playerID].kan_la()
        self._players[playerID].draw(self._deadWallDraw())
        self._startAnimate('pause', 15)

    def _riichi(self, playerID, toDiscard):
        """ Declares riichi on the last tile for the given playerID,
        playing sound and displaying the related text. This function is used for
        the user.

        _riichi(int, int) -> None

        playerID is the ID of the player who is declaring riichi.
        toDiscard is the index of which tile should be discarded in the riichi
        player's hand.

        """
        self._drawTextShort('Riichi')
        self._master.playVoiceSound('riichiSound')
        uniqueTiles = self._curWall.getUnique()
        self._playerDiscard(playerID, toDiscard)
        self._players[playerID].riichi(uniqueTiles, self._isDouble())
        self._curStage = 'turnend'

    def _riichiAI(self, playerID, curAI):
        """ Declares riichi on the last tile for the given playerID,
        playing sound and displaying the related text. This function is used for
        AI.

        _riichi(int, NoneAI) -> None

        playerID is the ID of the player who is declaring riichi.
        curAI is the AI who should be asked which tile they want to discard.

        """
        self._drawTextShort('Riichi')
        self._master.playVoiceSound('riichiSound')
        uniqueTiles = self._curWall.getUnique()
        possTiles = self._players[playerID].isTenpaiFullPoss(uniqueTiles)
        toDiscard = curAI.checkRiichiDiscard(possTiles)
        self._startAnimate('flashTileRiichi', (playerID, toDiscard))

    def _tsumo(self, playerID):
        """ Declares tsumo on the last tile for the given playerID, playing
        sound and displaying the related text.

        _tsumo(int) -> None

        playerID is the ID of the player who is declaring tsumo.

        """
        self._drawTextFinal('Tsumo')
        self._master.playVoiceSound('tsumoSound')
        self._playerWon = playerID
        self._startAnimate('pause', 100)
        self._curStage = 'roundend'
        self._endRoundType = 'tsumo'
        
    def _ron(self, playerID, stolenID):
        """ Declares ron on the last tile for the given playerID, playing sound
        and displaying the related text.

        _ron(int, int) -> None

        playerID is the ID of the player who is declaring ron.
        stolenID is the ID of the player who the tile is being taken from.

        """
        self._drawTextFinal('Ron')
        self._master.playVoiceSound('ronSound')
        self._players[playerID].draw(self._lastTile)
        self._playerWon = playerID
        self._playerLost = stolenID
        self._startAnimate('pause', 100)
        self._curStage = 'roundend'
        self._endRoundType = 'ron'

    #BUTTON PRESSED FUNCTIONS
    def _buttMenu(self):
        """ Runs the appropriate functions and actions when the menu button is
        pressed.

        _buttMenu() -> None

        """
        if self._hudMenuButton.getText() == 'Continue': #Go to next round
            self._roundFinalise()
        elif self._hudMenuButton.getText() == 'Cancel': #Cancel button
            if (self._hudCallButton.getText() == 'Tsumo' or
                    self._hudKanButton.getText() == 'Clos. Kan' or
                    self._hudKanButton.getText() == 'Late Kan' or
                    self._hudChiButton.getText() == 'Riichi'): #If user's turn
                self._curStage = 'turnmid'
                self._optionsDeny = True
            else: #If other player's discard
                self._curStage = 'turnstart'
        elif self._hudMenuButton.getText() == 'Menu':
            self.popupDialog("WindowGameMenu")
        self._disableButtons()

    def _buttSkip(self):
        """ Runs the appropriate functions and actions when the skip button is
        pressed. In other words, skips to the end of the score change thingo.

        _buttSkip() -> None

        """
        if self._curStage == 'scorechange':
            self._skipScoreButton.disable()
            for player in self._players:
                player.finScoreDiff()
            self._curStage = 'playerresponse'

    def _buttPon(self):
        """ Declares pon when the pon button is clicked.

        _buttPon() -> None

        """
        self._turnStartCheck2('pon')
        self._disableButtons()

    def _buttChi(self):
        """ Declares chi/riichi when this button is clicked.

        _buttChi() -> None

        """
        curText = self._hudChiButton.getText()
        if curText == 'Riichi': #If currently is a riichi button
            self._getRiichiResponse()
        else: #If currently is a chi button
            self._getChiResponse()
        self._disableButtons()

    def _buttKan(self):
        """ Declares kan when this button is clicked.

        _buttKan() -> None

        """
        curText = self._hudKanButton.getText()
        if curText == 'Clos. Kan': #If currently is a closed kan button
            self._kan_cl(0)
            self._curStage = 'turnmid'
        elif curText == 'Late Kan': #If currently is a late kan button
            self._kan_la(0)
            self._curStage = 'turnmid'
        else: #If currently is an open kan button
            self._turnStartCheck2('kan')
        self._disableButtons()

    def _buttCall(self):
        """ Calls on the last tile, either tsumo or ron.

        _buttCall() -> None

        """
        if self._hudCallButton.getText() == 'Ron':
            self._turnStartCheck2('ron')
        elif self._hudCallButton.getText() == 'Tsumo':
            self._tsumo(0)
        self._disableButtons()

    def _buttTile(self, tileInd):
        """ Runs when a tile button is clicked. Either discards the current tile
        or, if the tiles are currently being highlighted, runs the appropriate
        response function.

        _buttTile(int) -> None

        tileInd is the index of which tile was pressed.

        """
        if self._hudTileButtons[tileInd].isHighlight(): #If the tile is h/l
            self._highlightTiles.append(tileInd)
            if self._hudTileButtons[tileInd].getHighlightType() == 'Riichi':
                self._getRiichiResponse()
            else:
                self._getChiResponse()
        else: #If this is just a normal discard
            self._userCanDiscard = False
            self._playerDiscard(0, tileInd)
            self._curStage = 'turnend'
            
    #ANIMATION FUNCTIONS
    def _drawTextShort(self, text):
        """ Draws the given text on the screen for a short period of time,
        animated with a faded background and scrolling down the screen.

        _drawTextShort(string) -> None

        text is the text to display on screen.

        """
        self._aniText.append(AnimatedText(text, mahjongGlobals.OFFWHITE,
            mahjongGlobals.HUDFONT, 25, 1, 30))
        self._aniBack.append(FadeInOut(0, 0, (885,700), mahjongGlobals.BLACK,
            50, 1, 30))
    
    def _drawTextMid(self, text):
        """ Draws the given text on the screen for a middling period of time,
        animated with a faded background and scrolling down the screen.

        _drawTextMid(string) -> None

        text is the text to display on screen.

        """
        self._aniText.append(AnimatedText(text, mahjongGlobals.OFFWHITE,
            mahjongGlobals.HUDFONT, 25, 1, 50))
        self._aniBack.append(FadeInOut(0, 0, (885,700), mahjongGlobals.BLACK,
            130, 1, 50))

    def _drawTextFinal(self, text):
        """ Draws the given text on the screen for an extended period of time,
        animated with a faded background and scrolling down the screen.

        _drawTextFinal(string) -> None

        text is the text to display on screen.

        """
        self._aniText.append(AnimatedText(text, mahjongGlobals.OFFWHITE,
            mahjongGlobals.HUDFONT, 35, 1, 100))
        self._aniBack.append(FadeInOut(0, 0, (885,700), mahjongGlobals.BLACK,
            170, 1, 100))
    
    def _startAnimate(self, aniType, aniInfo):
        """ Prepares to animate the given animation using the provided info.
        Plays a sound if the animation has an associated sound.

        _startAnimate(string, object) -> None

        aniType is which animation to display.
        aniInfo is an object (usually an int or a tuple) with related info
        needed for displaying the animation of type aniType.

        """
        self._curStageTimer = 0
        self._animation = aniType
        self._animationInfo = aniInfo
        if aniType == 'dice':
            self._master.playButtonSound('diceSound')

    def _animate(self, aniType):
        """ Animates the animation of type aniType for this frame. Ends the
        animation process if the animation is over.

        _animate(string) -> None

        aniType is which animation to display.

        """
        if aniType == 'dice':
            if self._dieTimer():
                self._animation = False
        elif aniType == 'flashTile':
            if self._flashTimer():
                self._animation = False
                self._playerDiscardEnd()
        elif aniType == 'flashTileRiichi':
            if self._flashTimer():
                self._animation = False
                self._playerDiscardEndRiichi()
        elif aniType == 'pause':
            if self._curStageTimer == self._animationInfo:
                self._animation = False

    def _dieTimer(self):
        """ Animates a dice roll for 40 frames. Does this by setting the dice
        variables to random values every 3 frames. Returns whether the roll is
        done.

        _dieTimer() -> Boolean

        """
        if self._curStageTimer < 40: #40 being 40 frames for this animation
            if self._curStageTimer%3 == 0:
                self._die1 = random.randint(1, 6)
                self._die2 = random.randint(1, 6)
            return False
        else:
            return True

    def _flashTimer(self):
        """ Animates a tile flashing for 15 frames. Does this by setting a
        nodraw variable to and away from the relevant tile every 4 frames.
        Returns whether the flashing is done.
        done.

        _flashTimer() -> Boolean

        """
        if self._curStageTimer < 15: #15 being 15 frames for this animation
            if self._curStageTimer%4 == 0:
                self._noDraw = self._animationInfo
            elif self._curStageTimer%4 == 2:
                self._noDraw = (-1, -1)
            return False
        else:
            return True

    #GENERAL DRAWING FUNCTIONS
    def _loadTileImg(self, tileToLoad):
        """ Loads a tile image given a tile.

        _loadTileImg(Tile) -> Surface

        tileToLoad is the tile whose image should be loaded.

        """
        tileFN = str(tileToLoad.getUniqueID()) + ".png"
        return self._tileImgDict[tileFN]

    #DISCARD DRAWING FUNCTIONS
    def _getDiscard(self, player):
        """ Draws a surface for the given player's discard pile.

        _getDiscard(PlayerScore) -> Surface

        player is the player whose discard pile should be drawn.

        """
        discardList = player.getDiscardPile()
        riichiTilePos = player.getRiichiPos()
        size = (mahjongGlobals.TILEWIDTH*10, mahjongGlobals.TILEHEIGHT*3)
        tempSurface = pygame.Surface(size, pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        curXtop, curXmid, curXbtm = 0, 0, 0
        for i, tile in enumerate(discardList):
            #Go through each tile and draw it in turn
            tileSurface = self._loadTileImg(tile)
            if i == riichiTilePos: #Sideways if they declared riichi here
                currentWidth = mahjongGlobals.TILEHEIGHT
                tileSurface = pygame.transform.rotate(tileSurface, 90)
            else:
                currentWidth = mahjongGlobals.TILEWIDTH
            if 0 <= i < 6: #Top row           
                tempSurface.blit(tileSurface, (curXtop, 0))
                curXtop += currentWidth
            elif 6 <= i < 12: #Middle row
                tempSurface.blit(tileSurface, (curXmid,
                    mahjongGlobals.TILEHEIGHT))
                curXmid += currentWidth
            elif 12 <= i: #Bottom row
                tempSurface.blit(tileSurface, (curXbtm,
                    mahjongGlobals.TILEHEIGHT*2))
                curXbtm += currentWidth
        return tempSurface

    #WALL DRAWING FUNCTIONS
    def _getWallSection(self, side):
        """ Draws a surface for the given wall side. Displays darkened tiles if
        they are part of the dead wall.

        _getWallSection(string) -> Surface

        side is which side should be drawn, as in 'top', 'bottom' etc.

        """
        (curIndex, endIndex) = self._curWall.getWallPart(side)
        size = (mahjongGlobals.TILEWIDTH*(endIndex-curIndex)/2,
            mahjongGlobals.TILEHEIGHT + 10)
        curX = 0
        tempSurface = pygame.Surface(size, pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        while curIndex < endIndex:
            #Go through each tile between the start and end indexes in the wall
            if self._curWall[curIndex]: #If the tile exists
                if curIndex%2 == 0: #Only draw every second tile
                    if self._curWall.indexIsDoraInd(curIndex): #dora flip
                        tileSurface = self._loadTileImg(self._curWall[curIndex])
                        tempSurface.blit(tileSurface, (curX, 10))
                    elif self._curWall.indexInDead(curIndex): #dead wall
                        tileSurface = self._tileImgDict[
                            mahjongGlobals.TILEBACKDEADIMG]
                        tempSurface.blit(tileSurface, (curX, 10))
                    else: #normal tile
                        tileSurface = self._tileImgDict[
                            mahjongGlobals.TILEBACKIMG]
                        tempSurface.blit(tileSurface, (curX, 0))
                    curX += mahjongGlobals.TILEWIDTH
                elif not self._curWall[curIndex-1]: #Draw small tiles
                    #This only runs when the previous tile doesn't exist:
                    #Ie. only when you can see this tile.
                    curX -= mahjongGlobals.TILEWIDTH
                    scaleHeight = int(round(mahjongGlobals.TILEHEIGHT*0.8))
                    scaleWidth = int(round(mahjongGlobals.TILEWIDTH*0.8))
                    if self._curWall.indexInDead(curIndex): #Dead wall check
                        if self._curWall.indexInDead(curIndex-1):
                            scaleX = curX
                        else:
                            scaleX = int(round(curX +
                                mahjongGlobals.TILEWIDTH*0.2))
                        scaleY = int(round(mahjongGlobals.TILEHEIGHT*0.1)) + 10
                        tileSurface = self._tileImgDict[
                            mahjongGlobals.TILEBACKDEADIMG]
                    else: #Normal wall check
                        scaleX = int(round(curX + mahjongGlobals.TILEWIDTH*0.2))
                        scaleY = int(round(mahjongGlobals.TILEHEIGHT*0.1))
                        tileSurface = self._tileImgDict[
                            mahjongGlobals.TILEBACKIMG]
                    tileSurface = pygame.transform.scale(tileSurface,
                        (scaleWidth, scaleHeight))
                    tempSurface.blit(tileSurface, (scaleX, scaleY))
                    curX += mahjongGlobals.TILEWIDTH
            elif curIndex%2 == 0: #Otherwise, just skip it
                curX += mahjongGlobals.TILEWIDTH
            curIndex += 1
        return tempSurface


    #AI HAND DRAWING FUNCTIONS         
    def _getAIHandMain(self, handMutable, doShow, tileToFlash):
        """ Draws a surface for the given AI hand, just for the main part.

        _getAIHandMain(list of Tiles, Boolean, int) -> Surface

        handMutable is the mutable part of the player's hand.
        doShow is whether or not to have the hand face up.
        tileToFlash is the index of which tile should be skipped over for the
        flashing animation.

        """
        size = (mahjongGlobals.TILEWIDTH*len(handMutable),
            mahjongGlobals.TILEHEIGHT)
        tempSurface = pygame.Surface(size, pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        for i, tile in enumerate(handMutable):
            #For all tiles in the hand
            if doShow: #If the hand should be open to all
                tileSurface = self._loadTileImg(tile)
            else:
                tileSurface = self._tileImgDict[mahjongGlobals.TILEBACKIMG]
            if not tileToFlash == i:
                tempSurface.blit(tileSurface, (mahjongGlobals.TILEWIDTH*i,0))
        return tempSurface

    def _getAIHandCurMeld(self, tileColl):
        """ Draws a surface for the given meld in the AI hand.

        _getAIHandCurMeld(TileCollection) -> Surface

        tileColl is the TileCollection that should be drawn.

        """
        size = (mahjongGlobals.TILEWIDTH*tileColl.getAmtUpways()+
                mahjongGlobals.TILEHEIGHT*tileColl.getAmtSideways(),
                mahjongGlobals.TILEHEIGHT)
        tempSurface = pygame.Surface(size, pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        curXpos = 0
        sideSpacing = mahjongGlobals.TILEHEIGHT-mahjongGlobals.TILEWIDTH
        for i, tile in enumerate(tileColl.getTileList()):
            #For all tiles in the meld
            if tileColl.getType() == 'kan_cl' and ((i == 1) or (i == 2)):
                #Flipped tiles, for closed kans
                tileSurface = self._tileImgDict[mahjongGlobals.TILEBACKIMG]
            else:
                tileSurface = self._loadTileImg(tile)
            if i == tileColl.getSide(): #Sideways tile
                tileSurface = pygame.transform.rotate(tileSurface, 90)
                tempSurface.blit(tileSurface, (curXpos, sideSpacing))
                curXpos += mahjongGlobals.TILEHEIGHT
            else:
                tempSurface.blit(tileSurface, (curXpos, 0))
                curXpos += mahjongGlobals.TILEWIDTH
        return (tempSurface, size[0])

    def _getAIHandAllMelds(self, handImmutable):
        """ Draws a surface for the all open melds in the AI hand.
        Note that this goes backwards, with the first melds on the right and
        later ones further to the left.
        Also note that the hand will be HANDWIDTH wide, with empty space on
        the left.

        _getAIHandCurMeld(list of TileCollections) -> Surface

        handImmutable is the immutable portion of the player's hand.

        """
        curX = mahjongGlobals.HANDWIDTH
        tempSurface = pygame.Surface((mahjongGlobals.HANDWIDTH,
            mahjongGlobals.TILEHEIGHT), pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        for tileColl in handImmutable:
            #For all tilecollections in their hand
            (tileSurface, tileWidth) = self._getAIHandCurMeld(tileColl)
            curX -= tileWidth
            tempSurface.blit(tileSurface, (curX, 0))
        return tempSurface

    def _getAIHand(self, playerID):
        """ Draws a surface for the given AI player's hand.

        _getAIHand(int) -> Surface

        playerID is the ID of which player's hand should be drawn.

        """
        player = self._players[playerID]
        tempSurface = pygame.Surface((mahjongGlobals.HANDWIDTH,
            mahjongGlobals.TILEHEIGHT), pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        tileToFlash = -1
        if self._noDraw[0] == playerID: #This player has a flashing tile
            tileToFlash = self._noDraw[1]
        tempMain = self._getAIHandMain(player.getMutable(),
            player.getShowHand(), tileToFlash)
        tempMeld = self._getAIHandAllMelds(player.getImmutable())
        tempSurface.blit(tempMain, (0, 0)) #Get the main part
        tempSurface.blit(tempMeld, (0, 0)) #Get the immutable part
        return tempSurface


    #USER PLAYER HAND BUTTON FUNCTIONS
    #SEPARATED FROM AI FUNCTIONS FOR EASE OF USE AND SIZING
    def _getPlayerHandCurMeld(self, tileColl):
        """ Draws a surface for the given meld in the user's hand. Compare with
        _getAIHandCurMeld.

        _getPlayerHandCurMeld(TileCollection) -> Surface

        tileColl is the TileCollection that should be drawn.

        """
        size = (mahjongGlobals.PLAYERTILEWIDTH*tileColl.getAmtUpways()+
                mahjongGlobals.PLAYERTILEHEIGHT*tileColl.getAmtSideways(),
                mahjongGlobals.PLAYERTILEHEIGHT)
        tempSurface = pygame.Surface(size, pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        curXpos = 0
        sideSpacing = (mahjongGlobals.PLAYERTILEHEIGHT -
            mahjongGlobals.PLAYERTILEWIDTH)
        for i, tile in enumerate(tileColl.getTileList()):
            if tileColl.getType() == 'kan_cl' and ((i == 1) or (i == 2)):
                #Flipped tiles, for closed kans
                tileSurface = self._tileImgDict[mahjongGlobals.TILEBACKIMG]
            else:
                tileSurface = self._loadTileImg(tile)
            tileSurface = pygame.transform.scale(tileSurface,
                (mahjongGlobals.PLAYERTILEWIDTH,
                 mahjongGlobals.PLAYERTILEHEIGHT))
            if i == tileColl.getSide():
                tileSurface = pygame.transform.rotate(tileSurface, 90)
                tempSurface.blit(tileSurface, (curXpos, sideSpacing))
                curXpos += mahjongGlobals.PLAYERTILEHEIGHT
            else:
                tempSurface.blit(tileSurface, (curXpos, 0))
                curXpos += mahjongGlobals.PLAYERTILEWIDTH
        return (tempSurface, size[0])

    def _getPlayerHandMelds(self):
        """ Draws a surface for the all open melds in the user player's hand.
        Note that this goes backwards, with the first melds on the right and
        later ones further to the left.
        Also note that the hand will be PLAYERHANDWIDTH wide, with empty space
        on the left.

        _getPlayerHandMelds() -> Surface

        """
        handImmutable = self._players[0].getImmutable()
        curX = mahjongGlobals.PLAYERHANDWIDTH
        tempSurface = pygame.Surface((mahjongGlobals.PLAYERHANDWIDTH,
            mahjongGlobals.PLAYERTILEHEIGHT), pygame.SRCALPHA, 32)
        tempSurface.convert_alpha()
        for tileColl in handImmutable:
            (tileSurface, tileWidth) = self._getPlayerHandCurMeld(tileColl)
            curX -= tileWidth
            tempSurface.blit(tileSurface, (curX, 0))
        return tempSurface

    def _getPlayerButtons(self):
        """ Obtains a list of all buttons which should be drawn onto the screen
        for the player's hand, so that they can choose one to discard.

        _getPlayerButtons() -> list of Buttons

        """
        handMutable = self._players[0].getMutable()
        handMaxsize = self._players[0].getHandsize()
        handCursize = self._players[0].getTileNum()
        if handCursize == handMaxsize:
            tileSpace = True
        else:
            tileSpace = False
        curX = 195
        curY = 710
        tileList = []
        for i, tile in enumerate(handMutable):
            curButtonImg = self._loadTileImg(tile)
            curButton = ButtonTile(self._master,curX,curY,
            (mahjongGlobals.PLAYERTILEWIDTH,mahjongGlobals.PLAYERTILEHEIGHT),
            self._buttTile,i,curButtonImg)
            tileList.append(curButton)
            curX += mahjongGlobals.PLAYERTILEWIDTH
            if tileSpace and i == len(handMutable) - 2:
                #Add a gap for their last drawn tile
                curX += 10
        return tileList

    #UI DRAWING FUNCTIONS
    def _getGameInfo(self):
        """ Draws a surface for the game info; the frame shown in the bottom
        left of the screen.

        _getGameInfo() -> Surface

        """
        tempSurface = pygame.Surface((182, 64))
        tempSurface.blit(self._hudGameInfoImg, (0,0))
        curColour = mahjongGlobals.WHITE
        curFont = pygame.font.Font(mahjongGlobals.HUDFONT, 17)
    
        #Text for the current round name.
        roundText = self._getRoundName()
        roundDraw = curFont.render(roundText, True, curColour)
        tempSurface.blit(roundDraw, (10, 5))

        #Text for the turns remaining.
        turnsText = "Turns Remaining -- " + str(self._curWall.getTilesRemaining())
        turnsDraw = curFont.render(turnsText, True, curColour)
        tempSurface.blit(turnsDraw, (10, 30))
        return tempSurface

    def _getPlayerInfo(self, playerID):
        """ Draws a surface for the given player info; the frames shown on the
        right side of the screen.

        _getPlayerInfo(int) -> Surface

        playerID is the ID of the player whose info should be gotten.

        """
        tempSurface = pygame.Surface((139, 164))
        curPlayer = self._players[playerID]
        if self._playerTurn == playerID:
            tempSurface.blit(self._hudRightLightImg, (0,0))
            curColour = mahjongGlobals.BLACK
        else:
            tempSurface.blit(self._hudRightImg, (0,0))
            curColour = mahjongGlobals.WHITE
        curFont = pygame.font.Font(mahjongGlobals.HUDFONT, 17)

        #Text for name/ type of player
        nameText = curPlayer.getName()
        nameDraw = curFont.render(nameText, True, curColour)
        tempSurface.blit(nameDraw, (10, 10))
        if playerID == 0:
            typeText = "(You)"
        elif playerID == 1:
            typeText = self._p1ai
        elif playerID == 2:
            typeText = self._p2ai
        elif playerID == 3:
            typeText = self._p3ai
        typeDraw = curFont.render(typeText, True, curColour)
        tempSurface.blit(typeDraw, (15, 30))

        #Picture for seat wind
        if not (self._curStage == "roundstart1" or
                self._curStage == "roundstart2"):
            curWind = curPlayer.getSeatWind()
            windDraw = self._loadTileImg(curWind)
            tempSurface.blit(windDraw, (90, 35))

        #Text for score
        scoreText = "Score: " + str(curPlayer.getScore())
        scoreDraw = curFont.render(scoreText, True, curColour)
        tempSurface.blit(scoreDraw, (10, 70))

        #Text for rounds won
        roundText = "Rounds Won: " + str(curPlayer.getAmountOfWins())
        roundDraw = curFont.render(roundText, True, curColour)
        tempSurface.blit(roundDraw, (10, 90))

        #Text for riichi and dealer
        if curPlayer.isRiichi():   
            riichiText = "(riichi)"
            riichiDraw = curFont.render(riichiText, True, curColour)
            tempSurface.blit(riichiDraw, (10, 110))
        if playerID == self._curDealer:
            dealerText = "(dealer)"
            dealerDraw = curFont.render(dealerText, True, curColour)
            tempSurface.blit(dealerDraw, (50, 130))
        
        return tempSurface

    #OVERALL DRAWING FUNCTION
    def returnSurface(self):
        """ Returns the surface for this particular GameScreen. Does so by
        drawing all relevant data to the 'screen', which it then returns as a
        surface.

        returnSurface() -> Surface

        """
        #First, define the blank surface
        tempSurface = pygame.Surface(mahjongGlobals.SCREENSIZE)
        
        #Draw back
        tempSurface.blit(self.back, (0, 0))

        #Draw dice
        die1FN = str(self._die1) + ".gif"
        die2FN = str(self._die2) + ".gif"
        tempSurface.blit(self._diceImgDict[die1FN], (470,375))
        tempSurface.blit(self._diceImgDict[die2FN], (475,407))

        #Draw carryover sticks
        curFont = pygame.font.Font(mahjongGlobals.HUDFONT, 20)
        curColour = mahjongGlobals.WHITE
        text1 = curFont.render(" x " + str(self._riichiStore), True, curColour)
        text2 = curFont.render(" x " + str(self._bonusStore), True, curColour)
        tempSurface.blit(self._riichiTinyImg, (355,335))
        tempSurface.blit(text1, (400,345))
        tempSurface.blit(self._bonusTinyImg, (355,385))
        tempSurface.blit(text2, (400,395))

        #Riichi Sticks
        if self._players[0].isRiichi():
            tempSurface.blit(self._riichiImg, (342,460))
        if self._players[1].isRiichi():
            tempSurface.blit(self._riichiVertImg, (570,287))
        if self._players[2].isRiichi():
            tempSurface.blit(self._riichiImg, (342,295))
        if self._players[3].isRiichi():
            tempSurface.blit(self._riichiVertImg, (295,287))

        #Draw hand names
        curFont = pygame.font.Font(mahjongGlobals.HUDFONT, 20)
        curColour = mahjongGlobals.WHITE
        p1Draw = curFont.render("CPU Player 1", True, curColour)
        p1Draw = pygame.transform.rotate(p1Draw, 90)
        p2Draw = curFont.render("CPU Player 2", True, curColour)
        p3Draw = curFont.render("CPU Player 3", True, curColour)
        p3Draw = pygame.transform.rotate(p3Draw, 270)
        tempSurface.blit(p1Draw, (860, 600))
        tempSurface.blit(p2Draw, (700, 10))
        tempSurface.blit(p3Draw, (10, 70))
        
        #Draw discards
        p0DiscardSurface = self._getDiscard(self._players[0])
        p1DiscardSurface = self._getDiscard(self._players[1])
        p1DiscardSurface = pygame.transform.rotate(p1DiscardSurface, 90)
        p2DiscardSurface = self._getDiscard(self._players[2])
        p2DiscardSurface = pygame.transform.rotate(p2DiscardSurface, 180)
        p3DiscardSurface = self._getDiscard(self._players[3])
        p3DiscardSurface = pygame.transform.rotate(p3DiscardSurface, 270)
        tempSurface.blit(p0DiscardSurface, (337,490))
        tempSurface.blit(p1DiscardSurface, (600,142))
        tempSurface.blit(p2DiscardSurface, (197,150))
        tempSurface.blit(p3DiscardSurface, (150,282))

        #Draw wall
        bottomWallSurface = self._getWallSection('bottom')
        bottomWallSurface = pygame.transform.rotate(bottomWallSurface, 180)
        leftWallSurface = self._getWallSection('left')
        leftWallSurface = pygame.transform.rotate(leftWallSurface, 90)
        topWallSurface = self._getWallSection('top')
        rightWallSurface = self._getWallSection('right')
        rightWallSurface = pygame.transform.rotate(rightWallSurface, 270)
        tempSurface.blit(bottomWallSurface, (145,630))
        tempSurface.blit(rightWallSurface, (740,90))
        tempSurface.blit(topWallSurface, (145,90))
        tempSurface.blit(leftWallSurface, (90,90))
        
        #Draw ai hands
        ai1HandSurface = self._getAIHand(1)
        ai1HandSurface = pygame.transform.rotate(ai1HandSurface, 90)
        ai2HandSurface = self._getAIHand(2)
        ai2HandSurface = pygame.transform.rotate(ai2HandSurface, 180)
        ai3HandSurface = self._getAIHand(3)
        ai3HandSurface = pygame.transform.rotate(ai3HandSurface, 270)
        tempSurface.blit(ai1HandSurface, (810,35))
        tempSurface.blit(ai2HandSurface, (117,30))
        tempSurface.blit(ai3HandSurface, (30,35))

        #Draw UI
        #Sidebar
        tempSurface.blit(self._getPlayerInfo(0), (885,0))
        tempSurface.blit(self._hudRightSepImg, (885,164))
        tempSurface.blit(self._getPlayerInfo(1), (885,168))
        tempSurface.blit(self._hudRightSepImg, (885,332))
        tempSurface.blit(self._getPlayerInfo(2), (885,336))
        tempSurface.blit(self._hudRightSepImg, (885,500))
        tempSurface.blit(self._getPlayerInfo(3), (885,504))
        tempSurface.blit(self._hudRightImg, (885,668))
        tempSurface.blit(self._hudRightSepImg, (885,668))

        #Bottom bar
        tempSurface.blit(self._hudSepImg, (0,700))
        tempSurface.blit(self._hudMiniSepVertImg, (183,704))
        tempSurface.blit(self._hudMiniSepVertImg, (885,704))
        tempSurface.blit(self._hudMiniSepImg, (887,735))
        tempSurface.blit(self._hudMiniSepVertImg, (955,704))
        tempSurface.blit(self._hudMiniSepImg, (957,735))
        tempSurface.blit(self._getGameInfo(), (0,704))
        tempSurface.blit(self._hudHandBackImg, (185,704))

        #Player hand melds
        playerHandSurface = self._getPlayerHandMelds()
        tempSurface.blit(playerHandSurface, (195,710))

        #Buttons
        self.clearButtons()
        #Tile Buttons
        currentHandLen = len(self._players[0].getMutable())
        oldHandLen = len(self._hudTileButtons)
        if currentHandLen != oldHandLen: #Update if hand tiles change
            self._hudTileButtons = []
            for button in self._getPlayerButtons():
                self._hudTileButtons.append(button)
        for button in self._hudTileButtons:
            #Add all known buttons to the screen
            self.addButton(button)
            if self._userCanDiscard or button.isHighlight():
                #If the button is highlighted (ie. when choosing for chi/riichi)
                #or if the player can discard, enable the button for discarding
                button.enable()
            else:
                button.disable()
        #UI Buttons
        self.addButton(self._hudMenuButton)
        self.addButton(self._hudPonButton)
        self.addButton(self._hudChiButton)
        self.addButton(self._hudKanButton)
        self.addButton(self._hudCallButton)
        self.addButton(self._invisCancelButton)
        #Draw buttons
        for i, button in enumerate(self.buttonList):
            doSelect = (i == self.curButtonSel)
            curSurface = button.returnSurface(doSelect)
            curPos = button.getPos()
            tempSurface.blit(curSurface, curPos)

        #Draw messages/pop up nonsense
        updateBack = []
        for back in self._aniBack:
            if back.update():
                updateBack.append(back)
        if updateBack: #Only draw the first one
            curSurface = updateBack[0].returnSurface()
            curPos = updateBack[0].getPos()
            tempSurface.blit(curSurface, curPos)
        self._aniBack = updateBack
            
        updateList = []
        for message in self._aniText:
            shouldDisplay = message.update()
            if shouldDisplay:
                curSurface = message.returnSurface()
                curPos = message.getCoords(445, 370)
                tempSurface.blit(curSurface, curPos)
                updateList.append(message)
        self._aniText = updateList
        return tempSurface

    #SAVE/LOAD GAME FUNCTIONS
    def saveGame(self):
        """ Saves the current game in progress to the files located in
        SAVEGAMELOC and similar. This can only be run on the player's turn,
        during the 'choose a discard' phase.

        saveGame() -> None

        """
        #Save main data
        mainFile = open(mahjongGlobals.SAVEGAMELOC, "w")
        infoStore = []
        infoStore.append('self._curRound')
        infoStore.append('self._riichiStore')
        infoStore.append('self._bonusStore')
        infoStore.append('self._curDealer')
        infoStore.append('self._winTable')
        infoStore.append('self._playerName')
        infoStore.append('self._p1ai')
        infoStore.append('self._p2ai')
        infoStore.append('self._p3ai')
        infoStore.append('self._isJustEastRound')
        infoStore.append('self._bgImgLoc')
        infoStore.append('self._die1')
        infoStore.append('self._die2')
        infoStore.append('self._curTurn')
        infoStore.append('self._playerTurn')
        infoStore.append('self._lastTile')
        infoStore.append('self._canDouble')
        infoStore.append('self._optionsDeny')
        infoStore.append('self._lastDrawWasDead')
        for info in infoStore:
            mainFile.write(self._getRunnableLine(info))
            mainFile.write('\n')
        mainFile.close()

        #Save each player's data
        self._players[0].saveData(mahjongGlobals.SAVEP1LOC)
        self._players[1].saveData(mahjongGlobals.SAVEP2LOC)
        self._players[2].saveData(mahjongGlobals.SAVEP3LOC)
        self._players[3].saveData(mahjongGlobals.SAVEP4LOC)

        #Save the wall's data
        self._curWall.saveData(mahjongGlobals.SAVEWALLLOC)

    def _getRunnableLine(self, varName):
        """ Converts the given variable into a string line which, when run,
        sets the variable to its own value.

        e.g: If we had some variable x = 4, running _getRunnableLine('x') would
             return the string 'x = 4'

        _getRunnableLine(string) -> string

        varName is the name of the variable to convert, as a string.

        """
        value = eval(varName)
        value = repr(value)
        return varName + ' = ' + value
        
    def loadGame(self):
        """ Loads a previously saved game from the files located in
        SAVEGAMELOC and similar.

        loadGame() -> None

        """
        #Load the main data
        mainFile = open(mahjongGlobals.SAVEGAMELOC, "rU")
        for line in mainFile:
            exec(line) #Runs all those lines saved with _getRunnableLine
        mainFile.close()

        #Set some required default starting variables
        self._userCanDiscard = True
        self._hudMenuButton.enable()
        self._curStage = 'playerresponse'
        self._playerWon = None
        self._playerLost = None
        self._endRoundType = 'none'
        self._players = []

        #Load each player's data
        self._players.append(PlayerScore(None, None, None, None, None, None,
            mahjongGlobals.SAVEP1LOC))
        self._players.append(PlayerScore(None, None, None, None, None, None,
            mahjongGlobals.SAVEP2LOC))
        self._players.append(PlayerScore(None, None, None, None, None, None,
            mahjongGlobals.SAVEP3LOC))
        self._players.append(PlayerScore(None, None, None, None, None, None,
            mahjongGlobals.SAVEP4LOC))

        #Load each AI
        exec('ai1 = ' + self._p1ai + '(self, 1)')
        exec('ai2 = ' + self._p2ai + '(self, 2)')
        exec('ai3 = ' + self._p3ai + '(self, 3)')
        self._ai = [ai1, ai2, ai3]

        #Load the wall's data
        self._curWall = Wall(None, None, None, mahjongGlobals.SAVEWALLLOC)

        #(Note that the None values in the above are used to simply space out
        # the arguments given to PlayerScore and Wall; without them, the
        # constructor would poo itself, though their actual values are quite
        # irrelevant as they are ignored when the last flag is defined.)
        
    #GETTER FUNCTIONS
    def getPlayer(self, playerID):
        """ Returns the player at playerID. """
        return self._players[playerID]

    def getBackImgLoc(self):
        """ Returns the location of the background image. """
        return self._bgImgLoc

    def getRoundWind(self):
        """ Returns the current round wind, as a Tile. """
        textWind = self._curRound[0]
        if textWind == 'East':
            return Tile(52)
        else:
            return Tile(53)

    def getTilesRemaining(self):
        """ Returns the amount of tiles remaining in the wall. """
        return self._curWall.getTilesRemaining()

    def getGameYaku(self, playerID, typeDraw):
        """ Returns the relevant special game yaku.

        getGameYaku(int, string) -> list of Yaku

        playerID is the ID of which player to check.
        typeDraw is whether they won by tsumo or not.

        """
        curPlayer = self._players[playerID]
        temp = []
        if (self._lastDrawWasDead and playerID == self._playerTurn and
            typeDraw == 'tsumo'):
            temp.append(self._yakuRinshan)
        if self._curWall.getTilesRemaining() <= 0:
            if typeDraw == 'tsumo':
                temp.append(self._yakuHaitei)
            else:
                temp.append(self._yakuHoutei)
        return temp

    def getDoraList(self, playerID):
        """ Returns the list of dora a player has, given their ID. """
        currentDora = self._curWall.getDoraList()
        doraList = []
        for tile in self._players[playerID].returnTiles():
            if tile in currentDora:
                doraList.append(tile)
        return doraList

    def getUraList(self, playerID):
        """ Returns the list of ura dora a player has, given their ID. """
        currentDora = self._curWall.getUraList()
        doraList = []
        for tile in self._players[playerID].returnTiles():
            if tile in currentDora:
                doraList.append(tile)
        return doraList

    def getAllDiscards(self):
        """ Returns a list of all tiles in the discard piles for all players."""
        temp = []
        for player in self._players:
            temp += player.getDiscardPile()
        return temp

    def getAllMelds(self):
        """ Returns a list of the tiles in all melds that have been declared."""
        temp = []
        for player in self._players:
            for tileColl in player.getImmutable():
                temp += tileColl.getTileList()
        return temp

    def getNonRoundWinds(self):
        """ Returns a list of all wind tiles that aren't the round wind. """
        windList = [Tile(51), Tile(52), Tile(53), Tile(54)]
        windList.remove(self.getRoundWind())
        return windList
        
