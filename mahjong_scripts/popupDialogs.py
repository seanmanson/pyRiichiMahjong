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

""" popupDialogs.py:
Contains all Tkinter-based dialogs that can popup during gameplay.

"""

#Import major libraries
from Tkinter import *
from PIL import Image, ImageTk
import os.path
import tkMessageBox

#Import other mahjong modules
import mahjongGlobals
from mahjong_rulebase import *

#Define some global colours and fonts for Tkinter
CLR_MAINBG = "OldLace"
CLR_FRAMEBG = "Tan"
CLR_BUTTBG = "LemonChiffon"
CLR_BUTTPRESS = "Tan"
CLR_BUTTOTHERHOVER = "Bisque"
CLR_BUTTOTHERDOWN = "Peru"
CLR_ENTRYHL = "DarkGreen"
CLR_LABEL = "DarkGreen"
FNT_TITLEFONT = ("Courier",18,"bold")
FNT_LABELFONT = ("Helvetica",10,"bold")

class Window(object):
    """ Main popup window. Just defines the default values for any window.
    Should really only ever be subclassed, not run directly.

    """
    def __init__(self, curRoot, curScreen):
        """ Create a new Window.
        Constructor: Window(Tk, MenuScreen)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.

        """
        self._root = curRoot
        self._curScreen = curScreen
        self._root.configure(bg=CLR_MAINBG)
        self._root.title("CSSE1001 Assignment 3 - Sean Manson 42846413")

class WindowStartGame(Window):
    """ Start game window. Contains forms for setting up the game data, like
    the AI players or the player name text entry and stuff.

    """
    def __init__(self, curRoot, curScreen):
        """ Create a new WindowStartGame.
        Constructor: WindowStartGame(Tk, MenuScreen)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.

        """
        Window.__init__(self, curRoot, curScreen)
        self._root.title("Options -- Start New Game")
        self._root.resizable(False, False)
        Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_TITLEFONT,
            text="NEW GAME SETTINGS").pack(side=TOP, pady=10)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)
        Label(self._root, bg=CLR_MAINBG,
            text="Choose your game settings below:").pack(side=TOP, anchor=W,
            padx=5)

        self._midframe = WindowStartGame_MiddleFrame(self._root)
        self._midframe.pack(side=TOP,
            fill=BOTH, padx=20, pady=5)

        self._buttonframe = Frame(self._root, bg=CLR_MAINBG)
        self._buttonframe.pack(side=TOP, fill=X, padx=5, pady=5)
        buttPlay = Button(self._buttonframe,text="Play",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._playGame)
        buttCancel = Button(self._buttonframe,text="Cancel",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._cancelWindow)
        buttHelp = Button(self._buttonframe,text="Help",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._helpPopup)
        buttPlay.pack(side=LEFT)
        buttCancel.pack(side=LEFT,padx=8)
        buttHelp.pack(side=RIGHT)

    def _playGame(self):
        """ Using the given starting values, move the game to the GameScreen."""
        curValues = [False] + self._midframe.returnValues()
        if curValues: #If they entered it in correctly
            self._root.destroy()
            self._curScreen.destroyDialog()
            self._curScreen.changeScreen('GameScreen', curValues)

    def _cancelWindow(self):
        """ Cancel and close this window. """
        self._root.destroy()
        self._curScreen.destroyDialog()

    def _helpPopup(self):
        """ Popup another mini help dialog window. """
        #Create child window
        win = Toplevel(bg=CLR_MAINBG)
        win.resizable(False, False)
        #Display message
        title = "Start New Game Help"
        name = "Name -- Your personal player name."
        score = "Starting Score -- The score each player starts with. When your\
 score drops to zero, you lose."
        ai = "AI -- You can choose the type of AI for all other players. 'None'\
 means that the AI will just discard each tile as they draw it."
        gameType = "Game Type -- The length of the game; whether it will take\
 place over just the East round or the East and South rounds."
        bgcolour = "Background Colour -- The background colour the game window\
 will have."
        Label(win, text=title, font=FNT_LABELFONT, bg=CLR_MAINBG, padx=4,
            pady=4).pack(side=TOP, anchor=W)
        Label(win, text=name, bg=CLR_MAINBG, padx=4, pady=4).pack(side=TOP,
            anchor=W)
        Label(win, text=score, bg=CLR_MAINBG, padx=4, pady=4).pack(side=TOP,
            anchor=W)
        Label(win, text=ai, bg=CLR_MAINBG, padx=4, pady=4).pack(side=TOP,
            anchor=W)
        Label(win, text=gameType, bg=CLR_MAINBG, padx=4, pady=4).pack(side=TOP,
            anchor=W)
        Label(win, text=bgcolour, bg=CLR_MAINBG, padx=4, pady=4).pack(side=TOP,
            anchor=W)
        #Quit child window and return to root window
        Button(win, text='Okay', bg=CLR_BUTTBG, activebackground=CLR_BUTTPRESS,
               command=win.destroy).pack(side=TOP, anchor=E, padx=5, pady=5)

        
