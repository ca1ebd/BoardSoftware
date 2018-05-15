#!/usr/bin/env python
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

matrix = RGBMatrix(options = options)

offset_canvas = matrix.CreateFrameCanvas()

while True:
    offset_canvas.SetPixel(1, 1, 255, 255, 255)
