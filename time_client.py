import time
import rtc
import sys
from secrets import secrets

class TimeClient:

    def __init__(self, wifi):
        self.__wifi = wifi
        self.__uri = 'http://worldtimeapi.org/api/timezone/' + secrets['timezone']
        
        self.__update_interval = 3600
        self.__last_update = time.monotonic() - (self.__update_interval + 1)

    def update(self):
        if time.monotonic() - self.__last_update <= self.__update_interval:
            return

        while True:
            try:
                print("requesting worldtimeapi...")
                response = self.__wifi.get(self.__uri).json()

                rtc.RTC().datetime = time.localtime(response['unixtime'] + response['raw_offset'])
                self.__last_update = time.monotonic()

            except Exception as e:
                sys.print_exception(e)
                print("exception requesting worldtimeapi; will retry")
                time.sleep(5)
                continue
            
            break

    def get_time(self):
        self.update()
        t = time.localtime()
        return "%02d:%02d:%02d" % (t[3], t[4], t[5])

    def get_date(self):
        self.update()
        t = time.localtime()
        return "%02d/%02d/%d" % (t[2], t[1], t[0])