class WindowStartGame_MiddleFrame(Frame):
    """ Frame used for the centre part in all WindowStartGames. Contains the
    formatted grid of settings which the user can alter.

    """
    def __init__(self, curRoot):
        """ Create a new WindowStartGame_MiddleFrame.
        Constructor: WindowStartGame_MiddleFrame(Tk)

        curRoot refers to the root Tk class which should be running in the
        background in this process.

        """
        #Place all the labels and horizontal lines
        Frame.__init__(self, curRoot, bg=CLR_FRAMEBG, bd=2, padx=5,
            pady=3, relief=SUNKEN)
        Label(self, text="Your Name:", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=0, sticky=E)
        Frame(self,width=230,bg=CLR_ENTRYHL).grid(row=1, sticky=W+E,
            columnspan=2)
        Label(self, text="Starting Score:",
            bg=CLR_FRAMEBG, font=FNT_LABELFONT).grid(row=2, sticky=E)
        Frame(self,width=230,bg=CLR_ENTRYHL).grid(row=3, sticky=W+E,
            columnspan=2)
        Label(self, text="Player 2 AI:", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=4, sticky=E)
        Frame(self,width=230,bg=CLR_ENTRYHL).grid(row=5, sticky=W+E,
            columnspan=2)
        Label(self, text="Player 3 AI:", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=6, sticky=E)
        Frame(self,width=230,bg=CLR_ENTRYHL).grid(row=7, sticky=W+E,
            columnspan=2)
        Label(self, text="Player 4 AI:", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=8, sticky=E)
        Frame(self,width=230,bg=CLR_ENTRYHL).grid(row=9, sticky=W+E,
            columnspan=2)
        Label(self, text="Game Type:", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=10, sticky=E)
        Frame(self,width=230,bg=CLR_ENTRYHL).grid(row=11, sticky=W+E,
            columnspan=2)
        Label(self, text="Background Colour:", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=12, sticky=E)

        #Define some of the form entrys
        self._namebox = Entry(self,bd=2,relief=RIDGE,highlightcolor=CLR_ENTRYHL,
            highlightthickness=1,insertwidth=1,width=15)
        self._namebox.insert(0, "Mr. Green")
        self._scorebox= Entry(self,bd=2,relief=RIDGE,highlightcolor=CLR_ENTRYHL,
            highlightthickness=1,insertwidth=1,width=15)
        self._scorebox.insert(0, "25000")
        self._gametype = RadioTwoChoices(self, CLR_FRAMEBG, "East Only", "Both")

        #Define the drop down boxes
        aiList = mahjongGlobals.AILIST
        self._ptwovar = StringVar(self)
        self._pthreevar = StringVar(self)
        self._pfourvar = StringVar(self)
        self._ptwovar.set(aiList[0])
        self._pthreevar.set(aiList[0])
        self._pfourvar.set(aiList[0])
        self._ptwolist = OptionMenu(self,self._ptwovar,*aiList)
        self._ptwolist.configure(bg=CLR_BUTTBG,highlightbackground=CLR_FRAMEBG,
            activebackground=CLR_MAINBG,bd=2,relief=RIDGE,cursor='hand2')
        self._pthreelist = OptionMenu(self,self._pthreevar,*aiList)
        self._pthreelist.configure(bg=CLR_BUTTBG,highlightbackground=CLR_FRAMEBG,
            activebackground=CLR_MAINBG,bd=2,relief=RIDGE,cursor='hand2')
        self._pfourlist = OptionMenu(self,self._pfourvar,*aiList)
        self._pfourlist.configure(bg=CLR_BUTTBG,highlightbackground=CLR_FRAMEBG,
            activebackground=CLR_MAINBG,bd=2,relief=RIDGE,cursor='hand2')

        #BG colour drop down
        self._bgcolourvar = StringVar(self)
        self._bgcolourvar.set("Blue")
        self._bgcolour = OptionMenu(self,self._bgcolourvar,"Blue","Red","Green")
        self._bgcolour.configure(bg=CLR_BUTTBG,highlightbackground=CLR_FRAMEBG,
            activebackground=CLR_MAINBG,bd=2,relief=RIDGE,cursor='hand2')

        #Add these form things using .grid()
        self._namebox.grid(row=0, column=1, pady=3, padx=7, sticky=E)
        self._scorebox.grid(row=2, column=1, pady=3, padx=7, sticky=E)
        self._ptwolist.grid(row=4, column=1, pady=3, padx=7, sticky=E)
        self._pthreelist.grid(row=6, column=1, pady=3, padx=7, sticky=E)
        self._pfourlist.grid(row=8, column=1, pady=3, padx=7, sticky=E)
        self._gametype.grid(row=10, column=1, pady=3, padx=7, sticky=E)
        self._bgcolour.grid(row=12, column=1, pady=3, padx=7, sticky=E)

    def returnValues(self):
        """ Atempts to take all the information from the form fields in this
        frame. Errors if any of this data is invalid, popping up an error
        dialog and returning False. Otherwise, returns all the data in these
        fields.

        returnValues() -> either a list of values or False

        """
        try:
            name = self._namebox.get()
            if len(name) == 0:
                raise UserWarning("No name entered.")
            if len(name) > 25:
                raise UserWarning("Name must be less than 26 characters.")
            score = int(self._scorebox.get())
            if score < 10000 or score > 50000:
                raise UserWarning("Score must be between 10,000 and 50,000.")
            p2ai = self._ptwovar.get()
            p3ai = self._pthreevar.get()
            p4ai = self._pfourvar.get()
            gametype = self._gametype.get().get()
                #twice here, one to get the stringVar and the other to get
                #the actual value from that
            bgclr = self._bgcolourvar.get()
        except ValueError:
            err = "Provided score was not an integer value."
            tkMessageBox.showerror(title="Error: Invalid Settings", message=err)
            return False
        except Exception as err:
            tkMessageBox.showerror(title="Error: Invalid Settings", message=err)
            return False 
        return [name, score, p2ai, p3ai, p4ai, gametype, bgclr]


