import argparse
import time
import sys
import os
import rgbmatrix.core
import threading
import datetime
from enum import Enum

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image


class RGBView(object):

    def __init__(self, parent, x , y):
        self.__parent__ = parent
        self.__x__ = x
        self.__y__ = y

        self.width = 96
        self.height = 32

    def setOrigin(self, x, y):
        self.__x__ = x
        self.__y__ = y
        self.__parent__.redraw()

    def render(self, matrix, canvas):
        pass


class RGBImage(RGBView):

    def __init__(self, parent, x, y, image):
        super(RGBImage, self).__init__(parent, x, y)
        if type(image) == str:
            self.image = Image.open(image).convert('RGB')
        else:
            self.image = image
        self.__parent__.addView(self)
        self.__parent__.redraw()

    def render(self, matrix, canvas):
        matrix.SetImage(self.image, self.__x__, self.__y__)


class TextStyle(Enum):
    FONT = 0
    IMAGE = 1


class RGBLabel(RGBView):

    # X, Y is at BOTTOM LEFT for draw!!!
    def __init__(self, parent, x, y, text="", textStyle=TextStyle.FONT):
        # type: (RGBBase, int, int, str, TextStyle) -> None
        self.__text__ = text
        self.__textStyle__ = textStyle
        self.__color__ = graphics.Color(255, 255, 255)

        if self.__textStyle__ == TextStyle.FONT:
            super(RGBLabel, self).__init__(parent, x, (y + 10))
            self.__font__ = graphics.Font()
            self.__font__.LoadFont("../../fonts/7x13B.bdf")
        else:
            super(RGBLabel, self).__init__(parent, x, y)
            self.__font__ = []
            self.__font__.append(Image.open('../res/bb_0.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_1.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_2.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_3.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_4.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_5.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_6.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_7.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_8.png').convert('RGB'))
            self.__font__.append(Image.open('../res/bb_9.png').convert('RGB'))
        self.__parent__.addView(self)
        self.__parent__.redraw()

    # Fix the bottom left glitch
    def setOrigin(self, x, y):
        if self.__textStyle__ == TextStyle.FONT:
            self.__x__ = x
            self.__y__ = (y + 10)
        else:
            self.__x__ = x
            self.__y__ = y
        self.__parent__.redraw()

    def setText(self, text):
        self.__text__ = text
        self.__parent__.redraw()

    def setColor(self, color):
        self.__color__ = color
        self.__parent__ .redraw()

    def render(self, matrix, canvas):
        if self.__textStyle__ == TextStyle.FONT:
            graphics.DrawText(self.__parent__.__offscreen_canvas__, self.__font__, self.__x__, self.__y__, self.__color__, self.__text__)
        else:
            w = 17
            for index, char in enumerate(self.__text__):
                i = ord(char) - ord('0')
                matrix.SetImage(self.__font__[i], self.__x__ + (w*index), self.__y__)


class RGBBase:

    def __init__(self):
        # RGB Matrix Configuration
        self.__options__ = RGBMatrixOptions()
        self.__options__.rows = 16
        self.__options__.cols = 32
        self.__options__.chain_length = 3
        self.__options__.parallel = 3
        self.__options__.multiplexing = 3
        self.__options__.row_address_type = 2
        self.__options__.brightness = 100

        # Create the matrix stuff
        self.__matrix__ = RGBMatrix(options=self.__options__)
        self.__offscreen_canvas__ = self.__matrix__.CreateFrameCanvas()
        self.__offscreen_canvas__.Clear()

        # Create arrays to hold the child views
        self.__children__ = []

    def redraw(self):
        self.__offscreen_canvas__.Clear()

        for child in self.__children__:
            child.render(self.__matrix__, self.__offscreen_canvas__)
        self.__offscreen_canvas__ = self.__matrix__.SwapOnVSync(self.__offscreen_canvas__)

        for child in self.__children__:
            if type(child) != RGBLabel:
                child.render(self.__matrix__, self.__offscreen_canvas__)
            elif child.__textStyle__ == TextStyle.IMAGE:
                child.render(self.__matrix__, self.__offscreen_canvas__)

    def addView(self, view):
        self.__children__.append(view)
        self.redraw()

    def removeAllViews(self):
        self.__offscreen_canvas__.Clear()
        self.__children__ = []
        self.redraw()
        print('Removed All View')

    def setBrightness(self, dataStr):
        self.__matrix__.brightness = int(dataStr)
        self.redraw()



class PeriodIndicator:

    def __init__(self, rootView, x, y, letter='P'):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.letter = letter
        self.letterLabel = RGBLabel(self.__rootView__, self.__x__, self.__y__, self.letter)
        self.numLabel = RGBLabel(self.__rootView__, self.__x__+7, self.__y__, '1')

    def setPeriod(self, period):
        self.numLabel.setText(period)


class Clock:

    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.minLabel = RGBLabel(self.__rootView__, self.__x__, self.__y__, '00')
        self.minLabel.setColor(graphics.Color(0, 0, 255))
        self.seperatorImage = RGBImage(self.__rootView__, self.__x__+14, self.__y__+1, '../res/clocksep.png')
        self.secLabel = RGBLabel(self.__rootView__, self.__x__+17, self.__y__, '00')
        self.secLabel.setColor(graphics.Color(0, 0, 255))

    def setTime(self, timeStr):
        comps = timeStr.split(':')
        self.minLabel.setText(comps[0])
        self.secLabel.setText(comps[1])
        pass

