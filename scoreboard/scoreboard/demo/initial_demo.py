import sys
sys.path.append("../ViewHierarchy")

from rgbViews import *
from baseballBoard import BaseballBoard
from soccerBoard import SoccerBoard
from lacrosseBoard import LacrosseBoard
from footballBoard import FootballBoard
from stopwatchBoard import StopwatchBoard
from bootBoard import BootBoard
from FlaskRPC import FlaskRPC


class InitialDemo:

    def __init__(self):


        myFlask = FlaskRPC()
        #myFlask.start()
        myFlask.start()
        myFlask.createBaseball()
        # self.rootView = None
        # self.board = None
        #
        #
        # #create the baseball board
        # if self.rootView == None:
        #     self.start()
        # self.clear()
        # self.board = BaseballBoard(self.rootView)


    # def clear(self, dataStr=None):
    #     self.rootView.removeAllViews()
    #
    # def start(self, dataStr=None):
    #     if self.rootView is None:
    #         self.rootView = RGBBase()
    #     else:
    #         self.rootView.removeAllViews()
    #     return 'Success'


if __name__ == '__main__':
    demo = InitialDemo()


