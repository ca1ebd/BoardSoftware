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

    def setClock(self, time):
        self.clockIndicator.setTime(time)

    def setHalf(self, half):
        half = str(half)
        self.halfIndicator.setText("H" + half)


if __name__ == "__main__":
    rootView = RGBBase()
    board = SoccerBoard(rootView)
    while True:
        pass