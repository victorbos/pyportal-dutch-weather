import connect
import time

from weerlive_client import WeerliveClient
from buienradar_client import BuienradarClient
from time_client import TimeClient
from suntimes_client import SuntimesClient
from astronomy import Astronomy

import displayio
import draw
import board

board.DISPLAY.auto_brightness=False

# connect.wifi()
wifi = connect.wifi_manager()
draw = draw.Draw()

weerlive_client = WeerliveClient(wifi, draw)
buienradar_client = BuienradarClient(wifi, draw)
time_client = TimeClient(wifi)
suntimes_client = SuntimesClient(wifi)
astronomy = Astronomy(draw, suntimes_client, time_client)

wait=20

screens = [
    'astronomy.draw(wait)',
    'weerlive_client.draw_current(wait)',
    'weerlive_client.draw_forecasts(wait)',
    'buienradar_client.draw(wait)'
    ]

while True:
    for f in screens:
        eval(f)

