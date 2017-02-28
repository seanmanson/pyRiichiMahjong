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

""" menuItems.py:
Contains classes of buttons and Screens that can be interacted with.

"""
#Import major libraries
import pygame
from pygame.locals import *
from Tkinter import *

#Import other mahjong modules
import mahjongGlobals
from popupDialogs import *

class Button(object):
    """ Button object. Has an x and y position, a screen which it is attached
    to, and a function which occurs when pressed. Takes in mouse events and
    uses them to see whether the button is being hovered over or not, or being
    clicked or not.

    This class should NOT be used by itself; only subclasses should be used,
    as this class is made to be subclassed.

    """
    def __init__(self, master, xPos, yPos, func):
        """ Create a new Button attached to master at xPos, yPos.
        Constructor: Button(RiichiMahjongApp, int, int, function)

        master is the main app window which this button should be placed on.
        xPos, yPos are the (x, y) position of the button on the screen.
        func is the function which should be run when the button is pressed.
        
        """
        self._master = master
        self._x = xPos
        self._y = yPos
        self._func = func
        self._isMouseHover = False
        self._isMouseDown = False
        self._enabled = True
        self._size = (1, 1) #This will be superceeded by subclasses

    def enable(self):
        """ Enables this button for use. """
        self._enabled = True

    def disable(self):
        """ Disables this button, deselecting it if it were so. """
        self._enabled = False
        self._isMouseHover = False
        self._isMouseDown = False
            #In the case that the button is deleted while hovering over it

    def isEnabled(self):
        """ Returns whether this button is enabled. """
        return self._enabled

    def onMouseEvent(self, eventInfo):
        """ Break down the current mouse event and undergo the appropriate
        actions for each event, related to this button.

        onMouseEvent(MouseEvent) -> None

        eventInfo is the relevant info for this mouse event.

        """
        if self._enabled == False:
            return False
        if eventInfo[1] == MOUSEMOTION:
            self.onMouseMove(eventInfo[0])
        if eventInfo[1] == MOUSEBUTTONDOWN:
            self.onMouseDown(eventInfo[0])
        if eventInfo[1] == MOUSEBUTTONUP:
            self.onMouseUp(eventInfo[0])

    def onMouseMove(self, eventPos):
        """ Test to see if the mouse is currently over the button and, if so,
        select it and play a hover sound.

        onMouseMove(tuple of integers) -> None

        eventPos is the (x, y) location of the mouse.

        """
        mousex = eventPos[0]
        mousey = eventPos[1]
        if ((self._x <= mousex < self._x + self._size[0])
                and (self._y <= mousey < self._y + self._size[1])):
            if not self._isMouseHover:
                self._master.playButtonSound('hoverSound')
            self._isMouseHover = True
        else:
            self._isMouseHover = False

    def onMouseDown(self, event):
        """ Test to see if the mouse is currently pressed on the button and, if
        so, push the button down.

        onMouseDown(tuple of integers) -> None

        event is the (x, y) location of the mouse.

        """
        if self._isMouseHover:
            self._isMouseDown = True

    def onMouseUp(self, event):
        """ Test to see if the mouse has currently let go of the button and, if
        so, well, press it.

        onMouseUp(tuple of integers) -> None

        event is the (x, y) location of the mouse.

        """
        self._isMouseDown = False
        if self._isMouseHover:
            self._master.playButtonSound('clickSound')
            self.press()

    def press(self):
        """ If the button is pressed, run the function. """
        self._func()

    def getPos(self):
        """ Returns the (x, y) position of the button, as a tuple. """
        return (self._x, self._y)

    def returnSurface(self, doSelect):
        """ Draws and returns a Surface for this button.

        returnSurface(Boolean) -> Surface

        doSelect is whether or not this button is selected with the keyboard.

        """
        tempSurface = pygame.Surface((10,10), pygame.SRCALPHA, 32)
        return tempSurface

