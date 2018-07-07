from rgbViews import *
import json


class SoccerBoard:

    def __init__(self, rootView):
        self.__rootView__ = rootView

        # Views
        self.homeLabel = RGBLabel(self.__rootView__, 0, 0, "HOME")
        self.homeScore = RGBLabel(self.__rootView__, 0, 12, "00", TextStyle.IMAGE)
        self.awayLabel = RGBLabel(self.__rootView__, 63, 0, "AWAY")
        self.awayScore = RGBLabel(self.__rootView__, 60, 12, "00", TextStyle.IMAGE)
        self.clockIndicator = Clock(self.__rootView__, 33, 38)
        self.halfIndicator = RGBLabel(self.__rootView__, 43, 0, 'H1')

    def setHomeScore(self, dataStr):
        self.homeScore.setText(dataStr)

    def setHomeColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.homeLabel.setColor(graphics.Color(red, green, blue))

    def setAwayScore(self, dataStr):
        self.awayScore.setText(dataStr)

    def setAwayColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.awayLabel.setColor(graphics.Color(red, green, blue))

    def setClock(self, dataStr):
        self.clockIndicator.setTime(dataStr)

    def setHalf(self, dataStr):
        self.halfIndicator.setText(dataStr)


if __name__ == "__main__":
    rootView = RGBBase()
    board = SoccerBoard(rootView)
    while True:
        pass