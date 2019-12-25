import board
import busio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import terminalio
from adafruit_display_text import label
import time
import neopixel

from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager

import adafruit_requests as requests

def wifi_manager():

    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)

    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

    return adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)