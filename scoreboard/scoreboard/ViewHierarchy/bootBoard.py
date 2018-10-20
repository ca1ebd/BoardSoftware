from PIL import Image
from rgbViews import *
from rgbmatrix import graphics
from BoardInfo import GetWifiInfo, GetWifiConnectionInfo

class BootBoard:
    def __init__(self, rootView):
        self.rootDir = '/home/pi/scoreboard/scoreboard/ViewHierarchy/'
        self.__rootView__ = rootView
        self.logo = Image.open(self.rootDir + '../res/lederbord_logo_small.png')
        self.logo = self.logo.convert("RGB")
        # self.boardWidth = 96
        # wpercent = (self.boardWidth / float(self.logo.size[0]))
        # hsize = int((float(self.logo.size[1]) * float(wpercent)))
        # self.logo = self.logo.resize((self.boardWidth, hsize))
        self.bootImage = RGBImage(self.__rootView__,3, 5, self.logo)
        self.connectInfo = ConnectInfo(rootView, 0, 23)
        print("ran")

class ConnectInfo:
    def __init__(self, rootView, x, y):
        self.__rootView__ = rootView
        self.__x__ = x
        self.__y__ = y
        self.ssid = ''
        self.password = ''

        # data = GetWifiInfo()
        # for i in range(0, len(data)):
        #     if data[i][0] == 'ssid':
        #         self.ssid = data[i][1]
        #     elif data[i][0] == 'wpa_passphrase':
        #         self.password = data[i][1]

        (self.ssid, self.password) = GetWifiConnectionInfo()


        self.ssid_label = RGBLabel(self.__rootView__, self.__x__, self.__y__, self.ssid)
        self.ssid_label.setColor(graphics.Color(0, 255, 0))
        self.password_label = RGBLabel(self.__rootView__, self.__x__, self.__y__ + 10, self.password)
        self.password_label.setColor(graphics.Color(0, 255, 255))

    # def getData(self):
    #     data = []
    #     dataFile = open("/etc/hostapd/hostapd.conf", "r")
    #     for line in dataFile:
    #         split = line.rstrip().split('=')
    #         data.append(split)
    #
    #     #print(data)
    #
    #     return data




if __name__ == "__main__":
    root = RGBBase()
    boot = BootBoard(root)
    while True:
        pass
