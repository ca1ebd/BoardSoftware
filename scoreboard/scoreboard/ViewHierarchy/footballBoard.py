from rgbViews import *
import json


class DYIndicator:

    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.rootDir = '/home/pi/scoreboard/scoreboard/ViewHierarchy/'

        # Downs Text Image
        self.downsImage = RGBImage(rootView, self.__x__, self.__y__ + 1, self.rootDir + '../res/down.png')
        self.downsLabel = RGBLabel(rootView, self.__x__ + 10, self.__y__, '0')
        # Yards Text Image
        self.yardsImage = RGBImage(rootView, self.__x__ + 19, self.__y__ + 1, self.rootDir + '../res/yards.png')
        self.yardsLabel = RGBLabel(rootView, self.__x__ + 29, self.__y__, '0')



class FootballBoard:

    def __init__(self, rootView):
        self.__rootView__ = rootView

        # Views
        self.awayLabel = RGBLabel(self.__rootView__, 0, 0, "GUEST")
        self.awayScore = RGBLabel(self.__rootView__, 0, 12, "00", TextStyle.IMAGE)
        self.homeLabel = RGBLabel(self.__rootView__, 63, 0, "HOME")
        self.homeScore = RGBLabel(self.__rootView__, 60, 12, "00", TextStyle.IMAGE)
        self.awayLabel.setColor(graphics.Color(0, 255, 255))
        self.homeLabel.setColor(graphics.Color(0, 255, 255))
        self.bsoIndicator = DYIndicator(self.__rootView__, 0, 38)
        self.periodIndicator = PeriodIndicator(self.__rootView__, 43, 0, 'P')
        self.clockIndicator = Clock(self.__rootView__, 65, 38)

    def setHomeScore(self, score):
        # TODO make app send correct data instead of fixing here
        score = str(score)
        if len(score) == 1:
            self.homeScore.setText("0" + score)
        else:
            self.homeScore.setText(score)

    def setHomeColor(self, r, g, b):
        self.homeLabel.setColor(graphics.Color(r, g, b))

    def setAwayScore(self, score):
        # TODO make app send correct data instead of fixing here
        score = str(score)
        if len(score) == 1:
            self.awayScore.setText("0" + score)
        else:
            self.awayScore.setText(score)

    def setAwayColor(self, r, g, b):
        self.awayLabel.setColor(graphics.Color(r, g, b))

    def setClock(self, dataStr):
        self.clockIndicator.setTime(dataStr)

    def setQuarter(self, quarter):
        quarter = str(quarter)
        self.periodIndicator.setPeriod(quarter)

    def setYards(self, yards):
        yards = str(yards)
        self.bsoIndicator.yardsLabel.setText(yards)

    def setDown(self, down):
        down = str(down)
        self.bsoIndicator.downsLabel.setText(down)


if __name__ == "__main__":
    rootView = RGBBase()
    board = FootballBoard(rootView)
    while True:
        pass