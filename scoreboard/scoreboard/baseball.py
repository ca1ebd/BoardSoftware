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

class ScoreBoard:
	mainMenuText = "Select Option\n\n1) Set Strikes, Balls, and Outs\n2) Set Home Points\n3) Set Away Points\n4) Set Inning\n"
	def init(self):
		self.killEvent = threading.Event()
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
		self.matrix = RGBMatrix(options = options)
		self.offscreen_canvas = self.matrix.CreateFrameCanvas()
		self.timer = threading.Timer(.25, self.drawClock)
		self.timer.start()
		self.redrawDisplay()
		self.mainMenu()

	def mainMenu(self):
		while True:
#			os.system('clear')
			try:
				menuResp = input(self.mainMenuText)
				if menuResp == 1:
					self.setStrikesBallsAndOuts()
				if menuResp == 2:
					self.setHomeScore()
				if menuResp == 3:
					self.setAwayScore()
				if menuResp == 4:
					self.setInning()
			except SyntaxError:
				print "\nPlease enter a valid value\n"
			except KeyboardInterrupt:
				self.killEvent.set()
				sys.exit()


	def setColorMode(self):
		self.colorMode = self.colorMode ^ 1
		self.redrawDisplay()

	def setStrikesBallsAndOuts(self):
		os.system('clear')
		self.strikes = input("\nHow many strikes?\n")
		self.balls = input("\nHow many balls?\n")
		self.outs = input("\nHow many outs?\n")
		self.redrawDisplay()

	def setInning(self):
		os.system('clear')
		self.inning = input("\nWhat inning?\n")
		self.inningHalf = raw_input("\nt for Top, b for Bottom\n")
		self.redrawDisplay()

	def setAwayScore(self):
		self.awayScore = input("\nHow many points for away team?\n")
		self.redrawDisplay()

	def setHomeScore(self):
		self.homeScore = input("\nHow many points for home team?\n")
		self.redrawDisplay()

	def redrawDisplay(self):
		self.offscreen_canvas.Clear()
		if self.colorMode == 1:
			for x in range(0, self.matrix.width):
				for y in range(0, self.matrix.width):
							self.offscreen_canvas.SetPixel(x, y, 255, 255, 255)
		graphics.DrawText(self.offscreen_canvas, self.headerFont, 2, self.headerYOffset, graphics.Color(252,76,2), "BRONCOS")
		if self.inningHalf == "b":
			graphics.DrawText(self.offscreen_canvas, self.headerFont, self.inningArrowOffset, self.headerYOffset, self.inningArrowColor[self.colorMode], u"\u2193")
		else:
			graphics.DrawText(self.offscreen_canvas, self.headerFont, self.inningArrowOffset, self.headerYOffset, self.inningArrowColor[self.colorMode], u"\u2191")
		graphics.DrawText(self.offscreen_canvas, self.headerFont, self.inningNumberOffset, self.headerYOffset, self.inningColor[self.colorMode], str(self.inning))
		graphics.DrawText(self.offscreen_canvas, self.headerFont, self.homeHeaderXOffset, self.headerYOffset, graphics.Color(0, 0, 255), "HOME")
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
		# for i in range(0, 96):
		# 	for j in range(0, 48):
		# 		self.matrix.SetPixel(i, j, 255, 255, 255)

	def drawClock(self):
		lastSecond = "00"
		while not self.killEvent.is_set():
			time.sleep(.05)
			if lastSecond != datetime.datetime.now().strftime("%S"):
				lastSecond = datetime.datetime.now().strftime("%S")
				self.redrawDisplay()


#			print datetime.datetime.now().strftime("%M:%S")


if __name__ == "__main__":
	sb = ScoreBoard()
	sb.init()
