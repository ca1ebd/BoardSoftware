#!/usr/bin/env python
import argparse
import time
import sys
import os
import rgbmatrix.core
import threading
import datetime
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

class FootballBoard:
    mainMenuText = "Select Option\n\n1) Set down and yards\n2) Set Home Points\n3) Set Away Points\n4) Set Quarter\n5) Set Clock\n6) Start/Stop Clock\n"
    def __init__(self):
        self.stoppedClock = threading.Event()
        self.font = graphics.Font()
        self.headerFont = graphics.Font()
        self.scoreFont = graphics.Font()
        self.font.LoadFont("../fonts/7x13B.bdf")
        self.headerFont.LoadFont("../fonts/7x13B.bdf")
        options = RGBMatrixOptions()
        options.rows = 16
        options.cols = 32
        options.chain_length = 3
        options.parallel = 3
        options.multiplexing = 3
        options.row_address_type = 2
        options.brightness = 100
        self.homeName = "HOME"
        self.awayName = "AWAY"
        self.homeColor = graphics.Color(0, 0, 255)
        self.awayColor = graphics.Color(0, 0, 255)
        self.colorMode = 0
        self.scoreImage = [[],[]]
        self.scoreImage[0] = []
        self.scoreImage[0].append(Image.open('res/bb_0.png'))
        self.scoreImage[0].append(Image.open('res/bb_1.png'))
        self.scoreImage[0].append(Image.open('res/bb_2.png'))
        self.scoreImage[0].append(Image.open('res/bb_3.png'))
        self.scoreImage[0].append(Image.open('res/bb_4.png'))
        self.scoreImage[0].append(Image.open('res/bb_5.png'))
        self.scoreImage[0].append(Image.open('res/bb_6.png'))
        self.scoreImage[0].append(Image.open('res/bb_7.png'))
        self.scoreImage[0].append(Image.open('res/bb_8.png'))
        self.scoreImage[0].append(Image.open('res/bb_9.png'))

        self.scoreImage[1].append(Image.open('res/bb_0_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_1_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_2_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_3_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_4_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_5_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_6_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_7_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_8_w.png'))
        self.scoreImage[1].append(Image.open('res/bb_9_w.png'))

        self.downImg = []
        self.downImg.append(Image.open('res/down.png'))
        self.downImg.append(Image.open('res/down_w.png'))

        self.yardsImg = []
        self.yardsImg.append(Image.open('res/yards.png'))
        self.yardsImg.append(Image.open('res/yards_w.png'))

        self.clockSepImg = []
        self.clockSepImg.append(Image.open('res/clocksep.png'))
        self.clockSepImg.append(Image.open('res/clocksep_w.png'))

        self.quarterColor = []
        self.quarterColor.append(graphics.Color(255, 255, 255))
        self.quarterColor.append(graphics.Color(50, 0, 50))

        self.quarterHeaderColor = []
        self.quarterHeaderColor.append(graphics.Color(255, 255, 0))
        self.quarterHeaderColor.append(graphics.Color(100, 100, 0))

        self.firstClockStart = True
        self.down = 1
        self.yards = 10
        self.gameClock = 900000000
        self.homeScore = 0
        self.awayScore = 0
        self.quarter = 1
        self.headerYOffset = 10
        self.homeHeaderXOffset = 63
        self.quarterHeaderOffset = 43
        self.quarterNumberOffset = 51
        self.yardsHeaderXOffset = 20
        self.yardsNumberXOffset = 30
        self.downHeaderXOffset = 1
        self.downNumberXOffset = 11
        self.clockMinutesXOffset = 65
        self.clockSepXOffset = 79
        self.clockSecondsXOffset = 82
        self.yardsdownYOffset = 38
        self.yardsdownTextYOffset = self.yardsdownYOffset + 9
        self.homeScoreLeadingDigitXOffset = 60
        self.homeScoreTrailingDigitXOffset = 77
        self.awayScoreLeadingDigitXOffset = 2
        self.awayScoreTrailingDigitXOffset = 19
        self.scoreYOffset = 12
        self.matrix = RGBMatrix(options = options)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.timer = threading.Timer(.05, self.drawClock)
        self.redrawDisplay()
        #self.mainMenu()