class RadioTwoChoices(Frame):
    """ Frame containing two radio buttons, one of which is a 'yes' and the
    other is a 'no'.

    """
    def __init__(self, curRoot, backcolour, textone, texttwo):
        """ Create a new RadioTwoChoices.
        Constructor: RadioTwoChoices(Tk, colour, string, string)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        backcolour is the background colour of these buttons, given as a
        standard Tkinter colour.
        textone and texttwo are the labels for the 'yes' and 'no' buttons
        respectively.

        """
        Frame.__init__(self, curRoot)
        self._var = IntVar()
        Radiobutton(self, bg=backcolour, activebackground=backcolour,
            text=textone, variable=self._var, value=1).pack(side=LEFT, anchor=W)
        Radiobutton(self, bg=backcolour, activebackground=backcolour,
            text=texttwo, variable=self._var, value=0).pack(side=LEFT, anchor=W)

    def get(self):
        """ Returns the currently selected radio button. """
        return self._var

class WindowNoSaveError(Window):
    """ Error window for not having a save game and attempting to load. Has
    no other functionality beyond being an error message.

    """
    def __init__(self, curRoot, curScreen):
        """ Create a new WindowNoSaveError.
        Constructor: WindowNoSaveError(Tk, MenuScreen)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.

        """
        Window.__init__(self, curRoot, curScreen)
        self._root.title("Error")
        self._root.resizable(False, False)
        Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_TITLEFONT,
            text="Error:").pack(side=TOP, anchor=W, pady=10)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)
        Label(self._root, bg=CLR_MAINBG,
            text="There was no save file found. Please start a new game and\
 save before attempting to load a saved game.").pack(side=TOP, anchor=W,
            padx=5)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)
        self._buttonframe = Frame(self._root, bg=CLR_MAINBG)
        self._buttonframe.pack(side=TOP, fill=X, padx=5, pady=5)
        buttResume = Button(self._buttonframe,text="Okay",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._resumeGame)
        buttResume.pack(side=RIGHT)

    def _resumeGame(self):
        """ Cancel and close this window. """
        self._root.destroy()
        self._curScreen.destroyDialog()