class ButtonText(Button):
    """ ButtonText object, a subclass of Button. As well as having the
    properties of a button, it contains text which changes colour when hovered
    and pressed.

    """
    def __init__(self, master, xPos, yPos, text, textcolour, textcolour_hvr,
                 textcolour_down, font, fontsize, padding, func):
        """ Create a new ButtonText.
        Constructor: ButtonText(RiichiMahjongApp, int, int, string, 3-tuple,
                                3-tuple, 3-tuple, string, int, int, function)

        master is the main app window which this button should be placed on.
        xPos, yPos are the (x, y) position of the button on the screen.
        text is the string of text which the button should display.
        textcolour is a 3-tuple of RGB values for the base colour of text.
        textcolour_hvr is a RGB 3-tuple for the hover colour of text.
        textcolour_down is a RGB 3-tuple for the pressed colour of text.
        font is the file location of the font for this button.
        fontsize is the integer size of this text on screen.
        padding is the empty space around the text that should be added.
        func is the function which should be run when the button is pressed.
        
        """
        Button.__init__(self, master, xPos, yPos, func)
        self._text = text
        self._textcolour = textcolour
        self._font = pygame.font.Font(font, fontsize)
        self._fontDim = self._font.size(text)
        self._size = (self._fontDim[0]+2*padding, self._fontDim[1]+2*padding)
        self._padding = padding
        self._textcolour_hvr = textcolour_hvr
        self._textcolour_down = textcolour_down

    def changeText(self, textTo):
        """ Changes the text on this button to the given string. """
        self._text = textTo
        self._fontDim = self._font.size(textTo)
        self._size = (self._fontDim[0]+2*self._padding,
            self._fontDim[1]+2*self._padding)

    def getText(self):
        """ Returns the text on this button. """
        return self._text

    def returnSurface(self, doSelect):
        """ Draws and returns a Surface for this button, taking into account
        hover and pressed states.

        returnSurface(Boolean) -> Surface

        doSelect is whether or not this button is selected with the keyboard.

        """
        tempSurface = pygame.Surface(self._size, pygame.SRCALPHA, 32)
        if self._isMouseDown:
            curColour = self._textcolour_down
        elif self._isMouseHover or doSelect:
            curColour = self._textcolour_hvr
        else:
            curColour = self._textcolour
        tempTextDraw = self._font.render(self._text, True, curColour)
        tempSurface.blit(tempTextDraw, (self._padding, self._padding))
        return tempSurface


class ButtonImgText(Button):
    """ ButtonImgText object, a subclass of Button. Similar to ButtonText,
    except that the button now has a background image behind the text, which
    changes when the button is pressed.

    """
    def __init__(self, master, xPos, yPos, text, textcolour, textcolourdis,
                 font, fontsize, size, func, img, imgDown, imgHover):
        """ Create a new ButtonImgText.
        Constructor: ButtonImgText(RiichiMahjongApp, int, int, string, 3-tuple,
                                   3-tuple, string, int, 2-tuple, function,
                                   string, string, string)

        master is the main app window which this button should be placed on.
        xPos, yPos are the (x, y) position of the button on the screen.
        text is the string of text which the button should display.
        textcolour is a 3-tuple of RGB values for the base colour of text.
        textcolourdis is a RGB 3-tuple for the disabled colour of text.
        font is the file location of the font for this button.
        fontsize is the integer size of this text on screen.
        size is the (width, height) dimensions of the button.
        func is the function which should be run when the button is pressed.
        img is the file location of tbe base image.
        imgDown is the file location of the pressed image.
        imgHover is the file location of the hovering image.
        
        """
        Button.__init__(self, master, xPos, yPos, func)
        self._text = text
        self._textcolour = textcolour
        self._font = pygame.font.Font(font, fontsize)
        self._fontDim = self._font.size(text)
        self._size = size
        self._textcolourdis = textcolourdis
        self._leftpadding = (size[0] - self._fontDim[0])/2
        self._toppadding = (size[1] - self._fontDim[1])/2
        self._img = pygame.image.load(img)
        self._img = pygame.transform.scale(self._img, self._size)
        self._imgDown = pygame.image.load(imgDown)
        self._imgDown = pygame.transform.scale(self._imgDown, self._size)
        self._imgHover = pygame.image.load(imgHover)
        self._imgHover = pygame.transform.scale(self._imgHover, self._size)

    def changeText(self, textTo):
        """ Changes the text on this button to the given string. """
        self._text = textTo
        self._fontDim = self._font.size(textTo)
        self._leftpadding = (self._size[0] - self._fontDim[0])/2
        self._toppadding = (self._size[1] - self._fontDim[1])/2

    def getText(self):
        """ Returns the text on this button. """
        return self._text

    def returnSurface(self, doSelect):
        """ Draws and returns a Surface for this button, taking into account
        hover and pressed states.

        returnSurface(Boolean) -> Surface

        doSelect is whether or not this button is selected with the keyboard.

        """
        tempSurface = pygame.Surface(self._size)
        if not self._enabled:
            curImage = self._img
        elif self._isMouseDown:
            curImage = self._imgDown
        elif self._isMouseHover or doSelect:
            curImage = self._imgHover
        else:
            curImage = self._img
        tempSurface.blit(curImage, (0,0))
        if self._enabled:
            curColour = self._textcolour
        else:
            curColour = self._textcolourdis
        tempTextDraw = self._font.render(self._text, True, curColour)
        tempSurface.blit(tempTextDraw, (self._leftpadding, self._toppadding))
        return tempSurface

