from rgbViews import *
import json


class LacrosseBoard:

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
        self.periodIndicator = PeriodIndicator(self.__rootView__, 43, 0, 'Q')

    def setHomeScore(self, score):
        score = str(score)
        # TODO make app send correct data instead of fixing here
        if len(score) == 1:
            self.homeScore.setText("0" + score)
        else:
            self.homeScore.setText(score)

    def setHomeColor(self, r, g, b):
        self.homeLabel.setColor(graphics.Color(r, g, b))

    def setAwayScore(self, score):
        score = str(score)
        # TODO make app send correct data instead of fixing here
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

if __name__ == "__main__":
    rootView = RGBBase()
    board = LacrosseBoard(rootView)
    while True:
        pass