#
#     def mainMenu(self):
#         while True:
# #			os.system('clear')
#             try:
#                 menuResp = input(self.mainMenuText)
#                 if menuResp == 1:
#                     self.setyardsAndDown()
#                 if menuResp == 2:
#                     self.setHomeScore()
#                 if menuResp == 3:
#                     self.setAwayScore()
#                 if menuResp == 4:
#                     self.setQuarter()
#                 if menuResp == 5:
#                     self.setClock()
#                 if menuResp == 6:
#                     self.startStopClock()
#             except SyntaxError:
#                 print("\nPlease enter a valid value\n")
#             except KeyboardInterrupt:
#                 self.stoppedClock.set()
#                 sys.exit()


    def setColorMode(self):
        self.colorMode = self.colorMode ^ 1
        self.redrawDisplay()

    def startStopClock(self, dataNotUsed):
        if self.stoppedClock.is_set() or self.firstClockStart:
            self.stoppedClock.clear()
            self.timer = threading.Timer(.05, self.drawClock)
            self.timer.start()
        else:
            self.stoppedClock.set()

    # def setyardsAndDown(self):
    # 	os.system('clear')
    # 	self.yards = input("\nHow many yards?\n")
    # 	self.down = input("\nHow many down?\n")
    # 	self.redrawDisplay()

    def setYards(self, yards):
        self.yards = yards
        self.redrawDisplay()

    def setDown(self, down):
        self.down = down
        self.redrawDisplay()

    def setClock(self, newTime):
        clockStr = newTime
        tm = time.strptime(clockStr, "%M:%S")
        print(clockStr)
        self.gameClock = (tm.tm_sec + (60 * tm.tm_min)) * 1000000
        print(self.gameClock)
        self.redrawDisplay()

    def setQuarter(self, quarter):
        self.quarter = quarter
        self.redrawDisplay()

    def setAwayScore(self, score):
        self.awayScore = score
        self.redrawDisplay()

    def setHomeScore(self, score):
        self.homeScore = score
        self.redrawDisplay()

    def setHomeColor(self, colorJson):
        colorObject = json.loads(colorJson)
        red = colorObject["R"]
        green = colorObject["G"]
        blue = colorObject["B"]
        self.homeColor = graphics.Color(red, green, blue)
        self.redrawDisplay()

    def setAwayColor(self, colorJson):
        colorObject = json.loads(colorJson)
        red = colorObject["R"]
        green = colorObject["G"]
        blue = colorObject["B"]
        self.awayColor = graphics.Color(red, green, blue)
        self.redrawDisplay()

    def setHomeName(self, name):
        self.homeName = name
        self.redrawDisplay()

    def setAwayName(self, name):
        self.awayName = name
        self.redrawDisplay()

    def setBrightness(self, brightness):
        self.matrix.brightness = int(brightness)
        self.redrawDisplay()

    def redrawDisplay(self):
        self.offscreen_canvas.Clear()
        if self.colorMode == 1:
            for x in range(0, self.matrix.width):
                for y in range(0, self.matrix.width):
                            self.offscreen_canvas.SetPixel(x, y, 255, 255, 255)
        graphics.DrawText(self.offscreen_canvas, self.headerFont, 2, self.headerYOffset, self.awayColor, self.awayName)
        graphics.DrawText(self.offscreen_canvas, self.headerFont, self.quarterHeaderOffset, self.headerYOffset, self.quarterHeaderColor[self.colorMode], "Q")
        graphics.DrawText(self.offscreen_canvas, self.headerFont, self.quarterNumberOffset, self.headerYOffset, self.quarterColor[self.colorMode], str(self.quarter))
        graphics.DrawText(self.offscreen_canvas, self.headerFont, self.homeHeaderXOffset, self.headerYOffset, self.homeColor, self.homeName)
        graphics.DrawText(self.offscreen_canvas, self.scoreFont, self.homeHeaderXOffset, self.headerYOffset, graphics.Color(0, 255, 0), "00")
        graphics.DrawText(self.offscreen_canvas, self.font, self.downNumberXOffset, self.yardsdownTextYOffset, self.quarterColor[self.colorMode], str(self.down))
        graphics.DrawText(self.offscreen_canvas, self.font, self.yardsNumberXOffset, self.yardsdownTextYOffset, self.quarterColor[self.colorMode], str(self.yards))
        graphics.DrawText(self.offscreen_canvas, self.font, self.clockMinutesXOffset, self.yardsdownTextYOffset, graphics.Color(0, 0, 255),str(datetime.timedelta(microseconds=self.gameClock))[2:4])
        graphics.DrawText(self.offscreen_canvas, self.font, self.clockSecondsXOffset, self.yardsdownTextYOffset, graphics.Color(0, 0, 255),str(datetime.timedelta(microseconds=self.gameClock))[5:7])

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        self.matrix.SetImage(self.downImg[self.colorMode].convert('RGB'), self.downHeaderXOffset, self.yardsdownYOffset)
        self.matrix.SetImage(self.yardsImg[self.colorMode].convert('RGB'), self.yardsHeaderXOffset, self.yardsdownYOffset)

        self.matrix.SetImage(self.clockSepImg[self.colorMode].convert('RGB'), self.clockSepXOffset, self.yardsdownYOffset)
        self.drawScore()

    def drawScore(self):
        homeString = str(self.homeScore).zfill(2)
        awayString = str(self.awayScore).zfill(2)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(awayString[:1])].convert('RGB'), self.awayScoreLeadingDigitXOffset, self.scoreYOffset)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(awayString[1:])].convert('RGB'), self.awayScoreTrailingDigitXOffset, self.scoreYOffset)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(homeString[:1])].convert('RGB'), self.homeScoreLeadingDigitXOffset, self.scoreYOffset)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(homeString[1:])].convert('RGB'), self.homeScoreTrailingDigitXOffset, self.scoreYOffset)

    def drawClock(self):
        self.firstClockStart = False
        lastSecond = 0
        dt = datetime.datetime.now()
        gameClockStart = dt.microsecond + (dt.second * 1000000) + (dt.minute * 60000000) + self.gameClock
        while not self.stoppedClock.is_set():
            time.sleep(.025)
            dt = datetime.datetime.now()
            currentRemainder = dt.microsecond
            if currentRemainder > 20000 and currentRemainder < 60000:
                self.gameClock = gameClockStart - (dt.microsecond + (dt.second * 1000000) + (dt.minute * 60000000))
                #print(datetime.timedelta(microseconds=self.gameClock).seconds)
                if datetime.timedelta(microseconds=self.gameClock).seconds == 0:
                    #print(datetime.timedelta(microseconds=self.gameClock))
                    self.redrawDisplay()
                    self.stoppedClock.set()
                else:
                    self.redrawDisplay()