class ButtonInvis(Button):
    """ ButtonInvis object, a subclass of Button. An invisible button, used when
    testing if some misc position on the screen is clicked. Does not highlight.

    """
    def __init__(self, master, xPos, yPos, size, func):
        """ Create a new Button attached to master at xPos, yPos.
        Constructor: Button(RiichiMahjongApp, int, int, function)

        master is the main app window which this button should be placed on.
        xPos, yPos are the (x, y) position of the button on the screen.
        size is the (width, height) dimensions of the button.
        func is the function which should be run when the button is pressed.
        
        """
        Button.__init__(self, master, xPos, yPos, func)
        self._size = size

    def onMouseMove(self, eventPos):
        """ Test to see if the mouse is currently over the button and, if so,
        select it and play a hover sound. This is defined separately to remove
        the clicking sound for this button.

        onMouseMove(tuple of integers) -> None

        eventPos is the (x, y) location of the mouse.

        """
        mousex = eventPos[0]
        mousey = eventPos[1]
        if ((self._x <= mousex < self._x + self._size[0])
                and (self._y <= mousey < self._y + self._size[1])):
            self._isMouseHover = True
        else:
            self._isMouseHover = False

    def onMouseUp(self, event):
        """ Test to see if the mouse has currently let go of the button and, if
        so, well, press it. This is defined separately to remove the clicking
        sound for this button.

        onMouseUp(tuple of integers) -> None

        event is the (x, y) location of the mouse.

        """
        self._isMouseDown = False
        if self._isMouseHover:
            self.press()

class ButtonTile(Button):
    """ ButtonTile object, a subclass of Button. Used for the tile buttons on
    the main game screen. These have a highlight effect placed over them, rather
    than using separate images.

    """
    def __init__(self, master, xPos, yPos, size, func, tileIndex, img):
        """ Create a new ButtonTile.
        Constructor: ButtonTile(RiichiMahjongApp, int, int, 2-tuple, function,
                                int, Surface)

        master is the main app window which this button should be placed on.
        xPos, yPos are the (x, y) position of the button on the screen.
        size is the (width, height) dimensions of the button.
        func is the function which should be run when the button is pressed.
        tileIndex is the integer index of the tile in the hand.
        img is the surface of the tile's picture.

        """
        Button.__init__(self, master, xPos, yPos, func)
        self._size = size
        self._tileIndex = tileIndex
        self._img = pygame.transform.scale(img, self._size)
        self._highlight = False
        self._highlightType = 'none'

    def highlight(self, highlightType):
        """ Highlights this tile with type highlightType. """
        self._highlight = True
        self._highlightType = highlightType

    def unHighlight(self):
        """ Unhighlights this tile. """
        self._highlight = False
        self._highlightType = 'none'

    def isHighlight(self):
        """ Returns whether this tile is highlighted. """
        return self._highlight

    def getHighlightType(self):
        """ Returns the current highlight type of this tile. """
        return self._highlightType

    def press(self):
        """ Presses this tile, passing the function the current tileIndex. """
        self._func(self._tileIndex)

    def returnSurface(self, doSelect):
        """ Draws and returns a Surface for this button, taking into account
        hover and pressed states.

        returnSurface(Boolean) -> Surface

        doSelect is whether or not this button is selected with the keyboard.

        """
        tempSurface = pygame.Surface(self._size, pygame.SRCALPHA, 32)
        tempSurface.blit(self._img, (0,0))
        tempHighlight = pygame.Surface(self._size)
        if self._isMouseDown:
            tempHighlight.fill(mahjongGlobals.BLACK)
            tempHighlight.set_alpha(100)
        elif self._isMouseHover:
            tempHighlight.fill(mahjongGlobals.WHITE)
            tempHighlight.set_alpha(100)
        elif doSelect or self._highlight:
            tempHighlight.fill(mahjongGlobals.WHITE)
            tempHighlight.set_alpha(150)
        else:
            tempHighlight.fill(mahjongGlobals.WHITE)
            tempHighlight.set_alpha(0)
        tempSurface.blit(tempHighlight, (0,0))
        return tempSurface

