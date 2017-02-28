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

""" riichiMahjongApp.py:
Main program object definition. Contains the main screen and all pygame function
running methods, which is what actually displays itself in a window. Also used
for music and other central event-based functionality.

"""

#Import major libraries
import time
import sys
import pygame
from pygame.locals import *
from Tkinter import *

#Import other mahjong modules
import mahjongGlobals
from menuItems import *
from mainMenu import *
from gameScreen import *

class RiichiMahjongApp(object):
    """ The main app object, as created by main.py. Used for pretty much
    anything and everything for this game, such as music and drawing to the
    screen.

    """
    def __init__(self):
        """ Create a new RiichiMahjongApp.
        Constructor: RiichiMahjongApp()

        """
        pygame.mixer.pre_init(22050, -16, 2, 512) #Get the sound module ready
        pygame.init()
        self.screen = pygame.display.set_mode(mahjongGlobals.SCREENSIZE,
            RESIZABLE) #Setup the screen
        self.clock = pygame.time.Clock()
        self._setupValues()
        self._redraw()

    def _setupValues(self):
        """ Load all sounds, sound channels and default values, getting the game
        ready for its initial run.

        """
        pygame.display.set_caption(mahjongGlobals.GAMENAME)
        pygame.display.set_icon(pygame.image.load(mahjongGlobals.PROGRAMICON))
        self._buttonChannel = pygame.mixer.Channel(0)
        self._voiceChannel = pygame.mixer.Channel(1)
        self._musicVol = 0.2
        self._hoverSound = pygame.mixer.Sound(mahjongGlobals.BTNHOVERSOUND)
        self._clickSound = pygame.mixer.Sound(mahjongGlobals.BTNCLICKSOUND)
        self._drawSound = pygame.mixer.Sound(mahjongGlobals.BTNHOVERSOUND)
        self._discardSound = pygame.mixer.Sound(mahjongGlobals.BTNCLICKSOUND)
        self._scoreSound = pygame.mixer.Sound(mahjongGlobals.SCORESOUND)
        self._diceSound = pygame.mixer.Sound(mahjongGlobals.DICEROLLSOUND)
        self._ponSound = pygame.mixer.Sound(mahjongGlobals.PONSOUND)
        self._chiSound = pygame.mixer.Sound(mahjongGlobals.CHISOUND)
        self._kanSound = pygame.mixer.Sound(mahjongGlobals.KANSOUND)
        self._riichiSound = pygame.mixer.Sound(mahjongGlobals.RIICHISOUND)
        self._tsumoSound = pygame.mixer.Sound(mahjongGlobals.TSUMOSOUND)
        self._ronSound = pygame.mixer.Sound(mahjongGlobals.RONSOUND)
        self.changeScreen('MainMenu', None) #First screen is the main menu
        self._paused = False
        self._pauseImg = pygame.image.load(mahjongGlobals.PAUSEIMAGE)

    def _widthBigger(self, size):
        """ Returns whether the width or height is the bigger value compared to
        the required 4:3 ratio for the screen. Returns true if width is bigger.

        _widthBigger(2-tuple) -> None

        size is the (width, height) dimensions of the screen.

        """
        if size[0] > float(size[1])*float(4)/3:
            return True
        else:
            return False

    def _convertPos(self, pos):
        """ Converts the given (x, y) position to a scaled value according to
        the true size of the screen, as a 4:3 value. Returns this new value.

        """
        curSize = self.screen.get_size()
        if self._widthBigger(curSize):
            height = curSize[1]
            width = int(height * float(4)/3)
            xPos = (curSize[0] - width)/2
            yPos = 0
        else:
            width = curSize[0]
            height = int(width * float(3)/4)
            xPos = 0
            yPos = (curSize[1] - height)/2
        newX = int((pos[0] - xPos) * 1024/float(width))
        newY = int((pos[1] - yPos) * 768/float(height))
        return (newX, newY)

    def _redraw(self):
        """ Redraws the screen, taking the updated surface from self.curScreen.
        If the size of the window is not 4:3, adds black bars as neccessary and
        resizes the game display accordingly.

        """
        curSize = self.screen.get_size()
        if self._widthBigger(curSize):
            height = curSize[1]
            width = int(height * float(4)/3)
            xPos = (curSize[0] - width)/2
            yPos = 0
        else:
            width = curSize[0]
            height = int(width * float(3)/4)
            xPos = 0
            yPos = (curSize[1] - height)/2
        gameSurface = self.curScreen.returnSurface()
        if (self._paused):
            gameSurface.blit(self._pauseImg, (0,0))
        drawSurface = pygame.transform.scale(gameSurface, (width, height))
        self.screen.blit(drawSurface, (xPos, yPos))

    def getVolumes(self):
        """ Returns the current game volumes as a 3-tuple. """
        return (self._buttonChannel.get_volume(),
                self._voiceChannel.get_volume(),
                self._musicVol)

    def setButtonVolume(self, newVolume):
        """ Sets the new volume of button clicking. """
        self._buttonChannel.set_volume(newVolume)

    def setVoiceVolume(self, newVolume):
        """ Sets the new volume of voices. """
        self._voiceChannel.set_volume(newVolume)

    def setMusicVolume(self, newVolume):
        """ Sets the new volume of the music, rewinding it to the start. """
        self._musicVol = newVolume
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(self._musicVol)
        pygame.mixer.music.play(-1)

    def playButtonSound(self, sound):
        """ Plays the given sound string on the button channel. """
        exec('curSound = self._' + sound)
        self._buttonChannel.play(curSound)

    def playVoiceSound(self, sound):
        """ Plays the given sound string on the voice channel. """
        exec('curSound = self._' + sound)
        self._voiceChannel.play(curSound)

    def playMusic(self, screenTo):
        """ Plays the associated music for each MenuScreen.
        Stops and starts the music with the current music volume.

        """
        pygame.mixer.music.stop()
        if screenTo == 'MainMenu':
            pygame.mixer.music.load(mahjongGlobals.MAINMENUMUSIC)
            pygame.mixer.music.play(-1)
        elif screenTo == 'GameScreen':
            pygame.mixer.music.load(mahjongGlobals.GAMEMUSIC)
            pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self._musicVol)

    def changeScreen(self, screenTo, values):
        """ Changes the current screen displayed to the given new screen.
        Usually, each screen will have an associated music that plays when
        switching to it with this command.

        changeScreen(string, object) -> None

        screenTo is a string of which MenuScreen self.curScreen should be
        changed to.
        values is a set of values which can optionally be passed to this
        MenuScreen on creation.

        """
        self.playMusic(screenTo)
        if values:
            funcToRun = ("self.curScreen = " + str(screenTo) +
             "(self, " + str(values) + ")")
        else:
            funcToRun = "self.curScreen = " + str(screenTo) + "(self)"
        exec(funcToRun)

    def run(self):
        """ The standard pygame running loop. """
        while True: #Main game loop
            for event in pygame.event.get(): #Update events
                if event.type == MOUSEMOTION:
                    self.onMouseAction(event)
                if event.type == MOUSEBUTTONDOWN:
                    self.onMouseAction(event)
                if event.type == MOUSEBUTTONUP:
                    self.onMouseAction(event)
                if event.type == KEYDOWN:
                    self.onKeyDown(event)
                if event.type == KEYUP:
                    self.onKeyUp(event)
                if event.type == VIDEORESIZE:
                    self.onResize(event)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.curScreen.update() #Update the current screen's logic
            self._redraw() #Redraw all elements
            pygame.display.update() #Update pygame display
            self.clock.tick(mahjongGlobals.FRAMERATE)

    def pause(self):
        """ Pause the game, and display the associated pause screen. """
        self._paused = True
        self._redraw() #Force a refresh of the screen
        pygame.display.update()

    def resume(self):
        """ Resume the game, and return the game to normal. """
        self._paused = False
        self._redraw() #Force a refresh of the screen
        pygame.display.update()

    def onMouseAction(self, event):
        """ On mouse actions, pass this action to the current game screen and
        change the cursor if appropriate.

        """
        newPos = self._convertPos(event.pos)
        self.curScreen.onMouseEvent((newPos, event.type))
        if self.curScreen.isHovering():
            #If we're hovering over some menu element
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def onKeyUp(self, event):
        """ Pass keyUp events to the current game screen. """
        keyName = pygame.key.name(event.key)
        self.curScreen.onKeyUp(keyName)

    def onKeyDown(self, event):
        """ Key down events are ignored for this particular game. """
        pass

    def onResize(self, event):
        """ When resized, set the size of the window to the new size. """
        self.screen = pygame.display.set_mode(event.size,RESIZABLE)

    def onQuit(self):
        """ When quitting, be sure to exit all game elements cleanly. """
        pygame.quit()
        sys.exit()
