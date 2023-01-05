#!/bin/python
##############################################################################
#
#            skins: Skins First Pass
#    creation date: 2022-07-04
#           author: M. Nagle
#
##############################################################################
# Revisions
##############################################################################
# 2022-07-04  MFN1360  Revision 1.0  File Creation
########################################################################
# 1 - Import
########################################################################
import os
import random as r
import time
from time import sleep as sl
from datetime import datetime
import threading
import wx
import wx.lib.ticker as tick

########################################################################
# 2 - Globals
########################################################################
global colorBlack
colorBlack = (0, 0, 0)
global colorWhite
colorWhite = (255, 255, 255)
global colorBlue
colorBlue = (0, 0, 200)
global colorLightGrey
colorLightGrey = (200, 200, 200)
global colorGold
colorGold = (255, 215, 0)
global colorRed
colorRed = (200, 0, 0)
global colorGreen
colorGreen = (0, 200, 0)
global colorDefault
colorDefault = (-1, -1, -1, 255)
global dt_string
now = datetime.now()
dt_string = str(now.strftime("%Y%m%d%H%M%S")) + ".txt"


class GameLoop(threading.Thread):
    def __init__(self, parent, numgames1):
        threading.Thread.__init__(self)
        self._parent = parent
        self.parent = parent
        self.numgames = numgames1

    def run(self):
        global chosenNum
        global gn
        global chosenUserNum
        global gameactive
        gameactive = True

        gn = 1
        while gameactive:
            evtPostEventStartingSoon = StartingSoon(eventTypeStartingSoon)
            wx.PostEvent(self._parent, evtPostEventStartingSoon)
            sl(30)
            evtPostEventStartRound = StartRound(eventTypeStartRound)
            wx.PostEvent(self._parent, evtPostEventStartRound)
            chosenNum = []
            chosenUserNum = []
            c = 0
            while c < 20:
                val = r.randint(1, 80)
                if val not in chosenNum:
                    chosenNum.append(val)
                    if val in userNumbers:
                        chosenUserNum.append(val)
                    c += 1
                    evtPostEventUpdateBoard = UpdateBoard(eventTypeNumSelBoardUpdate)
                    wx.PostEvent(self._parent, evtPostEventUpdateBoard)
                    sl(3)
            evtPostEventEndRound = EndRound(eventTypeEndRound)
            wx.PostEvent(self._parent, evtPostEventEndRound)
            sl(10)
            gn += 1
            if len(chosenUserNum) == 1:
                gameactive = False
                evtPostEventEndGame = EndGame(eventTypeEndGame)
                wx.PostEvent(self._parent, evtPostEventEndGame)
            sl(140)


class UpdateBoard(wx.PyCommandEvent):
    def __init__(self, etype):
        wx.PyCommandEvent.__init__(self, etype)


class StartingSoon(wx.PyCommandEvent):
    def __init__(self, etype):
        wx.PyCommandEvent.__init__(self, etype)


class StartRound(wx.PyCommandEvent):
    def __init__(self, etype):
        wx.PyCommandEvent.__init__(self, etype)


class EndRound(wx.PyCommandEvent):
    def __init__(self, etype):
        wx.PyCommandEvent.__init__(self, etype)


class EndGame(wx.PyCommandEvent):
    def __init__(self, etype):
        wx.PyCommandEvent.__init__(self, etype)


class PancakeFrame(wx.Frame):
    def __init__(self):
        # Initialize Frame
        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]
        super().__init__(None, title="Skins", size=(screenWidth - 150, screenHeight - 150))

        # Revision
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(__file__)
        self.vRevDate = time.ctime(mtime)
        self.vRevision = "Revision 4.2"
        self.vRevOprid = "PancakeGuy (mnagle14@gmail.com)"

        # Create Notebook
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        self.nbTabConfig = PanelConfig(nb)
        self.nbTabBingo = PanelBingo(nb)
        nb.AddPage(self.nbTabConfig, "Setup")
        nb.AddPage(self.nbTabBingo, "Game")

        # Frame Sizer
        mainSizer = wx.BoxSizer()
        mainSizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(mainSizer)
        self.Maximize(True)


