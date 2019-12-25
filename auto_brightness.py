import board
import time
from analogio import AnalogIn

class AutoBrightness:
    def __init__(self):
        self.__light_sensor=AnalogIn(board.LIGHT)
        board.DISPLAY.auto_brightness=False
        self.__dim_seconds = 1
    
    def set(self):
        to_value = self.__sensor_to_brightness()
        steps = 10
        for i in range(1, steps):
            board.DISPLAY.brightness=(i * to_value) / steps
            time.sleep(self.__dim_seconds / steps)
        board.DISPLAY.brightness = to_value

    def dim(self):
        from_value = self.__sensor_to_brightness()
        steps = 10
        for i in range(1, steps):
            board.DISPLAY.brightness=from_value - (i * (from_value / steps))
            time.sleep(self.__dim_seconds / steps)
        board.DISPLAY.brightness = 0

    def __sensor_to_brightness(self):
        return self.__light_sensor.value/65535