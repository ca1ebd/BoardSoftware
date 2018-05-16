import time
from rgbViews import *

base = RGBBase()

# font = graphics.Font()
# font.LoadFont("../../fonts/7x13B.bdf")
# color = graphics.Color(255, 255, 255)
#
# graphics.DrawText(base.__offscreen_canvas__, font, 15, 15, color, 'TMY = BTCH')
# graphics.DrawText(base.__offscreen_canvas__, font, 15, 32, color, 'TMY = BTCH')
# base.__offscreen_canvas__ = base.__matrix__.SwapOnVSync(base.__offscreen_canvas__)

label = RGBLabel(base, 0, 0, "Python != <3", TextStyle.FONT)
base.addView(label)
base.redraw()

y = 0

while True:
    y += 1
    if y > 48:
        y = 0
    #label.setOrigin(0, y)
    time.sleep(0.5)
    pass
