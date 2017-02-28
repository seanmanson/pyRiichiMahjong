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

""" selfio.py:
A helper file used for loading information from other text settings files.

"""

#Import major libraries
import os

class IOHelper(object):
    """ Used for quick operations with info files, for tiles and yaku etc.
    Allows for the loading of data given ID's; effectively a collection of
    data functions.

    """

    def __init__(self, filename, delimiter, comment):
        """ Create an IOHelper object
        Constructor: IOHelper(sting, string, string)
        
        filename refers to the location of the file
        delimiter is the character separating line info
        comment is the character signifying a comment line
        
        """
        self._filename = filename
        self._delimiter = delimiter
        self._comment = comment

    def __str__(self):
        return "IOHelper(" + self._filename + ")"

    def __repr__(self):
        return "IOHelper file at " + self._filename

    def parseLine(self, line):
        """ Strips and splits a single line in a string, returning data as a
        list. The line is given.
    
        parse_line(string, char) -> list

        String must be separated by the character in the second argument.
        
        """
        return (line.strip()).split(self._delimiter)

    def concatInt(self, intone, inttwo):
        """ Concatenates two integers.
    
        concatInt(self, intone, inttwo) -> int
        
        """
        return int(str(intone) + str(inttwo))

    def getRowByOneID(self, curid):
        """ Given data with one id part, return a row.
        File must exist or an error is given.
        Info within a line must be delimited by commas.
        Comment lines have a # at the start

        getRowByOneID(str) -> list
        
        """
        parsed = None
        f = open(self._filename, 'rU')
        for line in f:
            if line[0]!= self._comment:
                parsed = self.parseLine(line)
                if parsed[0] == str(curid):
                    f.close()
                    return parsed
        f.close()
        return False

    def getRowByTwoID(self, idone, idtwo):
        """ Given data with two id parts, get a row.
        File must exist or an error is given.
        Info within a line must be delimited by commas.
        Comment lines have a # at the start

        getRowByTwoID(int, int) -> list
        
        """
        parsed = None
        f = open(self._filename, 'rU')
        for line in f:
            if line[0]!= self._comment:
                parsed = self.parseLine(line)
                if (parsed[0], parsed[1]) == (str(idone), str(idtwo)):
                    f.close()
                    return parsed
        f.close()
        return False

    def getAllRows(self):
        """ Returns a list of all rows of data in the file.
        File must exist or an error is given.
        Info within a line must be delimited by commas.
        Comment lines have a # at the start

        getAllRows -> list of tuples
        
        """
        f = open(self._filename, 'rU')
        temp = []
        for line in f:
            if line[0]!= self._comment:
                parsed = self.parseLine(line)
                temp.append(tuple(parsed))
        f.close()
        return temp
        
