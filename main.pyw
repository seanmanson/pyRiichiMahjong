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

""" main.py:
Main launcher for the mahjong game. This file should be run in the
root game directory, with all other scripts and modules placed in
./mahjong_scripts and all misc. files placed in ./resources.

"""

#Import major libraries
import sys
try: #Try to import pygame, if it exists.
    import pygame
    import pygame.font
    import pygame.mixer
except ImportError:
    print 'This game requires both the pygame module, pygame.font, and\
 pygame.mixer, but one or all of these are either not installed or there are\
 no known paths to find them.'
    sys.exit(1)
try: #Try to import PIL, if it exists.
    import PIL
except ImportError:
    print 'This game requires the Python Imaging Library (PIL), but it is\
 either not installed or there is no known path to find it.'
    sys.exit(1)

#Import all of the game scripts
from mahjong_scripts import * 

#Main function
def main():
    """ Starts up the game by creating an instance of it and running it.

    main() -> None

    """
    game = RiichiMahjongApp()
    game.run()

if __name__ == '__main__':
    main()
