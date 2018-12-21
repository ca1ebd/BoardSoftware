from rgbViews import *
import json
from rgbmatrix import graphics


class BSOIndicator:

    def __init__(self, rootView, x, y, defBalls='0', defStrikes='0', defOuts='0'):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.rootDir = '/home/pi/scoreboard/scoreboard/ViewHierarchy/'

        # Balls Text Image
        self.ballsImage = RGBImage(rootView, self.__x__, self.__y__+1, self.rootDir + '../res/balls.png')
        self.ballsLabel = RGBLabel(rootView, self.__x__+10, self.__y__, defBalls)
        # Strikes Text Image
        self.strikesImage = RGBImage(rootView, self.__x__+19, self.__y__+1, self.rootDir + '../res/strikes.png')
        self.strikesLabel = RGBLabel(rootView, self.__x__+29, self.__y__, defStrikes)
        # Outs Text Image
        self.outsImage = RGBImage(rootView, self.__x__+38, self.__y__+1, self.rootDir + '../res/outs.png')
        self.outsLabel = RGBLabel(rootView, self.__x__+48, self.__y__, defOuts)

    def setBalls(self, balls):
        self.ballsLabel.setText(balls)

    def setStrikes(self, strikes):
        self.strikesLabel.setText(strikes)

    def setOuts(self, outs):
        self.outsLabel.setText(outs)


class InningIndicator:

    def __init__(self, rootView, x, y, defInning="t1"):
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
        if self.isTop(defInning):
            self.arrowLabel = RGBImage(self.__rootView__, self.__x__ - 1, self.__y__ + 1, self.arrowUpImage)
        else:
            self.arrowLabel = RGBImage(self.__rootView__, self.__x__ - 1, self.__y__ + 1, self.arrowDownImage)
        self.numLabel = RGBLabel(self.__rootView__, self.__x__+8, self.__y__, defInning[1:])
        #self.arrowLabel.setColor(graphics.Color(255, 255, 0))
        #self.numLabel.setColor(graphics.Color(255, 255, 0))

    def setInning(self, inning):
        self.numLabel.setText(inning[1:])
        if not self.isTop(inning):
            #self.arrowLabel.setText(u"\u2193")
            self.arrowLabel.setImage(self.arrowDownImage)
        else:
            #self.arrowLabel.setText(u"\u2191")
            self.arrowLabel.setImage(self.arrowUpImage)

    def isTop(self, inning):
        return inning[:1]=='t'


class BaseballBoard:

    def __init__(self, rootView, defaults=None):
        self.__rootView__ = rootView

        print(defaults)

        if defaults==None:
            defaults = {
                "homeScore": "00",
                "awayScore": "00",
                "balls": "0",
                "strikes": "0",
                "outs": "0",
                "inning": "t1",
                "homeColor": {"R": 0, "G": 255, "B": 255},
                "awayColor": {"R": 0, "G": 255, "B": 255},
                "timeSeconds": "0"
            }


        # Views
        self.awayLabel = RGBLabel(self.__rootView__, 0, 0, "GUEST")
        self.awayScore = RGBLabel(self.__rootView__, 0, 12, str(defaults["awayScore"]), TextStyle.IMAGE)
        self.homeScore = RGBLabel(self.__rootView__, 60, 12, str(defaults["homeScore"]), TextStyle.IMAGE)
        self.homeLabel = RGBLabel(self.__rootView__, 63, 0, "HOME")
        defAway = defaults["awayColor"]
        defHome = defaults["homeColor"]
        self.awayLabel.setColor(graphics.Color(defAway["R"], defAway["G"], defAway["B"]))
        self.homeLabel.setColor(graphics.Color(defHome["R"], defHome["G"], defHome["B"]))
        self.bsoIndicator = BSOIndicator(self.__rootView__, 0, 38, defBalls=defaults['balls'], defStrikes=defaults['strikes'], defOuts=defaults['outs'])
        self.inningIndicator = InningIndicator(self.__rootView__, 43, 0, defInning=defaults["inning"])
        #self.inningIndicator.setInning('b3')
        self.clockIndicator = Clock(self.__rootView__, 65, 38, defSeconds=defaults["timeSeconds"])

        #set remaining defaults through functions
        #self.setClock(defaults["time"])
        # self.setBalls(str(defaults["balls"]))
        # self.setStrikes(str(defaults["strikes"]))
        # self.setOuts(str(defaults["outs"]))
        #self.setInning(defaults["inning"])

    def setHomeScore(self, dataStr):
        #TODO make app send correct data instead of fixing here
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

    def setBalls(self, dataStr):
        self.bsoIndicator.setBalls(dataStr)

    def setStrikes(self, dataStr):
        self.bsoIndicator.setStrikes(dataStr)

    def setOuts(self, dataStr):
        self.bsoIndicator.setOuts(dataStr)

    def setInning(self, dataStr):
        self.inningIndicator.setInning(dataStr)


if __name__ == "__main__":
    root = RGBBase()
    baseball = BaseballBoard(root)
    while True:
        pass

