import sys
import board
import busio
import time
import displayio
from adafruit_display_text import label

from digitalio import DigitalInOut

import adafruit_esp32spi as esp32spi
import adafruit_requests as requests

from secrets import secrets

import draw

class Weather:

    def __init__(self, weerlive_response):

        # current weather
        self.plaats = weerlive_response['plaats']
        self.temp = weerlive_response['temp'] + '°C'
        self.gtemp = weerlive_response['gtemp'] + '°C'
        self.samenvatting = weerlive_response['samenv']
        self.wind = weerlive_response['windr'] + ' ' + weerlive_response['winds']
        self.sun = weerlive_response['sup'] + '-' + weerlive_response['sunder']
        self.lv = weerlive_response['lv']
        self.luchtd = weerlive_response['luchtd'].strip()
        self.image = weerlive_response['image']

        if weerlive_response['alarm'] != '0':
            self.alarmtxt = weerlive_response.get('alarmtxt')[:100]
        else:
            self.alarmtxt = ''

        # forecasts
        self.verwachting = weerlive_response['verw']
        self.d0weer = weerlive_response['d0weer']
        self.d1weer = weerlive_response['d1weer']
        self.d2weer = weerlive_response['d2weer']

        self.d0temp = weerlive_response['d0tmin'] + '-' + weerlive_response['d0tmax'] + '°C'
        self.d1temp = weerlive_response['d1tmin'] + '-' + weerlive_response['d1tmax'] + '°C'
        self.d2temp = weerlive_response['d2tmin'] + '-' + weerlive_response['d2tmax'] + '°C'

        self.d0wind = weerlive_response['d0windr'] + ' ' + weerlive_response['d0windk']
        self.d1wind = weerlive_response['d1windr'] + ' ' + weerlive_response['d1windk']
        self.d2wind = weerlive_response['d2windr'] + ' ' + weerlive_response['d2windk']

        self.d0neerslag = weerlive_response['d0neerslag'] + '%'
        self.d1neerslag = weerlive_response['d1neerslag'] + '%'
        self.d2neerslag = weerlive_response['d2neerslag'] + '%'

        self.d0zon = weerlive_response['d0zon'] + '%'
        self.d1zon = weerlive_response['d1zon'] + '%'
        self.d2zon = weerlive_response['d2zon'] + '%'


class WeerliveClient:

    def __init__(self, wifi, draw):
        self.__wifi = wifi
        self.__draw = draw
        self.__update_interval = 300

        self.__weather = None

        self.__last_update = time.monotonic() - (self.__update_interval + 1)

        self.__uri =  "http://weerlive.nl/api/json-data-10min.php?key="+secrets['weerlive_key'] + '&locatie=' + secrets['GPS_COORDS']


    def update(self):
        if time.monotonic() - self.__last_update <= self.__update_interval:
            return

        while True:
            try:
                print("requesting weerlive...")
                response = self.__wifi.get(self.__uri).json()['liveweer'][0]

                self.__weather = Weather(response)
                self.__last_update = time.monotonic()

            except Exception as e:
                sys.print_exception(e)
                print("exception requesting weerlive; will retry")
                time.sleep(5)
                continue
            
            break

    def draw_current(self, wait_time):
        self.update()
        
        self.__draw.reset()
        self.__draw.draw_icon(self.__weather.image)
        self.__draw.draw_text(self.__weather.temp, 'x-large', 0xFFFF00, 10, 25)
        self.__draw.draw_text(self.__weather.samenvatting, 'large', 0xFFFF00, 10, 60)

        x = 150
        y = 100

        # self.__draw.draw_text('Waarnemingen', 'medium', 0xFFFFFF, 10, y)
        # self.__draw.draw_text(self.__weather.plaats, 'medium', 0xFFFFFF, x, y)
        # y += 25

        self.__draw.draw_text('Gevoelstemp', 'medium', 0xFFFFFF, 10, y)
        self.__draw.draw_text(self.__weather.gtemp, 'medium', 0xFFFFFF, x, y)
        y += 25

        self.__draw.draw_text('Wind', 'medium', 0xFFFFFF, 10, y)
        self.__draw.draw_text(self.__weather.wind, 'medium', 0xFFFFFF, x, y)
        y += 25
   
        self.__draw.draw_text('Luchtdruk', 'medium', 0xFFFFFF, 10, y)
        self.__draw.draw_text(self.__weather.luchtd, 'medium', 0xFFFFFF, x, y)
        y += 25

        self.__draw.draw_text('Zon', 'medium', 0xFFFFFF, 10, y)
        self.__draw.draw_text(self.__weather.sun, 'medium', 0xFFFFFF, x, y)
        y += 25
 
        if self.__weather.alarmtxt:
            self.__draw.draw_wrapped(self.__weather.alarmtxt, 'medium', 0xFF0000, 10, y, 50, 25)
        else:
            self.__draw.draw_text('geen waarschuwingen', 'medium', 0xFFFF00, 10, y)
            
        self.__draw.show()
        time.sleep(wait_time)

    def draw_forecasts(self, wait_time):
        self.update()
        self.__draw.reset() 

        self.__draw.draw_icon(self.__weather.d0weer)
        self.__draw.draw_text(self.__weather.d0temp, 'x-large', 0xFFFF00, 10, 25)
        self.__draw.draw_wrapped(self.__weather.verwachting, 'medium', 0xFFFF00, 10, 60, 30, 20)

        x1=65
        x2=150
        x3=235
        y=120

        self.__draw.draw_text('Vandaag', 'medium', 0xFFFF00, x1, y)
        self.__draw.draw_text('Morgen', 'medium', 0xFFFF00, x2, y)
        self.__draw.draw_text('Overmorgen', 'medium', 0xFFFF00, x3, y)

        y += 25
        self.__draw.draw_text('Temp', 'medium', 0xFFFF00, 10, y)
        self.__draw.draw_text(self.__weather.d0temp, 'medium', 0xFFFFFF, x1, y)
        self.__draw.draw_text(self.__weather.d1temp, 'medium', 0xFFFFFF, x2, y)
        self.__draw.draw_text(self.__weather.d2temp, 'medium', 0xFFFFFF, x3, y)

        y += 25
        self.__draw.draw_text('Zon', 'medium', 0xFFFF00, 10, y)
        self.__draw.draw_text(self.__weather.d0zon, 'medium', 0xFFFFFF, x1, y)        
        self.__draw.draw_text(self.__weather.d1zon, 'medium', 0xFFFFFF, x2, y)
        self.__draw.draw_text(self.__weather.d2zon, 'medium', 0xFFFFFF, x3, y)

        y += 25
        self.__draw.draw_text('Nrslg', 'medium', 0xFFFF00, 10, y)
        self.__draw.draw_text(self.__weather.d0neerslag, 'medium', 0xFFFFFF, x1, y)                
        self.__draw.draw_text(self.__weather.d1neerslag, 'medium', 0xFFFFFF, x2, y)        
        self.__draw.draw_text(self.__weather.d2neerslag, 'medium', 0xFFFFFF, x3, y)

        y += 25
        self.__draw.draw_text('Wind', 'medium', 0xFFFF00, 10, y)
        self.__draw.draw_text(self.__weather.d0wind, 'medium', 0xFFFFFF, x1, y)         
        self.__draw.draw_text(self.__weather.d1wind, 'medium', 0xFFFFFF, x2, y) 
        self.__draw.draw_text(self.__weather.d2wind, 'medium', 0xFFFFFF, x3, y)

        self.__draw.show()
        time.sleep(wait_time)
