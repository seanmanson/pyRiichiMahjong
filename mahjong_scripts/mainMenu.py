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

""" mainMenu.py:
Contains the MainMenu class, which is the MenuScreen which the user initially
lands on when starting the game.

"""
#Import major libraries
import pygame
import webbrowser
import os.path
from pygame.locals import *

#Import other mahjong modules
import mahjongGlobals
from menuItems import *

class MainMenu(MenuScreen):
    """ The MainMenu object, a subclass of MenuScreen. Is made up of a set of
    buttons on a background, as defined in MenuScreen. These buttons do things
    when clicked.

    """
    def __init__(self, master):
        """ Create a new MainMenu.
        Constructor: MainMenu(RiichiMahjongApp)

        master is the main app window which this screen should be placed on.

        """
        bgImg = pygame.image.load(mahjongGlobals.MAINMENUBACKIMG)
        MenuScreen.__init__(self, master, bgImg)
        self._gameVolume = 1.0
        self.addButton(ButtonText(master,40,250,"Start New Game",(255,255,255),
            (255,0,0),(0,0,255),mahjongGlobals.CURRENTFONT,16,5,
            self.buttStartGame))
        self.addButton(ButtonText(master,40,280,"Load Previous Game",
            (255,255,255),(255,0,0),(0,0,255),mahjongGlobals.CURRENTFONT,16,5,
            self.buttLoadGame))
        self.addButton(ButtonText(master,40,350,"Sound Settings",(255,255,255),
            (255,0,0),(0,0,255),mahjongGlobals.CURRENTFONT,16,5,
            self.buttSettings))
        self.addButton(ButtonText(master,40,380,"Help",(255,255,255),
            (255,0,0),(0,0,255),mahjongGlobals.CURRENTFONT,16,5,self.buttHelp))
        self.addButton(ButtonText(master,40,480,"Credits",(255,255,255),
            (255,0,0),(0,0,255),mahjongGlobals.CURRENTFONT,16,5,
            self.buttCredits))
        self.addButton(ButtonText(master,40,510,"Quit",(255,255,255),
            (255,0,0),(0,0,255),mahjongGlobals.CURRENTFONT,16,5,self.buttQuit))

    def buttStartGame(self):
        """ Popup the start game window. """
        self.popupDialog("WindowStartGame")

    def buttLoadGame(self):
        """ If a save file exists, load the previous game, else popup an error.

        """
        if os.path.isfile(mahjongGlobals.SAVEGAMELOC):
            self.changeScreen('GameScreen', [True])
        else:
            self.popupDialog("WindowNoSaveError")

    def buttSettings(self):
        """ Popup the volume settings window. """
        (buttVol, voiceVol, musicVol) = self._master.getVolumes()
            #Prepare to pass the window the current volumes of each thing.
        buttVol = int(buttVol*100)
        voiceVol = int(voiceVol*100)
        musicVol = int(musicVol*100)
        self.popupDialog("WindowVolume", [buttVol, voiceVol, musicVol])

    def buttHelp(self):
        """ Open the help page on the user's default browser. """
        webbrowser.open(mahjongGlobals.HELPWEBSITE)

    def buttCredits(self):
        """ Popup the credits window. """
        self.popupDialog("WindowCredits")

    def buttQuit(self):
        """ Quit the program. """
        pygame.quit()
        sys.exit()
