from rgbViews import *

class FakeBoard:

    def __init__(self, rootView):
        self.__rootView__ = rootView
        self.label1 = RGBLabel(self.__rootView__, 0, 0, "BEFORE UPDATE")
        self.label2 = RGBLabel(self.__rootView__, 0, 13, "USE UPDATE TO")
        self.label3 = RGBLabel(self.__rootView__, 0, 26, "REPLACE ME")