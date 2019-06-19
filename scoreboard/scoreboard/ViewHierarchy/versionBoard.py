from rgbViews import *
import json


class VersionBoard:

    def __init__(self, rootView, defaults=None):
        self.__rootView__ = rootView


        # Views
        self.versionNum = 22
        self.versionLabel = RGBLabel(self.__rootView__, 9, 18, "VERSION: " + str(self.versionNum))
        self.versionLabel.setColor(graphics.Color(0, 255, 255))


if __name__ == "__main__":
    rootView = RGBBase()
    board = VersionBoard(rootView)
    while True:
        pass