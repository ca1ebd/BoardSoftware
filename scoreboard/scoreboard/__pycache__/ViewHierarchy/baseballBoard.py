from rgbViews import *
import json


class BSOIndicator:

    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y

        # Balls Text Image
        self.ballsImage = RGBImage(rootView, self.__x__, self.__y__+1, '../res/balls.png')
        self.ballsLabel = RGBLabel(rootView, self.__x__+10, self.__y__, '0')
        # Strikes Text Image
        self.strikesImage = RGBImage(rootView, self.__x__+19, self.__y__+1, '../res/strikes.png')
        self.strikesLabel = RGBLabel(rootView, self.__x__+29, self.__y__, '0')
        # Outs Text Image
        self.outsImage = RGBImage(rootView, self.__x__+38, self.__y__+1, '../res/outs.png')
        self.outsLabel = RGBLabel(rootView, self.__x__+48, self.__y__, '0')

    def setBalls(self, balls):
        self.ballsLabel.setText(balls)

    def setStrikes(self, strikes):
        self.strikesLabel.setText(strikes)

    def setOuts(self, outs):
        self.outsLabel.setText(outs)


class InningIndicator:

    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.arrowLabel = RGBLabel(self.__rootView__, self.__x__, self.__y__, u"\u2193")
        self.numLabel = RGBLabel(self.__rootView__, self.__x__+8, self.__y__, '1')

    def setInning(self, inning):
        self.numLabel.setText(inning[1:])
        if inning[:1] == 'b':
            self.arrowLabel.setText(u"\u2193")
        else:
            self.arrowLabel.setText(u"\u2191")


class BaseballBoard:

    def __init__(self, rootView):
        self.__rootView__ = rootView

        # Views
        self.homeLabel = RGBLabel(self.__rootView__, 0, 0, "HOME")
        self.homeScore = RGBLabel(self.__rootView__, 0, 12, "00", TextStyle.IMAGE)
        self.awayLabel = RGBLabel(self.__rootView__, 63, 0, "AWAY")
        self.awayScore = RGBLabel(self.__rootView__, 60, 12, "00", TextStyle.IMAGE)
        self.bsoIndicator = BSOIndicator(self.__rootView__, 0, 38)
        self.inningIndicator = InningIndicator(self.__rootView__, 43, 0)
        self.clockIndicator = Clock(self.__rootView__, 65, 38)

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

    def setBalls(self, dataStr):
        self.bsoIndicator.setBalls(dataStr)

    def setStrikes(self, dataStr):
        self.bsoIndicator.setStrikes(dataStr)

    def setOuts(self, dataStr):
        self.bsoIndicator.setOuts(dataStr)


if __name__ == "__main__":
    root = RGBBase()
    baseball = BaseballBoard(root)
    while True:
        pass

