from rgbViews import *
import json
from rgbmatrix import graphics



class WrestlingBoard:

    def __init__(self, rootView, defaults=None):
        self.__rootView__ = rootView

        if defaults==None:
            #set default values here
            defaults = {
                "homeScore": "00",
                "awayScore": "00",
                "awayColor": {"R": 255, "G": 0, "B": 0},
                "homeColor": {"R": 0, "G": 255, "B": 0},
                "timeSeconds": "120",
                "weightClass": "000",
                "period": "1"
            }

        # Views
        self.awayLabel = RGBLabel(self.__rootView__, 63, 0, "AWAY")
        self.awayScore = RGBLabel(self.__rootView__, 60, 12, defaults["awayScore"], TextStyle.IMAGE)
        self.homeLabel = RGBLabel(self.__rootView__, 5, 0, "HOME")
        self.homeScore = RGBLabel(self.__rootView__, 0, 12, defaults["homeScore"], TextStyle.IMAGE)
        self.weightClass = RGBLabel(self.__rootView__, 0, 36, "WT " + defaults["weightClass"])
        defAway = defaults["awayColor"]
        defHome = defaults["homeColor"]
        self.awayLabel.setColor(graphics.Color(defAway["R"], defAway["G"], defAway["B"]))
        self.homeLabel.setColor(graphics.Color(defHome["R"], defHome["G"], defHome["B"]))
        self.clockIndicator = Clock(self.__rootView__, 62, 38, defSeconds=defaults['timeSeconds'])
        self.periodIndicator = PeriodIndicator(self.__rootView__, 42, 0, 'P', defPeriod= defaults["period"])

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

    def setWeightClass(self, dataStr):
        self.weightClass.setText("WT " + dataStr)

    def setPeriod(self, dataStr):
        self.periodIndicator.setPeriod(dataStr)

if __name__ == "__main__":
    rootView = RGBBase()
    board = WrestlingBoard(rootView)
    while True:
        pass