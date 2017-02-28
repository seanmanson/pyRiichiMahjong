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

""" yaku.py:
Contains information on yaku and how they get their information, decriptions,
han value etc.

"""

#Import mahjong libraries
from selfio import *

#Set default globals
DELIMITER = ";"
COMMENTIND = "#"

class Yaku(object):
    """ A general class used for yaku.
    Similar to tuples, but with more functions.
    Stores info related to yaku for scoring, such as their han value,
    descriptions and otehr useful info.

    """
    
    def __init__(self, yakuID, yakuFile):
        """ Creates a new yaku from the given yakuFile.
        Constructor: Yaku(string, string)
        
        yakuID is an identifier in the yaku file.
        yakuFile is the location of said file.
        
        """
        self._yakuID = yakuID
        loadInfo = IOHelper(yakuFile, DELIMITER, COMMENTIND)
        rowInfo = loadInfo.getRowByOneID(yakuID)
        if rowInfo:
            self._name = rowInfo[1]
            self._scoreClosed = int(rowInfo[2])
            self._scoreOpen = int(rowInfo[3])
            self._desc = rowInfo[5]

            self._invalid = rowInfo[4].split(',') #these are separated by commas
        else:
            self._name = "Unknown"
            self._scoreOpen = None
            self._scoreClosed = None
            self._soundFile = None
            self._invalid = None
            self._desc = None
            
    def __str__(self):
        return self._name

    def __repr__(self):
        return "Yaku(" + self.__str__() + ")"

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self._yakuID == other._yakuID)

    def __ne__(self, other):
        return not self.__eq__(other)

    def getName(self):
        return self._name

    def getScoreOpen(self):
        return self._scoreOpen

    def getScoreClosed(self):
        return self._scoreClosed

    def getSound(self):
        return self._soundFile

    def getInvalid(self):
        return self._invalid

    def getDesc(self):
        return self._desc
