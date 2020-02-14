import time
import sys
from secrets import secrets


class SunTimes:
    def __init__(self, response):
        self.azimuth = response['azimuth'] + '°'
        self.altitude = response['altitude'] + '°'
        self.sunrise = response['sunrise'][:-3]
        self.sunset = response['sunset'][:-3]
        self.culmination = response['culmination'][:-3]
        self.culmination_altitude = response['culminationAltitude'] + '°'

class SuntimesClient:

    def __init__(self, wifi):
        self.__wifi = wifi
        lat_lng = [ str(item) for item in secrets['GPS_COORDS'].split(',') ]
        self.__uri = secrets['suntimes_uri'] + '?lat=' + lat_lng[0] + '&lng=' + lat_lng[1]

        self.__suntimes = None
        self.__update_interval = 60
        self.__last_update = time.monotonic() - (self.__update_interval + 1)

    def update(self):
        if time.monotonic() - self.__last_update <= self.__update_interval:
            return

        while True:
            try:
                print("requesting gcp suntimes...")
                response = self.__wifi.get(self.__uri).json()
                self.__suntimes = SunTimes(response)

                self.__last_update = time.monotonic()

            except Exception as e:
                sys.print_exception(e)
                print("exception requesting gcp suntimes; will retry")
                time.sleep(5)
                continue
            
            break

    def get_suntimes(self):
        self.update()
        return self.__suntimes

