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
	mainMenuText = "Select Option\n\n1) Set Home Points\n2) Set Away Points\n3) Set Period\n4) Set Clock\n5) Start/Stop Clock\n"
	def init(self):
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

		self.clockSepImg = []
		self.clockSepImg.append(Image.open('res/clocksep.png'))
		self.clockSepImg.append(Image.open('res/clocksep_w.png'))

		self.periodColor = []
		self.periodColor.append(graphics.Color(255, 255, 255))
		self.periodColor.append(graphics.Color(50, 0, 50))

		self.periodHeaderColor = []
		self.periodHeaderColor.append(graphics.Color(255, 255, 0))
		self.periodHeaderColor.append(graphics.Color(100, 100, 0))

		self.firstClockStart = True
		self.gameClock = 2700000000
		self.homeScore = 0
		self.awayScore = 0
		self.period = 1
		self.headerYOffset = 10
		self.homeHeaderXOffset = 63
		self.periodHeaderOffset = 43
		self.periodNumberOffset = 51
		self.clockMinutesXOffset = 33
		self.clockSepXOffset = 47
		self.clockSecondsXOffset = 50
		self.clockYOffset = 38
		self.clockTextYOffset = self.clockYOffset + 9
		self.homeScoreLeadingDigitXOffset = 60
		self.homeScoreTrailingDigitXOffset = 77
		self.awayScoreLeadingDigitXOffset = 2
		self.awayScoreTrailingDigitXOffset = 19
		self.scoreYOffset = 12
		self.matrix = RGBMatrix(options = options)
		self.offscreen_canvas = self.matrix.CreateFrameCanvas()
		self.timer = threading.Timer(.05, self.drawClock)
		self.redrawDisplay()
		self.mainMenu()
				
	def mainMenu(self):
		while True:
#			os.system('clear')
			try:
				menuResp = input(self.mainMenuText)

				if menuResp == 1:
					self.setHomeScore()				
				if menuResp == 2:
					self.setAwayScore()
				if menuResp == 3:
					self.setPeriod()
				if menuResp == 4:
					self.setClock()
				if menuResp == 5:
					self.startStopClock()
			except SyntaxError:
				print "\nPlease enter a valid value\n"
			except KeyboardInterrupt:
				self.stoppedClock.set()
				sys.exit()


	def setColorMode(self):
		self.colorMode = self.colorMode ^ 1
		self.redrawDisplay()

	def startStopClock(self):
		if self.stoppedClock.is_set() or self.firstClockStart:
			self.stoppedClock.clear()
			self.timer = threading.Timer(.05, self.drawClock)
			self.timer.start()
		else:
			self.stoppedClock.set()

	def setClock(self):
		os.system('clear')
		clockStr = raw_input("\nSet clock (Format: MM:SS)\n")
		tm = time.strptime(clockStr, "%M:%S")
		print(clockStr)
		self.gameClock = (tm.tm_sec + (60 * tm.tm_min)) * 1000000
		print(self.gameClock)
		self.redrawDisplay()

	def setPeriod(self):
		os.system('clear')
		self.period = input("\nWhat period?\n")
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
		graphics.DrawText(self.offscreen_canvas, self.headerFont, 2, self.headerYOffset, graphics.Color(0, 0, 255), "GUEST")	
		graphics.DrawText(self.offscreen_canvas, self.headerFont, self.periodHeaderOffset, self.headerYOffset, self.periodHeaderColor[self.colorMode], "P")			
		graphics.DrawText(self.offscreen_canvas, self.headerFont, self.periodNumberOffset, self.headerYOffset, self.periodColor[self.colorMode], str(self.period))
		graphics.DrawText(self.offscreen_canvas, self.headerFont, self.homeHeaderXOffset, self.headerYOffset, graphics.Color(0, 0, 255), "HOME")
		graphics.DrawText(self.offscreen_canvas, self.scoreFont, self.homeHeaderXOffset, self.headerYOffset, graphics.Color(0, 255, 0), "00")
		graphics.DrawText(self.offscreen_canvas, self.font, self.clockMinutesXOffset, self.clockTextYOffset, graphics.Color(0, 0, 255),str(datetime.timedelta(microseconds=self.gameClock))[2:4])
		graphics.DrawText(self.offscreen_canvas, self.font, self.clockSecondsXOffset, self.clockTextYOffset, graphics.Color(0, 0, 255),str(datetime.timedelta(microseconds=self.gameClock))[5:7])

		self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

		self.matrix.SetImage(self.clockSepImg[self.colorMode].convert('RGB'), self.clockSepXOffset, self.clockYOffset)
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

			
			

if __name__ == "__main__":
	sb = ScoreBoard()
	sb.init()