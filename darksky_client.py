import sys
import board
import busio
import time

from digitalio import DigitalInOut
import adafruit_esp32spi as esp32spi
import adafruit_requests as requests

from secrets import secrets

class DarkskyClient:

    def __init__(self):
        self.__update_interval = 600

        self.__current_fields=['time', 'summary', 'icon', 'precipProbability', 'precipIntensity', 'temperature', 'windSpeed', 'windBearing']
        self.__forecast_fields=['time', 'summary', 'icon', 'precipProbability', 'temperatureHigh', 'temperatureLow', 'windSpeed']

        self.__current=None
        self.__forecast=None
        self.__last_update = time.monotonic() - (self.__update_interval + 1)

    def get_current(self):
        self.update()
        return self.__current

    def get_forecast(self):
        self.update()
        return self.__forecast

    def update(self):
        if time.monotonic() - self.__last_update <= 600:
            return

        print("updating weather...")

        uri = "https://api.darksky.net/forecast/"+secrets['DARKSKY_KEY'] + '/' + secrets['GPS_COORDS'] + "?units=si&lang=nl&exclude=hourly,minutely,flags,alerts"
    
        try:
            current = None
            forecast = []

            response = requests.get(uri).json()
            current = {key:value for key, value in response['currently'].items() if key in self.__current_fields}
            
            for day in response['daily']['data']:
                forecast.append( {key:value for key, value in day.items() if key in self.__forecast_fields} )

            if current != None:
                self.__current = current
            if len(forecast) > 0:
                self.__forecast = forecast

            self.__last_update = time.monotonic()

        except Exception as e:
            sys.print_exception(e)

    def draw(self):
        self.update()

