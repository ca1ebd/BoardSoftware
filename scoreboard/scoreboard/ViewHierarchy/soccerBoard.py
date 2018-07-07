from rgbViews import *
import json


class SoccerBoard:

    def __init__(self, rootView):
        self.__rootView__ = rootView

        # Views
        self.awayLabel = RGBLabel(self.__rootView__, 0, 0, "GUEST")
        self.awayScore = RGBLabel(self.__rootView__, 0, 12, "00", TextStyle.IMAGE)
        self.homeLabel = RGBLabel(self.__rootView__, 63, 0, "HOME")
        self.homeScore = RGBLabel(self.__rootView__, 60, 12, "00", TextStyle.IMAGE)
        self.awayLabel.setColor(graphics.Color(0, 255, 255))
        self.homeLabel.setColor(graphics.Color(0, 255, 255))
        self.clockIndicator = Clock(self.__rootView__, 33, 38)
        self.halfIndicator = RGBLabel(self.__rootView__, 43, 0, 'H1')
        self.halfIndicator.setColor(graphics.Color(255, 255, 0))

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

    def setHalf(self, dataStr):
        self.halfIndicator.setText(dataStr)


if __name__ == "__main__":
    rootView = RGBBase()
    board = SoccerBoard(rootView)
    while True:
        pass