class WindowVolume(Window):
    """ Volume changer window, which allows users to edit the volumes defined
    in the main game file.

    """
    def __init__(self, curRoot, curScreen, startingVolumes):
        """ Create a new WindowVolume.
        Constructor: WindowVolume(Tk, MenuScreen, list of integers)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.
        startingVolumes is a list, 3 elements long, of the three volumes,
        button volume, voice volume and music volume.

        """
        Window.__init__(self, curRoot, curScreen)
        self._root.title("Volume Select")
        self._root.resizable(False, False)
        Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_TITLEFONT,
            text="SOUND SETTINGS").pack(side=TOP, pady=10)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)

        #Define the three volume scalers
        self._buttVol = Scale(self._root, from_=0, to=100, orient=HORIZONTAL,
            bg=CLR_MAINBG, highlightbackground=CLR_MAINBG,
            activebackground=CLR_FRAMEBG, bd=0)
        self._voiceVol = Scale(self._root, from_=0, to=100, orient=HORIZONTAL,
            bg=CLR_MAINBG, highlightbackground=CLR_MAINBG,
            activebackground=CLR_FRAMEBG, bd=0)
        self._musicVol = Scale(self._root, from_=0, to=100, orient=HORIZONTAL,
            bg=CLR_MAINBG, highlightbackground=CLR_MAINBG,
            activebackground=CLR_FRAMEBG, bd=0)

        #Set their initial values
        self._buttVol.set(startingVolumes[0])
        self._voiceVol.set(startingVolumes[1])
        self._musicVol.set(startingVolumes[2])

        #Pack them on the screen with labels
        Label(self._root, bg=CLR_MAINBG,
            text="Button and tile sound volume:").pack(side=TOP, anchor=W,
            padx=5)
        self._buttVol.pack(side=TOP)
        Label(self._root, bg=CLR_MAINBG, text="Voice volume:").pack(side=TOP,
            anchor=W, padx=5)
        self._voiceVol.pack(side=TOP)
        Label(self._root, bg=CLR_MAINBG, text="Music volume:").pack(side=TOP,
            anchor=W, padx=5)
        self._musicVol.pack(side=TOP)
        
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)
        self._buttonframe = Frame(self._root, bg=CLR_MAINBG)
        self._buttonframe.pack(side=TOP, fill=X, padx=5, pady=5)
        buttResume = Button(self._buttonframe,text="Okay",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._resumeGame)
        buttResume.pack(side=RIGHT)

    def _resumeGame(self):
        """ Close this window, passing the volumes to set them. """
        volumes = []
        volumes.append(self._buttVol.get()/100.0)
        volumes.append(self._voiceVol.get()/100.0)
        volumes.append(self._musicVol.get()/100.0)
        self._curScreen.setVolumes(volumes)
        self._root.destroy()
        self._curScreen.destroyDialog()

class WindowCredits(Window):
    """ Credits window, containing information taken from a predefined text
    file.

    """
    def __init__(self, curRoot, curScreen):
        """ Create a new WindowNoSaveError.
        Constructor: WindowNoSaveError(Tk, MenuScreen)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.

        """
        Window.__init__(self, curRoot, curScreen)
        self._root.title("Credits")
        self._root.resizable(False, False)
        Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_TITLEFONT,
            text="Game Credits:").pack(side=TOP, anchor=W, padx=25, pady=10)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)

        f = open(mahjongGlobals.CREDITSPAGE, "rU")
        for line in f:
            line = line.strip()
            if line:
                Label(self._root, bg=CLR_MAINBG, text=line).pack(side=TOP, anchor=W,
                    padx=15)
        f.close()
        
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)
        self._buttonframe = Frame(self._root, bg=CLR_MAINBG)
        self._buttonframe.pack(side=TOP, fill=X, padx=5, pady=5)
        buttResume = Button(self._buttonframe,text="Close",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._resumeGame)
        buttResume.pack(side=RIGHT)

    def _resumeGame(self):
        """ Cancel and close this window. """
        self._root.destroy()
        self._curScreen.destroyDialog()


