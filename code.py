import connect
import time
import weerlive_client
import buienradar_client
import displayio
import draw
import board

board.DISPLAY.auto_brightness=False

# connect.wifi()
wifi = connect.wifi_manager()
draw = draw.Draw()

weerlive_client = weerlive_client.WeerliveClient(wifi, draw)
buienradar_client = buienradar_client.BuienradarClient(wifi, draw)
wait=20

screens = [
    'weerlive_client.draw_current()',
    'weerlive_client.draw_forecasts()',
    'buienradar_client.draw()'
    ]

while True:
    for f in screens:
        eval(f)
        time.sleep(wait)
