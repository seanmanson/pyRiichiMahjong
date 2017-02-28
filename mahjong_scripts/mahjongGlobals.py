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

""" mahjongGlobals.py:
Contains all global constants and file locations for use in other module files.
Also determines platform-independant filenames in advance.

"""

#Import major libraries
import os

GAMENAME = "pyRiichiMahjong -- By Sean Manson, for CSSE1001"
FRAMERATE = 25 #Limits the framerate of the game to the given value
SCREENSIZE = [1024, 768]
WHITE = (255,255,255)
OFFWHITE = (240,240,240)
BLACK = (0,0,0)
REDDISH = (155,55,55)
HELPWEBSITE = "http://www.japanesemahjong.com/"
CURRENTFONT = os.path.join('resources', 'corbel.ttf')
HUDFONT = os.path.join('resources', 'jupiterc.ttf')
PROGRAMICON = os.path.join('resources', 'images', 'icon.png')
PAUSEIMAGE = os.path.join('resources', 'images', 'paused.png')
MAINMENUBACKIMG = os.path.join('resources', 'images', 'mainbg.jpg')
MAINBACKBLUEIMG = os.path.join('resources', 'images', 'gamescreenblue.png')
MAINBACKREDIMG = os.path.join('resources', 'images', 'gamescreenred.png')
MAINBACKGREENIMG = os.path.join('resources', 'images', 'gamescreengreen.png')
HUDSEPIMG = os.path.join('resources', 'images', 'hudsep.png')
HUDMINISEPIMG = os.path.join('resources', 'images', 'hudminisep.png')
HUDMINISEPVERTIMG = os.path.join('resources', 'images', 'hudminisep_v.png')
HUDGAMEINFOIMG = os.path.join('resources', 'images', 'hudgameinfo.png')
HUDHANDBACKIMG = os.path.join('resources', 'images', 'hudhandback.png')
HUDRIGHTIMG = os.path.join('resources', 'images', 'hudright.png')
HUDRIGHTLIGHTIMG = os.path.join('resources', 'images', 'hudrightlight.png')
HUDRIGHTSEPIMG = os.path.join('resources', 'images', 'hudrightsep.png')
BUTTONIMG = os.path.join('resources', 'images', 'butt.png')
BUTTONHOVERIMG = os.path.join('resources', 'images', 'butt2.png')
BUTTONDOWNIMG = os.path.join('resources', 'images', 'butt3.png')
BUTTONREDIMG = os.path.join('resources', 'images', 'butt_r.png')
BUTTONREDHOVERIMG = os.path.join('resources', 'images', 'butt2_r.png')
BUTTONREDDOWNIMG = os.path.join('resources', 'images', 'butt3_r.png')
TILEIMGLOC = os.path.join('resources', 'tilesprites')
TILEBACKIMG = 'back.png'
TILEBACKDEADIMG = 'backdead.png'
RIICHIIMG = os.path.join('resources', 'sticksprites', 'riichi.png')
RIICHITINYIMG = os.path.join('resources', 'sticksprites', 'riichitiny.png')
BONUSTINYIMG = os.path.join('resources', 'sticksprites', 'bonustiny.png')
DICEIMGLOC = os.path.join('resources', 'dicesprites')
MAINMENUMUSIC = os.path.join('resources', 'music', 'mainmenu.ogg')
GAMEMUSIC = os.path.join('resources', 'music', 'soothinggame.ogg')
BTNHOVERSOUND = os.path.join('resources', 'sounds', 'tileclick.wav')
BTNCLICKSOUND = os.path.join('resources', 'sounds', 'tiledis.wav')
SCORESOUND = os.path.join('resources', 'sounds', 'score.wav')
DICEROLLSOUND = os.path.join('resources', 'sounds', 'diceroll.wav')
PONSOUND = os.path.join('resources', 'sounds', 'pon.wav')
CHISOUND = os.path.join('resources', 'sounds', 'chi.wav')
KANSOUND = os.path.join('resources', 'sounds', 'kan.wav')
RIICHISOUND = os.path.join('resources', 'sounds', 'riichi.wav')
TSUMOSOUND = os.path.join('resources', 'sounds', 'tsumo.wav')
RONSOUND = os.path.join('resources', 'sounds', 'ron.wav')
GAMESETTINGSLOC = os.path.join('resources', 'gameplaysettings.txt')
SAVEGAMELOC = os.path.join('resources', 'savefolder', 'currentsave.txt')
SAVEP1LOC = os.path.join('resources', 'savefolder', 'currentsavep1.txt')
SAVEP2LOC = os.path.join('resources', 'savefolder', 'currentsavep2.txt')
SAVEP3LOC = os.path.join('resources', 'savefolder', 'currentsavep3.txt')
SAVEP4LOC = os.path.join('resources', 'savefolder', 'currentsavep4.txt')
SAVEWALLLOC = os.path.join('resources', 'savefolder', 'currentsavewall.txt')
CREDITSPAGE = os.path.join('resources', 'credits.txt')
AILIST = ['NoneAI', 'GeoffAI', 'HighHandAI', 'AttackAI', 'DefendAI']
TILEWIDTH = 35
TILEHEIGHT = 45
HANDWIDTH = 650
PLAYERTILEWIDTH = 40
PLAYERTILEHEIGHT = 52
PLAYERHANDWIDTH = 680
DELIMITER = ";"
COMMENTIND = "#"
