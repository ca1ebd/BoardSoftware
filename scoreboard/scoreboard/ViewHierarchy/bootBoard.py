from PIL import Image
from rgbViews import *

class BootBoard:
    def __init__(self, rootView):
        self.__rootView__ = rootView
        self.logo = Image.open('../res/lederbord_logo.png')
        self.logo = self.logo.convert("RGB")
        self.boardWidth = 96
        wpercent = (self.boardWidth / float(self.logo.size[0]))
        hsize = int((float(self.logo.size[1]) * float(wpercent)))
        self.logo = self.logo.resize((self.boardWidth, hsize))
        self.bootImage = RGBImage(self.__rootView__, 0, 0, self.logo)
        print("ran")

if __name__ == "__main__":
    root = RGBBase()
    boot = BootBoard(root)
    while True:
        pass
