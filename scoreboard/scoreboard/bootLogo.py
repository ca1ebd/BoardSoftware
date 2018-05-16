import argparse
import time
import sys
import os
import rgbmatrix.core
import threading
import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image


options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 3
options.parallel = 3
options.multiplexing = 3
options.row_address_type = 2
options.brightness = 100


matrix = RGBMatrix(options=options)

offscreen_canvas = matrix.CreateFrameCanvas()

logo = Image.open('res/lederbord_logo.png')
logo = logo.convert('RGB')

basewidth = 96
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize))

offscreen_canvas.Clear()

matrix.SetImage(logo, 0, 0)
x=0
y=0

x2 = -96

while True:

    #matrix.SetPixel(0, 0, 255, 255, 255)
    matrix.SetImage(logo, x, y)
    matrix.SetImage(logo, x2, y)
    x+=1
    x2+=1
    if(x>96):
        x=-96

    if (x2 > 96):
        x2 = -96

    time.sleep(.1)
