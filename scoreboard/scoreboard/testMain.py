#!/usr/bin/env python

import sys

from baseballParam import BaseballBoard
#from baseball import ScoreBoard

# oldBoard = ScoreBoard()
# oldBoard.init()

board = BaseballBoard()


board.setHomeScore("5")
board.setAwayScore("7")

board.setInning("3b")
board.setBalls("4")
board.setOuts("2")
board.setStrikes("3")

json = '{"R":255, "G":0, "B":0}'
board.setHomeColor(json)

json = '{"R":128, "G":0, "B":128}'
board.setAwayColor(json)

board.setHomeName("Caleb")
board.setAwayName("David")


while(True):
    try:
        continue
    except KeyboardInterrupt:
        board.killEvent.set()
        break
