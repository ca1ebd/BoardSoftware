from rgbViews import *
import json
from rgbmatrix import graphics



class SwimmingBoard:

    def __init__(self, rootView, defaults=None):
        self.__rootView__ = rootView

        if defaults==None:
            #set default values here
            defaults = {
                "homeScore": "11",
                "awayScore": "08",
                "eventColor": {"R": 0, "G": 255, "B": 255},
                "heatColor": {"R": 0, "G": 255, "B": 255},
            }

        # Views
        self.eventLabel = RGBLabel(self.__rootView__, 0, 0, "EVENT")
        self.eventScore = RGBLabel(self.__rootView__, 0, 12, defaults["awayScore"], TextStyle.IMAGE)
        self.heatLabel = RGBLabel(self.__rootView__, 63, 0, "HEAT")
        self.heatScore = RGBLabel(self.__rootView__, 60, 12, defaults["homeScore"], TextStyle.IMAGE)
        defEvent = defaults["eventColor"]
        defHeat = defaults["heatColor"]
        self.eventLabel.setColor(graphics.Color(defEvent["R"], defEvent["G"], defEvent["B"]))
        self.heatLabel.setColor(graphics.Color(defHeat["R"], defHeat["G"], defHeat["B"]))

    def setEventScore(self, dataStr):
        # TODO make app send correct data instead of fixing here
        if len(dataStr) == 1:
            self.eventScore.setText("0" + dataStr)
        else:
            self.eventScore.setText(dataStr)

    def setEventColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.eventLabel.setColor(graphics.Color(red, green, blue))

    def setHeatScore(self, dataStr):
        # TODO make app send correct data instead of fixing here
        if len(dataStr) == 1:
            self.heatScore.setText("0" + dataStr)
        else:
            self.heatScore.setText(dataStr)

    def setHeatColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.heatLabel.setColor(graphics.Color(red, green, blue))


if __name__ == "__main__":
    rootView = RGBBase()
    board = SoccerBoard(rootView)
    while True:
        pass