class WindowGameMenu(Window):
    """ Ingame menu window, containing all relevant buttons.

    """
    def __init__(self, curRoot, curScreen):
        """ Create a new WindowGameMenu.
        Constructor: WindowGameMenu(Tk, MenuScreen)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.

        """
        Window.__init__(self, curRoot, curScreen)
        self._root.title("Game Menu")
        self._root.resizable(False, False)
        Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_TITLEFONT,
            text="GAME MENU").pack(side=TOP, pady=10)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)

        self._buttonframe = Frame(self._root, bg=CLR_MAINBG)
        self._buttonframe.pack(side=TOP, fill=X, padx=5, pady=5)
        buttResume = Button(self._buttonframe,text="Resume",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._resumeGame)
        buttSave = Button(self._buttonframe,text="Save and Quit",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._saveQuitGame)
        buttQuit = Button(self._buttonframe,text="Quit Without Saving",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,
            command=self._quitGame)
        buttResume.pack(side=TOP,fill=X)
        buttSave.pack(side=TOP,fill=X)
        buttQuit.pack(side=TOP,fill=X)

    def _resumeGame(self):
        """ Cancel and close this window. """
        self._root.destroy()
        self._curScreen.destroyDialog()

    def _saveQuitGame(self):
        """ Save the game and then change the screen to the MainMenu. """
        self._root.destroy()
        self._curScreen.destroyDialog()
        self._curScreen.saveGame()
        self._curScreen.changeScreen('MainMenu',None)

    def _quitGame(self):
        """ Change the screen to the MainMenu. """
        self._root.destroy()
        self._curScreen.destroyDialog()
        self._curScreen.changeScreen('MainMenu',None)


