#!/usr/bin/env python
import argparse
import time
import sys
import os
import rgbmatrix.core
import threading
import datetime
import json

sys.path.append('/usr/local/lib/python2.7/dist-packages/rgbmatrix/')
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

class BaseballBoard:
    def __init__(self):
        self.killEvent = threading.Event()
        self.font = graphics.Font()
        self.headerFont = graphics.Font()
        self.scoreFont = graphics.Font()
        self.font.LoadFont("../fonts/7x13B.bdf")
        self.headerFont.LoadFont("../fonts/7x13B.bdf")
        self.homeName = "HOME"
        self.awayName = "AWAY"
        self.homeColor = graphics.Color(0, 0, 255)
        self.awayColor = graphics.Color(0, 0, 255)
        self.options = RGBMatrixOptions()
        self.options.rows = 16
        self.options.cols = 32
        self.options.chain_length = 3
        self.options.parallel = 3
        self.options.multiplexing = 3
        self.options.row_address_type = 2
        self.options.brightness = 100
        self.colorMode = 0
        self.scoreImage = [[], []]
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

        self.ballsImg = []
        self.ballsImg.append(Image.open('res/balls.png'))
        self.ballsImg.append(Image.open('res/balls_w.png'))

        self.strikesImg = []
        self.strikesImg.append(Image.open('res/strikes.png'))
        self.strikesImg.append(Image.open('res/strikes_w.png'))

        self.outsImg = []
        self.outsImg.append(Image.open('res/outs.png'))
        self.outsImg.append(Image.open('res/outs_w.png'))

        self.clockSepImg = []
        self.clockSepImg.append(Image.open('res/clocksep.png'))
        self.clockSepImg.append(Image.open('res/clocksep_w.png'))

        self.inningColor = []
        self.inningColor.append(graphics.Color(255, 255, 255))
        self.inningColor.append(graphics.Color(50, 0, 50))

        self.inningArrowColor = []
        self.inningArrowColor.append(graphics.Color(255, 255, 0))
        self.inningArrowColor.append(graphics.Color(100, 100, 0))

        self.balls = 0
        self.strikes = 0
        self.outs = 0
        self.homeScore = 0
        self.awayScore = 0
        self.inningHalf = "t"
        self.inning = 1
        self.headerYOffset = 10
        self.homeHeaderXOffset = 63
        self.inningArrowOffset = 43
        self.inningNumberOffset = 51
        self.strikesHeaderXOffset = 20
        self.strikesNumberXOffset = 30
        self.ballsHeaderXOffset = 1
        self.ballsNumberXOffset = 11
        self.outsHeaderXOffset = 39
        self.outsNumberXOffset = 49
        self.clockHoursXOffset = 65
        self.clockSepXOffset = 79
        self.clockMinutesXOffset = 82
        self.strikesBallsYOffset = 38
        self.strikesBallsTextYOffset = self.strikesBallsYOffset + 9
        self.homeScoreLeadingDigitXOffset = 60
        self.homeScoreTrailingDigitXOffset = 77
        self.awayScoreLeadingDigitXOffset = 2
        self.awayScoreTrailingDigitXOffset = 19
        self.scoreYOffset = 12
        self.matrix = RGBMatrix(options=self.options)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.timer = threading.Timer(.25, self.drawClock)
        self.timer.start()
        self.redrawDisplay()

    def setBalls(self, balls):
        self.balls = int(balls)
        self.redrawDisplay()

    def setStrikes(self, strikes):
        self.strikes = int(strikes)
        self.redrawDisplay()

    def setOuts(self, outs):
        self.outs = int(outs)
        self.redrawDisplay()

    def setHomeScore(self, score):
        self.homeScore = int(score)
        self.redrawDisplay()

    def setAwayScore(self, score):
        self.awayScore = int(score)
        self.redrawDisplay()

    def setInning(self, inning):
        self.inning = int(inning[0])
        self.inningHalf = inning[1]
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

    #drawing
    def redrawDisplay(self):
        self.offscreen_canvas.Clear()
        if self.colorMode == 1:
            for x in range(0, self.matrix.width):
                for y in range(0, self.matrix.width):
                    self.offscreen_canvas.SetPixel(x, y, 255, 255, 255)
        graphics.DrawText(self.offscreen_canvas, self.headerFont, 2, self.headerYOffset, self.awayColor, self.awayName)
        if self.inningHalf == "b":
            graphics.DrawText(self.offscreen_canvas, self.headerFont, self.inningArrowOffset, self.headerYOffset, self.inningArrowColor[self.colorMode], u"\u2193")
        else:
            graphics.DrawText(self.offscreen_canvas, self.headerFont, self.inningArrowOffset, self.headerYOffset, self.inningArrowColor[self.colorMode], u"\u2191")
        graphics.DrawText(self.offscreen_canvas, self.headerFont, self.inningNumberOffset, self.headerYOffset, self.inningColor[self.colorMode], str(self.inning))
        graphics.DrawText(self.offscreen_canvas, self.headerFont, self.homeHeaderXOffset, self.headerYOffset, self.homeColor, self.homeName)
        graphics.DrawText(self.offscreen_canvas, self.scoreFont, self.homeHeaderXOffset, self.headerYOffset, graphics.Color(0, 255, 0), "00")
        graphics.DrawText(self.offscreen_canvas, self.font, self.ballsNumberXOffset, self.strikesBallsTextYOffset, self.inningColor[self.colorMode], str(self.balls))
        graphics.DrawText(self.offscreen_canvas, self.font, self.strikesNumberXOffset, self.strikesBallsTextYOffset, self.inningColor[self.colorMode], str(self.strikes))
        graphics.DrawText(self.offscreen_canvas, self.font, self.clockHoursXOffset, self.strikesBallsTextYOffset, graphics.Color(0, 0, 255),datetime.datetime.now().strftime("%I"))
        graphics.DrawText(self.offscreen_canvas, self.font, self.clockMinutesXOffset, self.strikesBallsTextYOffset, graphics.Color(0, 0, 255),datetime.datetime.now().strftime("%M"))
        graphics.DrawText(self.offscreen_canvas, self.font, self.outsNumberXOffset, self.strikesBallsTextYOffset, self.inningColor[self.colorMode], str(self.outs))
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        self.matrix.SetImage(self.ballsImg[self.colorMode].convert('RGB'), self.ballsHeaderXOffset, self.strikesBallsYOffset)
        self.matrix.SetImage(self.strikesImg[self.colorMode].convert('RGB'), self.strikesHeaderXOffset, self.strikesBallsYOffset)
        self.matrix.SetImage(self.outsImg[self.colorMode].convert('RGB'), self.outsHeaderXOffset, self.strikesBallsYOffset)
        self.matrix.SetImage(self.clockSepImg[self.colorMode].convert('RGB'), self.clockSepXOffset, self.strikesBallsYOffset)
        self.drawScore()

    def drawScore(self):
        homeString = str(self.homeScore).zfill(2)
        awayString = str(self.awayScore).zfill(2)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(awayString[:1])].convert('RGB'), self.awayScoreLeadingDigitXOffset, self.scoreYOffset)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(awayString[1:])].convert('RGB'), self.awayScoreTrailingDigitXOffset, self.scoreYOffset)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(homeString[:1])].convert('RGB'), self.homeScoreLeadingDigitXOffset, self.scoreYOffset)
        self.matrix.SetImage(self.scoreImage[self.colorMode][int(homeString[1:])].convert('RGB'), self.homeScoreTrailingDigitXOffset, self.scoreYOffset)

    def drawClock(self):
        lastSecond = "00"
        while not self.killEvent.is_set():
            time.sleep(.05)
            if lastSecond != datetime.datetime.now().strftime("%S"):
                lastSecond = datetime.datetime.now().strftime("%S")
                self.redrawDisplay()