class PanelConfig(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = self.GetParent().GetGrandParent()

        global userNumbers
        userNumbers = {}
        choiceNumbers = []
        for i in range(1, 81):
            choiceNumbers.append(str(i))
        choiceGames = [str("∞")]
        for j in range(1, 10):
            choiceGames.append(str(j))

        self.btAdd = wx.Button(self, label="Add User")
        self.btDelete = wx.Button(self, label="Delete User")
        self.tcName = wx.TextCtrl(self)
        self.chNumbers = wx.Choice(self, choices=choiceNumbers)

        self.lcUsers = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lcUsers.InsertColumn(0, "Number")
        self.lcUsers.InsertColumn(1, "Name                   ")

        self.szConfigCol1Row2 = wx.BoxSizer()
        self.szConfigCol1Row2.Add(wx.StaticText(self, label="Name"), 1, wx.ALL, 5)
        self.szConfigCol1Row2.Add(self.tcName, 2, wx.EXPAND | wx.ALL, 5)

        self.szConfigCol1Row3 = wx.BoxSizer()
        self.szConfigCol1Row3.Add(wx.StaticText(self, label="Number"), 1, wx.ALL, 5)
        self.szConfigCol1Row3.Add(self.chNumbers, 2, wx.EXPAND | wx.ALL, 5)

        self.szConfigCol1Row4 = wx.BoxSizer()
        self.szConfigCol1Row4.Add(self.btAdd, 1, wx.ALL, 5)
        self.szConfigCol1Row4.Add(self.btDelete, 1, wx.ALL, 5)

        self.szConfigCol1 = wx.BoxSizer(wx.VERTICAL)
        self.szConfigCol1.Add(wx.StaticText(self, label="User Setup"), 0, wx.ALL | wx.CENTRE, 5)
        self.szConfigCol1.Add(self.szConfigCol1Row2, 0, wx.ALL | wx.LEFT, 5)
        self.szConfigCol1.Add(self.szConfigCol1Row3, 0, wx.ALL | wx.LEFT, 5)
        self.szConfigCol1.Add(self.szConfigCol1Row4, 0, wx.ALL | wx.LEFT, 5)

        self.szConfigCol2 = wx.BoxSizer(wx.VERTICAL)
        self.szConfigCol2.Add(self.lcUsers, -1, wx.EXPAND)

        self.szConfig = wx.BoxSizer(wx.HORIZONTAL)
        self.szConfig.Add(self.szConfigCol1, 1, wx.EXPAND | wx.ALL, 5)
        self.szConfig.Add(self.szConfigCol2, 5, wx.EXPAND | wx.ALL, 5)

        self.btAdd.Bind(wx.EVT_BUTTON, self.adduser)
        self.btDelete.Bind(wx.EVT_BUTTON, self.deleteuser)

        # Layouts
        self.SetSizer(self.szConfig)
        self.Layout()

    def adduser(self, event):
        global userNumbers
        userNumbers[int(self.chNumbers.GetString(self.chNumbers.GetCurrentSelection()))] = str(self.tcName.GetValue())
        self.lcUsers.DeleteAllItems()
        for dikey, divalue in sorted(userNumbers.items()):
            icount = int(self.lcUsers.GetItemCount())
            self.lcUsers.InsertItem(icount, str(dikey))
            self.lcUsers.SetItem(icount, 1, str(divalue))

    def deleteuser(self, event):
        if self.lcUsers.GetFocusedItem() != -1:
            del userNumbers[int(self.lcUsers.GetItemText(self.lcUsers.GetFocusedItem(), col=0))]
        self.lcUsers.DeleteAllItems()
        for dikey, divalue in sorted(userNumbers.items()):
            icount = int(self.lcUsers.GetItemCount())
            self.lcUsers.InsertItem(icount, str(dikey))
            self.lcUsers.SetItem(icount, 1, str(divalue))


class PanelBingo(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = self.GetParent().GetGrandParent()

        self.szKenoRow1 = wx.BoxSizer()
        self.szKenoRow2 = wx.BoxSizer()
        self.szKenoRow3 = wx.BoxSizer()
        self.szKenoRow4 = wx.BoxSizer()
        self.szKenoRow5 = wx.BoxSizer()
        self.szKenoRow6 = wx.BoxSizer()
        self.szKenoRow7 = wx.BoxSizer()
        self.szKenoRow8 = wx.BoxSizer()
        self.szKenoRow9 = wx.BoxSizer()
        self.kenoSizer = wx.BoxSizer(wx.VERTICAL)

        textstr1 = "Skins"
        font = wx.Font(36, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.tickerCtl = tick.Ticker(self, wx.ID_ANY, text=textstr1, fgcolor=colorWhite, bgcolor=colorBlack, fps=25)
        self.tickerCtl.SetFont(font)
        self.szKenoRow5.Add(self.tickerCtl, 1, wx.EXPAND | wx.CENTRE | wx.ALL, 2)

        self.btStartSkins = wx.Button(self, -1, "Start")
        self.btStopSkins = wx.Button(self, -1, "Stop")
        self.szStartStop = wx.BoxSizer()
        self.szStartStop.Add(self.btStartSkins, 0, wx.CENTRE | wx.ALL, 5)
        self.szStartStop.Add(self.btStopSkins, 0, wx.CENTRE | wx.ALL, 5)
        self.stLastNumber = wx.StaticText(self, label="  ", style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE)
        font = wx.Font(72, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.stLastNumber.SetFont(font)
        self.stLastNumber.SetBackgroundColour(colorLightGrey)
        self.stLastNumber.SetForegroundColour(colorBlack)

        self.lcKnUsers = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lcKnUsers.InsertColumn(0, "Number")
        self.lcKnUsers.InsertColumn(1, "Name                    ")
        self.lcKnUsers.SetBackgroundColour(colorBlack)
        self.lcKnUsers.SetForegroundColour(colorWhite)

        self.sidebarSizer = wx.BoxSizer(wx.VERTICAL)
        self.sidebarSizer.Add(self.stLastNumber, 0, wx.ALL | wx.CENTRE, 5)
        self.sidebarSizer.Add(self.lcKnUsers, 1, wx.ALL | wx.EXPAND, 5)
        self.sidebarSizer.Add(self.szStartStop, 0, wx.ALL | wx.CENTRE, 5)

        self.btStartSkins.Bind(wx.EVT_BUTTON, self.eventskinsstart)
        self.btStopSkins.Bind(wx.EVT_BUTTON, self.eventskinsstop)
        self.Bind(eventBinderNumSelBoardUpdate, self.eventupdateboard)
        self.Bind(eventBinderStartingSoon, self.eventstartingsoon)
        self.Bind(eventBinderEndRound, self.eventendround)
        self.Bind(eventBinderEndGame, self.eventendgame)
        self.Bind(eventBinderStartRound, self.eventstartround)

        for w in range(1, 81):
            font = wx.Font(52, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            exec('self.st' + str(w) + ' = wx.StaticText(self,label="' + str(w) + '",style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE)')
            exec('self.st' + str(w) + '.SetBackgroundColour(colorLightGrey)')
            exec('self.st' + str(w) + '.SetForegroundColour(colorBlack)')
            exec('self.st' + str(w) + '.SetFont(font)')
            if w in range(1, 11):
                exec('self.szKenoRow1.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')
            if w in range(11, 21):
                exec('self.szKenoRow2.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')
            if w in range(21, 31):
                exec('self.szKenoRow3.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')
            if w in range(31, 41):
                exec('self.szKenoRow4.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')
            if w in range(41, 51):
                exec('self.szKenoRow6.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')
            if w in range(51, 61):
                exec('self.szKenoRow7.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')
            if w in range(61, 71):
                exec('self.szKenoRow8.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')
            if w in range(71, 81):
                exec('self.szKenoRow9.Add(self.st' + str(w) + ',1,wx.ALL|wx.EXPAND,5)')

        self.kenoSizer.Add(self.szKenoRow1, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow2, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow3, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow4, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow5, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow6, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow7, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow8, 1, wx.ALL | wx.EXPAND, 5)
        self.kenoSizer.Add(self.szKenoRow9, 1, wx.ALL | wx.EXPAND, 5)

        # Layouts
        self.allSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.allSizer.Add(self.kenoSizer, 8, wx.ALL | wx.EXPAND, 2)
        self.allSizer.Add(self.sidebarSizer, 2, wx.ALL | wx.EXPAND, 2)
        self.SetSizer(self.allSizer)
        self.Layout()

    def eventskinsstart(self, event):
        font2 = wx.Font(18, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.lcKnUsers.DeleteAllItems()
        for dikey, divalue in sorted(userNumbers.items()):
            icount = int(self.lcKnUsers.GetItemCount())
            self.lcKnUsers.InsertItem(icount, str(dikey))
            self.lcKnUsers.SetItem(icount, 1, str(divalue))
            self.lcKnUsers.SetItemFont(icount, font2)
            self.lcKnUsers.SetColumnWidth(0, -2)
            self.lcKnUsers.SetColumnWidth(1, -2)
        self.lcKnUsers.SortItems(1)
        self.btStartSkins.Disable()
        self.btStopSkins.Enable()
        self.worker = GameLoop(self, 0)
        self.worker.start()

    def eventskinsstop(self, event):
        gameactive = False

    def eventendgame(self, event):
        self.btStartSkins.Enable()
        self.btStopSkins.Disable()

    def eventstartingsoon(self, event):
        self.tickerCtl.SetText("Game #" + str(gn) + " Starting Soon!")
        for listnum in range(self.lcKnUsers.GetItemCount()):
            self.lcKnUsers.SetItemBackgroundColour(listnum, colorBlack)
            self.lcKnUsers.SetItemTextColour(listnum, colorWhite)
        for y in range(1, 81):
            exec('self.st' + str(y) + '.SetBackgroundColour(colorLightGrey)')
            exec('self.st' + str(y) + '.SetForegroundColour(colorBlack)')

    def eventstartround(self, event):
        self.tickerCtl.SetText("Game #" + str(gn) + " in Progress")

    def eventendround(self, event):
        chosenNum.sort()
        if len(chosenUserNum) == 1:
            self.tickerCtl.SetText("Game #" + str(gn) + " (GAME OVER): " + str(chosenNum))
        elif len(chosenUserNum) == 0:
            self.tickerCtl.SetText("Game #" + str(gn) + " (NO NUMBERS PICKED): " + str(chosenNum))
        else:
            self.tickerCtl.SetText("Game #" + str(gn) + " (TWO-TIE-ALL-TIE): " + str(chosenNum))
        self.stLastNumber.SetLabel(str("  "))
        with open(dt_string, "a+") as writeFile:
            writeFile.write("Game #" + str(gn) + ": " + str(chosenNum) + "\n")

    def eventupdateboard(self, event):
        for val in chosenNum:
            exec('self.st' + str(val) + '.SetBackgroundColour(colorBlue)')
            exec('self.st' + str(val) + '.SetForegroundColour(colorWhite)')
        self.stLastNumber.SetLabel(str(chosenNum[-1]).rjust(2, " "))
        for val in chosenUserNum:
            exec('self.st' + str(val) + '.SetBackgroundColour(colorRed)')
            exec('self.st' + str(val) + '.SetForegroundColour(colorWhite)')

            for listnum in range(self.lcKnUsers.GetItemCount()):
                if int(self.lcKnUsers.GetItemText(listnum, 0)) == int(val):
                    self.lcKnUsers.SetItemBackgroundColour(listnum, colorRed)
                    self.lcKnUsers.SetItemTextColour(listnum, colorWhite)


if __name__ == '__main__':
    eventTypeNumSelBoardUpdate = wx.NewEventType()
    eventBinderNumSelBoardUpdate = wx.PyEventBinder(eventTypeNumSelBoardUpdate, 1)
    eventTypeStartingSoon = wx.NewEventType()
    eventBinderStartingSoon = wx.PyEventBinder(eventTypeStartingSoon, 1)
    eventTypeEndRound = wx.NewEventType()
    eventBinderEndRound = wx.PyEventBinder(eventTypeEndRound, 1)
    eventTypeStartRound = wx.NewEventType()
    eventBinderStartRound = wx.PyEventBinder(eventTypeStartRound, 1)
    eventTypeEndGame = wx.NewEventType()
    eventBinderEndGame = wx.PyEventBinder(eventTypeEndGame, 1)
    app = wx.App(False)
    PancakeFrame().Show()
    app.MainLoop()
