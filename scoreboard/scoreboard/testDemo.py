import time
from baseballParam import BaseballBoard
from soccerParam import SoccerBoard
# from baseballParam import BaseballBoard
# from baseballParam import BaseballBoard

board = BaseballBoard()
time.sleep(5)
board.killEvent.set()

board = SoccerBoard()
time.sleep(5)
board.stoppedClock.set()