class AnimatedText(object):
    """ AnimatedText object. Used for displaying text in the middle of the
    screen for a limited period of time. This text fades in and out, scrolling
    down the screen.

    """
    def __init__(self, text, textcolour, font, fontsize, step, lifetime):
        """ Create a new AnimatedText.
        Constructor: AnimatedText(string, 3-tuple, string, int, int, int)

        text is the string of text which should be displayed.
        textcolour is a 3-tuple of RGB values for the base colour of text.
        font is the file location of the font for this text.
        fontsize is the integer size of this text on screen.
        step is the integer value of how many pixels the text should move per
        frame.
        lifetime is the amount of frames this text should live for.

        """
        self._text = text
        self._textcolour = textcolour
        self._font = pygame.font.Font(font, fontsize)
        self._fontDim = self._font.size(text)
        self._step = step
        self._lifetime = lifetime
        self._curStep = 0 #mover variable
        self._moveY = -self._step*self._lifetime/2
        self._alpha = 0

    def update(self):
        """ Updates the current position and alpha value for this text. Returns
        whether or not the animation has finished.

        update() -> Boolean

        """
        self._curStep+=1
        if self._curStep < self._lifetime/4:
            self._moveY += self._step
            self._alpha = 255*(self._curStep)/(self._lifetime/4)
        elif self._curStep < 3*self._lifetime/4:
            self._alpha = 255
        elif self._curStep < self._lifetime:
            self._moveY += self._step
            self._alpha = 255*(self._lifetime-self._curStep)/(self._lifetime/4)
        else:
            return False
        if self._alpha > 255:
            self._alpha = 255
        return True

    def getCoords(self, xPos, yPos):
        """ Returns the coordinates needed to put the top middle of this text at
        (xPos, yPos).

        """
        realX = xPos - (self._fontDim[0]/2)
        realY = yPos + self._moveY
        return (realX, realY)

    def returnSurface(self):
        """ Returns this text as a transparent surface which can be blit'd. """
        tempSurface = self._font.render(self._text, True, self._textcolour)
        tempSurface.fill((255, 255, 255, self._alpha), None,
            pygame.BLEND_RGBA_MULT)
        return tempSurface

class FadeInOut(object):
    """ FadeInOut object. Animates a rectancle with a given colour over a
    lifetime of frames, fading it in and out again.

    """
    def __init__(self, xPos, yPos, size, colour, maxAlpha, step, lifetime):
        """ Create a new FadeInOut.
        Constructor: FadeInOut(int, int, 2-tuple, 3-tuple, int, int, int)

        xPos, yPos are the (x, y) position of the rectangle on the screen.
        size is the (width, height) dimensions of the rectangle.
        colour is a 3-tuple of RGB values for the colour of the rectangle.
        maxAlpha is the maximum alpha value the rectangle will reach.
        step is unused, and is kept for backward compatibility.
        lifetime is the amount of frames this rectangle should live for.
        
        """
        self._x = xPos
        self._y = yPos
        self._size = size
        self._colour = colour
        self._step = step
        self._lifetime = lifetime
        self._curStep = 0 #mover variable
        self._alpha = 0
        self._maxAlpha = maxAlpha

    def update(self):
        """ Updates the current alpha value for this rectangle. Returns
        whether or not the animation has finished.

        update() -> Boolean

        """
        self._curStep+=1
        if self._curStep < self._lifetime/4:
            self._alpha = self._maxAlpha*(self._curStep)/(self._lifetime/4)
        elif self._curStep < 3*self._lifetime/4:
            self._alpha = self._maxAlpha
        elif self._curStep < self._lifetime:
            self._alpha = (self._maxAlpha*(self._lifetime-
                self._curStep)/(self._lifetime/4))
        else:
            return False
        if self._alpha > self._maxAlpha:
            self._alpha = self._maxAlpha
        return True

    def getPos(self):
        """ Returns the (x, y) position of the rectangle on the screen. """
        return (self._x, self._y)

    def returnSurface(self):
        """ Returns a surface for this rectangle. """
        tempSurface = pygame.Surface(self._size, pygame.SRCALPHA, 32)
        tempSurface.fill((self._colour[0], self._colour[1], self._colour[2],
            self._alpha))
        return tempSurface


