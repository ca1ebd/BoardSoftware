from rgbViews import *
import json
from rgbmatrix import graphics


class BSOIndicator:

    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.rootDir = '/home/pi/scoreboard/scoreboard/ViewHierarchy/'

        # Balls Text Image
        self.ballsImage = RGBImage(rootView, self.__x__, self.__y__+1, self.rootDir + '../res/balls.png')
        self.ballsLabel = RGBLabel(rootView, self.__x__+10, self.__y__, '0')
        # Strikes Text Image
        self.strikesImage = RGBImage(rootView, self.__x__+19, self.__y__+1, self.rootDir + '../res/strikes.png')
        self.strikesLabel = RGBLabel(rootView, self.__x__+29, self.__y__, '0')
        # Outs Text Image
        self.outsImage = RGBImage(rootView, self.__x__+38, self.__y__+1, self.rootDir + '../res/outs.png')
        self.outsLabel = RGBLabel(rootView, self.__x__+48, self.__y__, '0')

    def setBalls(self, balls):
        balls = str(balls)
        self.ballsLabel.setText(balls)

    def setStrikes(self, strikes):
        strikes = str(strikes)
        self.strikesLabel.setText(strikes)

    def setOuts(self, outs):
        outs = str(outs)
        self.outsLabel.setText(outs)


class InningIndicator:

    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.rootDir = '/home/pi/scoreboard/scoreboard/ViewHierarchy/'
        self.arrowUpImage = Image.open(self.rootDir + '../res/arrow_up.png')
        self.arrowUpImage = self.arrowUpImage.convert('RGB')
        self.arrowDownImage = Image.open(self.rootDir + '../res/arrow_down.png')
        self.arrowDownImage = self.arrowDownImage.convert('RGB')
        # self.arrowLabel = RGBLabel(self.__rootView__, self.__x__, self.__y__, u"\u2193")
        #self.arrowLabel = RGBLabel(self.__rootView__, self.__x__, self.__y__, u"\u2038")
        self.arrowLabel = RGBImage(self.__rootView__, self.__x__ - 1, self.__y__ + 1, self.arrowUpImage)
        self.numLabel = RGBLabel(self.__rootView__, self.__x__+8, self.__y__, '1')
        #self.arrowLabel.setColor(graphics.Color(255, 255, 0))
        #self.numLabel.setColor(graphics.Color(255, 255, 0))

    def setInning(self, inning):
        self.numLabel.setText(inning[1:])
        if inning[:1] == 'b':
            #self.arrowLabel.setText(u"\u2193")
            self.arrowLabel.setImage(self.arrowDownImage)
        else:
            #self.arrowLabel.setText(u"\u2191")
            self.arrowLabel.setImage(self.arrowUpImage)


class BaseballBoard:

    def __init__(self, rootView):
        self.__rootView__ = rootView

        # Views
        self.awayLabel = RGBLabel(self.__rootView__, 0, 0, "GUEST")
        self.awayScore = RGBLabel(self.__rootView__, 0, 12, "00", TextStyle.IMAGE)
        self.homeScore = RGBLabel(self.__rootView__, 60, 12, "00", TextStyle.IMAGE)
        self.homeLabel = RGBLabel(self.__rootView__, 63, 0, "HOME")
        self.awayLabel.setColor(graphics.Color(0, 255, 255))
        self.homeLabel.setColor(graphics.Color(0, 255, 255))
        self.bsoIndicator = BSOIndicator(self.__rootView__, 0, 38)
        self.inningIndicator = InningIndicator(self.__rootView__, 43, 0)
        #self.inningIndicator.setInning('b3')
        self.clockIndicator = Clock(self.__rootView__, 65, 38)

    def setHomeScore(self, score):
        #TODO make app send correct data instead of fixing here
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

    def setBalls(self, balls):
        self.bsoIndicator.setBalls(balls)

    def setStrikes(self, strikes):
        self.bsoIndicator.setStrikes(strikes)

    def setOuts(self, outs):
        self.bsoIndicator.setOuts(outs)

    def setInning(self, inning):
        self.inningIndicator.setInning(inning)


if __name__ == "__main__":
    root = RGBBase()
    baseball = BaseballBoard(root)
    while True:
        pass

