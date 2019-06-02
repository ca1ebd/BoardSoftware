from rgbViews import *
import json
from rgbmatrix import graphics



class UltimateBoard:

    def __init__(self, rootView, defaults=None):
        self.__rootView__ = rootView

        if defaults==None:
            #set default values here
            defaults = {
                "homeScore": "16",
                "awayScore": "12",
                "homeColor": {"R": 0, "G": 255, "B": 255},
                "awayColor": {"R": 0, "G": 255, "B": 255},
                "timeSeconds": "856"
            }

        # Views
        self.homeLabel = RGBLabel(self.__rootView__, 63, 0, "HOME")
        self.homeScore = RGBLabel(self.__rootView__, 60, 12, defaults["homeScore"], TextStyle.IMAGE)
        self.awayLabel = RGBLabel(self.__rootView__, 5, 0, "GUEST")
        self.awayScore = RGBLabel(self.__rootView__, 0, 12, defaults["awayScore"], TextStyle.IMAGE)
        defAway = defaults["awayColor"]
        defHome = defaults["homeColor"]
        self.awayLabel.setColor(graphics.Color(defAway["R"], defAway["G"], defAway["B"]))
        self.homeLabel.setColor(graphics.Color(defHome["R"], defHome["G"], defHome["B"]))
        self.clockIndicator = Clock(self.__rootView__, 33, 38, defSeconds=defaults['timeSeconds'])

    def setHomeScore(self, dataStr):
        # TODO make app send correct data instead of fixing here
        if len(dataStr) == 1:
            self.homeScore.setText("0" + dataStr)
        else:
            self.homeScore.setText(dataStr)

    def setHomeColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.homeLabel.setColor(graphics.Color(red, green, blue))

    def setAwayScore(self, dataStr):
        # TODO make app send correct data instead of fixing here
        if len(dataStr) == 1:
            self.awayScore.setText("0" + dataStr)
        else:
            self.awayScore.setText(dataStr)

    def setAwayColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.awayLabel.setColor(graphics.Color(red, green, blue))

    def setClock(self, dataStr):
        self.clockIndicator.setTime(dataStr)

if __name__ == "__main__":
    rootView = RGBBase()
    board = UltimateBoard(rootView)
    while True:
        pass