class MenuScreen(object):
    """ A MenuScreen is an object with a background image and a collection of
    buttons on it which can be clicked or pressed with the mouse or keyboard.
    It also can open up Tkinter dialogs on command.

    """
    def __init__(self, master, bgImg):
        """ Create a new MenuScreen.
        Constructor: MenuScreen(RiichiMahjongApp, Surface)

        master is the main app window which this screen should be placed on.
        bgImg is a Surface for the image placed in the background.

        """
        self._master = master
        self.backImg = bgImg
        self.back = pygame.transform.scale(self.backImg,
            mahjongGlobals.SCREENSIZE)
        self.buttonList = []
        self.curButtonSel = -1 #No button selected at the start
        self.curDialog = False

    def update(self):
        """ Updates the logic status of the screen. Should be used by subclasses
        that actually have logic which should be updated every frame.

        """
        pass
        
    def addButton(self, Button):
        """ Add a new button Button to this screen. """
        self.buttonList.append(Button)

    def clearButtons(self):
        """ Remove all buttons from this screen. """
        self.buttonList = []

    def popupDialog(self, dialogType="Window", otherInfo=None):
        """ Popup a Tkinter dialog window, as defined in popupDialogs.py. This
        window will interrupt current operation of the screen, and will continue
        to do so until closed. This will also display a 'paused' message on the
        screen.

        popupDialog(string, object) -> None

        dialogType is a string of which Window type should be created, as
        defined in popupDialogs.py.
        otherInfo is misc. information which can be passed to the popup window,
        of any type.

        """
        if not self.curDialog:
            self.curDialog = True
            self._master.pause()
            root = Tk()
            if otherInfo:
                appToRun = "app = " + dialogType + "(root, self, otherInfo)"
            else:
                appToRun = "app = " + dialogType + "(root, self)"
            exec(appToRun)
            root.mainloop()
            self.destroyDialog()

    def destroyDialog(self):
        """ Close the current popup dialog and resume normal operation. """
        pygame.event.clear() #Get rid of all those events they might have made
        self._master.resume()
        self.curDialog = False

    def changeScreen(self, screenTo, values):
        """ Change the current screen displayed to a different one.

        changeScreen(string, object) -> None

        screenTo is a string saying which screen the game should be changed to.
        values is a misc. object containing information that should be passed
        to this screen on creation.

        """
        self._master.changeScreen(screenTo, values)

    def setVolumes(self, newVolumes):
        """ Sets the volumes in master to the 3-tuple of volumes given. """
        self._master.setButtonVolume(newVolumes[0])
        self._master.setVoiceVolume(newVolumes[1])
        self._master.setMusicVolume(newVolumes[2])

    def onMouseEvent(self, eventInfo):
        """ Breaks down the current mouse event and passes it along to all the
        buttons on this screen.

        onMouseEvent(MouseEvent) -> None

        eventInfo is the relevant info for this mouse event.

        """
        if (eventInfo[1] == MOUSEBUTTONDOWN or
            eventInfo[1] == MOUSEBUTTONUP):
            self.curButtonSel = -1
        for button in self.buttonList:
            button.onMouseEvent(eventInfo)

    def isHovering(self):
        """ Returns whether the mouse is currently over any buttons. """
        if not self.curDialog:
            for button in self.buttonList:
                if button._isMouseHover:
                    self.curButtonSel = -1
                    return True
            return False

    def onKeyUp(self, keyName):
        """ Breaks down the key up event and runs the appropriate function.

        onKeyUp(string) -> None

        keyName is a string containing the name of the key pressed.

        """
        if keyName == 'up' or keyName == 'left':
            self.scrollUpButtons()
        elif keyName == 'down' or keyName == 'right' or keyName == 'tab':
            self.scrollDownButtons()
        elif keyName == 'return' or keyName == 'space':
            self.pressCurrentButton()

    def scrollUpButtons(self):
        """ Scrolls up the current list of buttons. """
        self.curButtonSel -= 1
        if self.curButtonSel < -1:
            self.curButtonSel = len(self.buttonList) - 1
        if not (self.buttonList[self.curButtonSel].isEnabled() or
                self.curButtonSel == -1):
            self.scrollUpButtons()
        else:
            self._master.playButtonSound('hoverSound')

    def scrollDownButtons(self):
        """ Scrolls down the current list of buttons. """
        self.curButtonSel += 1
        if self.curButtonSel >= len(self.buttonList):
            self.curButtonSel = -1
        if not (self.buttonList[self.curButtonSel].isEnabled() or
                self.curButtonSel == -1):
            self.scrollDownButtons()
        else:
            self._master.playButtonSound('hoverSound')

    def pressCurrentButton(self):
        """ Press the currently selected button. """
        if not (self.curButtonSel == -1):
            self.buttonList[self.curButtonSel].press()

    def returnSurface(self):
        """ Returns the surface for this particular MenuScreen, by going through
        and drawing the background then bliting all buttons on top of it.

        returnSurface() -> Surface

        """
        tempSurface = pygame.Surface(mahjongGlobals.SCREENSIZE)
        tempSurface.blit(self.back, (0, 0))
        for i, button in enumerate(self.buttonList):
            doSelect = (i == self.curButtonSel)
            curSurface = button.returnSurface(doSelect)
            curPos = button.getPos()
            tempSurface.blit(curSurface, curPos)
        return tempSurface