class WindowRoundEnd(Window):
    """ Round end window, with a display of the winning hand and a list of yaku,
    along with further info on these yaku.

    """
    def __init__(self, curRoot, curScreen, winInfo):
        """ Create a new WindowRoundEnd.
        Constructor: WindowVolume(Tk, MenuScreen, list)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.
        winInfo is a list of information on the currently ended round:
            winInfo[0] - How the last round ended.
            winInfo[1] - The PlayerScore of who won.
            winInfo[2] - The amount of Fu they had.
            winInfo[3] - The list of yaku in their hand.
            winInfo[4] - The amount of dora they had.
            winInfo[5] - The list of all dora in play.
            winInfo[6] - The list of all ura dora in play, if applicable.
            winInfo[7] - The score of the winning hand.
            winInfo[8] - The name of the score, i.e. 'Mangan' and such.

        """
        Window.__init__(self, curRoot, curScreen)
        self._root.title("End Of Round Results")
        self._root.resizable(False, False)

        #Get info
        roundType = winInfo[0]

        #Top bar
        Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_TITLEFONT,
            text="End Of Round Results").pack(side=TOP, anchor=W, padx=30,
            pady=10)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)

        if roundType == 'ron' or roundType == 'tsumo':
            winningPlayer = winInfo[1]
            handFu = winInfo[2]
            totalYaku = winInfo[3]
            doraAmount = winInfo[4]
            doraList = winInfo[5]
            uraList = winInfo[6]
            handScore = winInfo[7]
            scoreWord = winInfo[8]
            backImgLoc = curScreen.getBackImgLoc()
            #Say player name
            if roundType == 'ron':
                topText = 'Ron by ' + winningPlayer.getName() + ':'
            else:
                topText = 'Tsumo by ' + winningPlayer.getName() + ':'
            Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL,
                text=topText).pack(side=TOP, anchor=W, padx=30, pady=3)
            #Hand display
            handDraw = WindowRoundEnd_DrawHandCanvas(self._root, winningPlayer,
                doraList, uraList, backImgLoc)
            handDraw.pack(side=TOP, padx=10, anchor=W, fill=X)
            Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
                padx=5, pady=5)
            #List of yaku
            Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL,
                text="List of Yaku: (Click on a yaku for more details)").pack(
                side=TOP, anchor=W, padx=30, pady=3)
            listFrame = WindowRoundEnd_YakuFrame(self._root, totalYaku)
            listFrame.pack(side=TOP, anchor=W, fill=X, padx=20, pady=3)
            Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
                padx=5, pady=5)
            #Bottom area
            buttonFrame = Frame(self._root, bg=CLR_MAINBG)
            buttonFrame.pack(side=TOP, fill=X, padx=5, pady=5)
            #Hand Worth
            Label(buttonFrame, bg=CLR_MAINBG, fg=CLR_LABEL,
                text=str(handFu) + " Fu").pack(side=LEFT, anchor=W, padx=10)
            currentHan = 0
            if winningPlayer.isClosed():
                for yaku in totalYaku:
                    if yaku.getScoreClosed() == -1: #if yakuman
                        currentHan = -1
                        break
                    else:
                        currentHan += yaku.getScoreClosed()  
            else:
                for yaku in totalYaku:
                    if yaku.getScoreOpen() == -1: #if yakuman
                        currentHan = -1
                        break
                    else:
                        currentHan += yaku.getScoreOpen()
            if currentHan != -1:
                Label(buttonFrame, bg=CLR_MAINBG, fg=CLR_LABEL,
                    text=str(currentHan) + " Han").pack(side=LEFT, anchor=W,
                    padx=10)
            Label(buttonFrame, bg=CLR_MAINBG, fg=CLR_LABEL,
                text=str(doraAmount) + " Dora").pack(side=LEFT, anchor=W,
                padx=10)
            Label(buttonFrame, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_LABELFONT,
                text=scoreWord).pack(side=LEFT, anchor=W, padx=30)
            Label(buttonFrame, bg=CLR_MAINBG, fg=CLR_LABEL,
                text=str(handScore) + " points").pack(side=LEFT, anchor=W, padx=30)
            #Continue Button
            buttContinue = Button(buttonFrame,text="Resume",bg=CLR_BUTTBG,
                activebackground=CLR_BUTTPRESS,padx=8,command=self._resumeGame)
            buttContinue.pack(side=RIGHT)
        else:
            if roundType == 'nomoretiles':
                topText = 'Draw -- No more tiles remaining in the wall.'
            elif roundType == 'fourkans':
                topText = 'Draw -- Four kans have been declared.'
            elif roundType == 'allriichi':
                topText = 'Draw -- All players have declared riichi.'
            else:
                topText = 'Draw'
            Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL,
                text=topText).pack(side=TOP, anchor=W, padx=30, pady=3)
            Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
                padx=5, pady=5)
            buttonFrame = Frame(self._root, bg=CLR_MAINBG)
            buttonFrame.pack(side=TOP, fill=X, padx=5, pady=5)
            buttContinue = Button(buttonFrame,text="Resume",bg=CLR_BUTTBG,
                activebackground=CLR_BUTTPRESS,padx=8,command=self._resumeGame)
            buttContinue.pack(side=RIGHT)

    def _resumeGame(self):
        """ Cancel and close this window. """
        self._root.destroy()
        self._curScreen.destroyDialog()

