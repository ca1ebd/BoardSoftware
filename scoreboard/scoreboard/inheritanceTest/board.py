#!/usr/bin/env python
import argparse
import time
import sys
import os
import rgbmatrix.core
import threading
import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

class Board:
    def init(self):
        self.killEvent = threading.Event()
        self.font = graphics.Font()
        self.headerFont = graphics.Font()
        self.scoreFont = graphics.Font()
        self.font.LoadFont("../../fonts/7x13B.bdf")
        self.headerFont.LoadFont("../../fonts/7x13B.bdf")
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
        self.scoreImage = [[], []]
        self.scoreImage[0] = []
        self.scoreImage[0].append(Image.open('../res/bb_0.png'))
        self.scoreImage[0].append(Image.open('../res/bb_1.png'))
        self.scoreImage[0].append(Image.open('../res/bb_2.png'))
        self.scoreImage[0].append(Image.open('../res/bb_3.png'))
        self.scoreImage[0].append(Image.open('../res/bb_4.png'))
        self.scoreImage[0].append(Image.open('../res/bb_5.png'))
        self.scoreImage[0].append(Image.open('../res/bb_6.png'))
        self.scoreImage[0].append(Image.open('../res/bb_7.png'))
        self.scoreImage[0].append(Image.open('../res/bb_8.png'))
        self.scoreImage[0].append(Image.open('../res/bb_9.png'))

        self.scoreImage[1].append(Image.open('../res/bb_0_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_1_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_2_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_3_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_4_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_5_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_6_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_7_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_8_w.png'))
        self.scoreImage[1].append(Image.open('../res/bb_9_w.png'))

        self.clockSepImg = []
        self.clockSepImg.append(Image.open('../res/clocksep.png'))
        self.clockSepImg.append(Image.open('../res/clocksep_w.png'))

        self.homeScore = 0
        self.awayScore = 0
        self.headerYOffset = 10
        self.homeHeaderXOffset = 2
        self.awayHeaderXOffset = 63
        self.clockHoursXOffset = 65
        self.clockImageYOffset = 38
        self.clockTextYOffset = self.clockImageYOffset + 9
        self.clockSepXOffset = 79
        self.clockMinutesXOffset = 82
        self.homeScoreLeadingDigitXOffset = 60
        self.homeScoreTrailingDigitXOffset = 77
        self.awayScoreLeadingDigitXOffset = 2
        self.awayScoreTrailingDigitXOffset = 19
        self.scoreYOffset = 12
        self.matrix = RGBMatrix(options=options)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.timer = threading.Timer(.25, self.drawClock)
        self.timer.start()
        self.redrawDisplay()

    def redrawDisplay(self):
        self.offscreen_canvas.Clear()
        if self.colorMode == 1:
            for x in range(0, self.matrix.width):
                for y in range(0, self.matrix.width):
                    self.offscreen_canvas.SetPixel(x, y, 255, 255, 255)
        else:
            graphics.DrawText(self.offscreen_canvas, self.headerFont, self.homeHeaderXOffset, self.headerYOffset, self.homeColor, self.homeName)
            graphics.DrawText(self.offscreen_canvas, self.headerFont, self.awayHeaderXOffset, self.headerYOffset, self.awayColor, self.awayName)
            graphics.DrawText(self.offscreen_canvas, self.scoreFont, self.homeHeaderXOffset, self.headerYOffset, graphics.Color(0, 255, 0), "00")
            graphics.DrawText(self.offscreen_canvas, self.font, self.clockHoursXOffset, self.clockTextYOffset, graphics.Color(0, 0, 255), datetime.datetime.now().strftime("%I"))
            graphics.DrawText(self.offscreen_canvas, self.font, self.clockMinutesXOffset, self.clockTextYOffset, graphics.Color(0, 0, 255), datetime.datetime.now().strftime("%M"))
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
            self.matrix.SetImage(self.clockSepImg[self.colorMode].convert('RGB'), self.clockSepXOffset, self.clockImageYOffset)
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

    def kill(self):
        self.killEvent.set()


if __name__ == "__main__":
    board = Board()
    board.init()