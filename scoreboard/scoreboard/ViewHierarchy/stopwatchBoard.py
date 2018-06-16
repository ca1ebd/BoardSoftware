from rgbViews import *
import json

class splitView:
    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.splits = 0
        self.zeroString = "00:00"
        self.dataStr1 = ""
        self.dataStr2 = ""
        self.dataStr3 = ""


    def split(self, dataStr):
        self.dataStr3 = self.dataStr2
        self.dataStr2 = self.dataStr1
        self.dataStr1 = dataStr

        self.splits+=1

        if self.splits == 1:
            self.__split1__ = Clock(self.__rootView__, self.__x__, self.__y__)
        if self.splits == 2:
            self.__split2__ = Clock(self.__rootView__, self.__x__ + 32, self.__y__)
        if self.splits == 3:
            self.__split3__ = Clock(self.__rootView__, self.__x__ + 64, self.__y__)

        self.__split1__.setTime(self.dataStr1)
        self.__split2__.setTime(self.dataStr2)
        self.__split3__.setTime(self.dataStr3)


class StopwatchBoard:
    # TODO implement color scheme (splits are darker as they go down to help readability)

    def __init__(self, rootView):
        self.__rootView__ = rootView

        self.splitView = splitView(self.__rootView__, 1, 38)
        self.mainClock = Clock(self.__rootView__, 33, 10) # TODO make big clock

    def setClock(self, dataStr):
        self.mainClock.setTime(dataStr)

    def split(self, dataStr):
        self.splitView.split(dataStr)