class WindowRoundEnd_DrawHandCanvas(Frame):
    """ Frame used for drawing the canvas part of the WindowRoundEnd, with the
    hand that won and everything. Compare with the hand drawing functions in
    gameScreen.py.

    """
    def __init__(self, curRoot, player, doraList, uraList, backImgLoc):
        """ Create a new WindowRoundEnd_DrawHandCanvas.
        Constructor: WindowRoundEnd_DrawHandCanvas(Tk, PlayerScore, list, list,
                                                   string)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        player is the PlayerScore of whoever this hand belongs to.
        doraList is the list of Tiles that are dora.
        uraList is the list of TIles that are ura dora.
        backImgLoc is the file location of the current background image.

        """
        Frame.__init__(self, curRoot, bg=CLR_MAINBG)
        #Draw canvas
        canvas = Canvas(self, bg="white", bd=2, width=650, height=104,
            relief=SUNKEN)
        canvas.pack(side=TOP, padx=4, fill=X)
        canvas.image = []
        
        #Draw background
        canvasBack = self._getImage(backImgLoc)
        canvas.create_image((0,0), image=canvasBack, anchor=NW)
        canvas.image.append(canvasBack)

        #HAND DRAWING:
        curX = 5
        curY = 5
        #Draw mutable
        handMutable = player.getMutable()
        for i, tile in enumerate(handMutable):
            tileImg = self._loadTileImg(tile)
            canvas.create_image((curX,curY), image=tileImg, anchor=NW)
            canvas.image.append(tileImg)
            curX+=mahjongGlobals.TILEWIDTH
            if i == len(handMutable)-2:
                curX+=5
        #Draw immutable
        curX+=5
        handImmutable = player.getImmutable()
        for tileColl in handImmutable:
            for i, tile in enumerate(tileColl.getTileList()):
                if i == tileColl.getSide():
                    tileImg = self._loadTileImgRot(tile)
                    nextStep = mahjongGlobals.TILEHEIGHT
                    topSpace = 10
                elif tileColl.getType == 'kan_cl' and ((i == 1) or (i == 2)):
                    tileImg = self._getImage(mahjongGlobals.TILEBACKIMGLOC)
                    nextStep = mahjongGlobals.TILEWIDTH
                    topSpace = 0
                else:
                    tileImg = self._loadTileImg(tile)
                    nextStep = mahjongGlobals.TILEWIDTH
                    topSpace = 0
                canvas.create_image((curX,curY+topSpace), image=tileImg,
                    anchor=NW)
                canvas.image.append(tileImg)
                curX+=nextStep
            curX+=5
        #Draw dora
        curX = 15
        curY = 60
        for tile in doraList:
            tileImg = self._loadTileImg(tile)
            canvas.create_image((curX,curY), image=tileImg, anchor=NW)
            canvas.image.append(tileImg)
            curX+=mahjongGlobals.TILEWIDTH
        curX += 5
        for tile in uraList:
            tileImg = self._loadTileImg(tile)
            canvas.create_image((curX,curY), image=tileImg, anchor=NW)
            canvas.image.append(tileImg)
            curX+=mahjongGlobals.TILEWIDTH

    def _getImage(self, imageLoc):
        """ Load the image at imageLoc and convert it to a Tk PhotoImage. """
        img = Image.open(imageLoc)
        photo = ImageTk.PhotoImage(img)
        return photo

    def _getImageRot(self, imageLoc):
        """ Load the image at imageLoc, rotate it 90 degrees anticlockwise and
        convert it to a Tk PhotoImage.

        """
        img = Image.open(imageLoc)
        img = img.rotate(90)
        photo = ImageTk.PhotoImage(img)
        return photo
        
    def _loadTileImg(self, tileToLoad):
        """ Load the tile PhotoImage for the given tile. """
        tileFN = str(tileToLoad.getUniqueID()) + ".png"
        tileLoc = os.path.join(mahjongGlobals.TILEIMGLOC, tileFN)
        return self._getImage(tileLoc)

    def _loadTileImgRot(self, tileToLoad):
        """ Load the tile PhotoImage for the given tile, rotated sideways. """
        tileFN = str(tileToLoad.getUniqueID()) + ".png"
        tileLoc = os.path.join(mahjongGlobals.TILEIMGLOC, tileFN)
        return self._getImageRot(tileLoc)

