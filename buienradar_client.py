import sys
import board
import busio
import time
import displayio


from digitalio import DigitalInOut

import adafruit_esp32spi as esp32spi
import adafruit_requests as requests

from secrets import secrets

class Rain:

    def __init__(self, time, rain):
        self.time = time
        self.bucket = self.__to_bucket(self.__to_mm_hr(rain))
        self.bucket_name = self.__bucket_to_name(self.bucket)

    def __to_mm_hr(self, value):
        return round(10**(( int(value) - 109)/32), 1)

    def __to_bucket(self, mm_hr):
        if mm_hr >= 100:
            return 5
        elif mm_hr >= 10:
            return 4
        elif mm_hr >= 5:
            return 3
        elif mm_hr >= 2:
            return 2
        elif mm_hr >= 0.1:
            return 1
        else:
            return 0

    def __bucket_to_name(self, bucket):
        return ['geen', 'Lichte neerslag', 'Matige neerslag', 'Zware neerslag', 'Zeer zware neerslag', 'Wolkbreuk'][bucket]


class BuienradarClient:

    def __init__(self, wifi, draw):
        self.__wifi = wifi
        self.__draw = draw

        self.__update_interval = 120
        self.__last_update = time.monotonic() - (self.__update_interval + 1)
        self.__rain_list = None

        lat_lon = [ str(round(float(item), 2)) for item in secrets['GPS_COORDS'].split(',') ]
        self.__uri = "http://gpsgadget.buienradar.nl/data/raintext/?lat=" + lat_lon[0] + "&lon=" + lat_lon[1]

    def update(self):
        if time.monotonic() - self.__last_update <= self.__update_interval:
            return

        while True:
            try:
                print("requesting buienradar...")
                response = self.__wifi.get(self.__uri)
                
                rain_list = str(response.content, None).split('\r\n')
                splitted_list = [ item.split('|') for item in rain_list if item ]

                if len(splitted_list) == 0:
                    raise RuntimeError("Received empty list from buienradar")

                self.__rain_list = [ Rain(item[1], item[0]) for item in splitted_list ]
                self.__last_update = time.monotonic()

            except Exception as e:
                sys.print_exception(e)
                print("exception requesting buienradar; will retry")
                time.sleep(5)
                continue

            break

    def draw(self, wait_time):
        self.update()
        self.__draw.reset()

        self.__draw_text()
        self.__draw_chart()

        self.__draw.show()

        if self.__has_rain():
            time.sleep(wait_time)
        else:
            time.sleep(5)

    def __draw_chart(self):
        start_x = 30
        base_y = 200
        bar_bucket_height = 30
        bar_width = 8
        bar_spacing = 2

        for i, rain in enumerate(self.__rain_list):
            bar_length = rain.bucket * bar_bucket_height + 1
            top_y = base_y - bar_length
            top_x = start_x + (bar_width * (i + 1)) + (i * bar_spacing)
        
            self.__draw.draw_bar(
                top_x,
                top_y,
                bar_width,
                bar_length,
                0x0000ff
            )

            if i % 5 == 0:
                self.__draw.draw_text(rain.time, 'small', 0xFFFFFF, top_x + bar_width, base_y + 20)
            
            if (i + 1) % 5 == 0:
                start_x = start_x + 3

    def __draw_text(self):
        start_rain = []
        end_rain = None
        for rain in self.__rain_list:
            if (not start_rain) and rain.bucket > 0:
                start_rain = [rain.time, rain.bucket_name]
            if (not end_rain) and start_rain and rain.bucket == 0:
                end_rain = rain.time

        if start_rain and end_rain:
            text = start_rain[1] + ' vanaf ' + start_rain[0] + ' tot ' + end_rain
        elif start_rain:
            text = start_rain[1] + ' vanaf ' + start_rain[0]
        else:
            text = 'Droog tot ' + self.__rain_list[-1].time

        if start_rain:
            self.__draw.draw_text(text, 'medium', 0xFFFF00, 20, 20)
        else:
            self.__draw.draw_text(text, 'large', 0xFFFF00, 85, 100)

    def __has_rain(self):
        any(rain.bucket > 0 for rain in self.__rain_list)
