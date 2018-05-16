from board import Board
import sys
import time

board = Board()
def run():
    board.init()

try:
    run()
except KeyboardInterrupt:
    board.kill()
    sys.exit(0)

# while True:
#     try:
#         time.sleep(1)
#     except KeyboardInterrupt:
#         board.kill()
#         sys.exit(0)