class WindowRoundEnd_YakuFrame(Frame):
    """ Frame used for positioning the list of yaku in WindowRoundEnd, and for
    adding interactive buttons for these yaku

    """
    def __init__(self, curRoot, yakuList):
        Frame.__init__(self, curRoot, bg=CLR_MAINBG)
        leftPortion = Frame(self, bg=CLR_FRAMEBG, bd=2, padx=4,
            pady=3, relief=SUNKEN)
        leftPortion.pack(side=LEFT, fill=Y)
        Label(leftPortion, text="Name of Yaku", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=0, sticky=W)
        Label(leftPortion, text="Han Score", bg=CLR_FRAMEBG,
            font=FNT_LABELFONT).grid(row=0, ipadx=30, column=2, sticky=E)
        for i, yaku in enumerate(yakuList):
            curCommand = lambda m=yaku: self.explainYakuWindow(m)
            curScore = str(yaku.getScoreClosed())
            if curScore == '-1':
                curScore = 'Yakuman'
            Button(leftPortion, text=yaku.getName(), bg=CLR_BUTTOTHERHOVER,
                activebackground=CLR_BUTTOTHERDOWN, relief=RIDGE,
                command=curCommand).grid(row=i+1,sticky=W)
            Label(leftPortion, text=curScore, bg=CLR_FRAMEBG,
                font=FNT_LABELFONT).grid(row=i+1, column=2, sticky=E)

    def explainYakuWindow(self, yaku):
        """ Popup a window with the description for yaku. """
        #Create child window
        win = Toplevel(bg=CLR_MAINBG)
        win.resizable(False, False)
        #Display message
        title = yaku.getName()
        message = yaku.getDesc()
        Label(win, text=title, font=FNT_LABELFONT, bg=CLR_MAINBG, padx=4,
            pady=4).pack(side=TOP, anchor=W)
        Label(win, text=message, bg=CLR_MAINBG, padx=4, pady=4).pack(side=TOP,
            anchor=W)
        #Quit child window and return to root window
        Button(win, text='Okay', bg=CLR_BUTTBG, activebackground=CLR_BUTTPRESS,
               command=win.destroy).pack(side=TOP, anchor=E, padx=5, pady=5)

class WindowGameEnd(Window):
    """ End game window, containing a table breakdown for all the players over
    the course of the game.

    """
    def __init__(self, curRoot, curScreen, finalInfo):
        """ Create a new WindowGameEnd.
        Constructor: WindowGameEnd(Tk, MenuScreen, list)

        curRoot refers to the root Tk class which should be running in the
        background in this process.
        curScreen refers to the MenuScreen that opened up this popup.
        finalInfo is a list of various pieces of game info:
            finalInfo[0] - PlayerScore of whoever won.
            finalInfo[1] - A list of all players in the game.
            finalInfo[2] - A 2D table containing all the scores and roundnames
                           at each point in the game.

        """
        Window.__init__(self, curRoot, curScreen)
        self._root.title("End Game Results")
        self._root.resizable(False, False)

        playerWon = finalInfo[0]
        allPlayers = finalInfo[1]
        winTable = finalInfo[2]

        #Top bar
        Label(self._root, bg=CLR_MAINBG, fg=CLR_LABEL, font=FNT_TITLEFONT,
            text="Game Over - " + playerWon.getName() + " Wins").pack(side=TOP,
            anchor=W, padx=30, pady=10)
        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)

        #Player scores list
        scoreTable = Frame(self._root,bg=CLR_ENTRYHL, bd=2, relief=SUNKEN)
        for x, player in enumerate(allPlayers):
            Label(scoreTable, text=player.getName(), bg=CLR_FRAMEBG, width=20,
                height=1, font=FNT_LABELFONT).grid(row=0, column=x+1, sticky=E,
                pady=1, padx=1)
        for i, row in enumerate(winTable):
            for j, value in enumerate(row):
                if i != 0:
                    Label(scoreTable, text=str(value), bg=CLR_FRAMEBG, width=23,
                        height=1).grid(row=j+1, column=i, sticky=E)
                else:
                    Label(scoreTable, text=str(value), bg=CLR_FRAMEBG, width=30,
                        height=1, font=FNT_LABELFONT).grid(row=j+1, column=i,
                        sticky=E, pady=1, padx=1)
        scoreTable.pack(side=TOP, fill=X, padx=5, pady=5)

        Frame(self._root,height=1,bg=CLR_ENTRYHL).pack(side=TOP, fill=X,
            padx=5, pady=5)
        buttonFrame = Frame(self._root, bg=CLR_MAINBG)
        buttonFrame.pack(side=TOP, fill=X, padx=5, pady=5)
        buttContinue = Button(buttonFrame,text="Quit",bg=CLR_BUTTBG,
            activebackground=CLR_BUTTPRESS,padx=8,command=self._resumeGame)
        buttContinue.pack(side=RIGHT)

    def _resumeGame(self):
        """ Cancel and close this window. """
        self._root.destroy()
        self._curScreen.destroyDialog()
        self._curScreen.changeScreen('MainMenu',None)
