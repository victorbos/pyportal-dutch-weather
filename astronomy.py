import time

class Astronomy:

    def __init__(self, draw, suntimes_client, time_client):
        self.__draw = draw
        self.__suntimes_client = suntimes_client
        self.__time_client = time_client

    def draw(self, wait_time):
        self.__draw.reset()

        self.__draw.draw_icon('zonnig')

        time_label = self.__draw.draw_text('--:--:--', 'x-large', 0xFFFF00, 10, 25)
        date = self.__time_client.get_date()
        self.__draw.draw_text(date, 'large', 0xFFFF00, 10, 60)
        
        x = 100
        y = 90
        suntimes = self.__suntimes_client.get_suntimes()
        self.__draw.draw_text('Zon op:', 'medium', 0xFFFFFF, 10, y)
        self.__draw.draw_text(suntimes.sunrise, 'medium', 0xFFFFFF, x, y)
        
        y += 25
        self.__draw.draw_text('Zon onder:', 'medium', 0xFFFFFF, 10, y)
        self.__draw.draw_text(suntimes.sunset, 'medium', 0xFFFFFF, x, y)

        y += 25
        self.__draw.draw_text('Culminatie:', 'medium', 0xFFFFFF, 10, y)
        self.__draw.draw_text(
            suntimes.culmination + ', ' + suntimes.culmination_altitude
            , 'medium', 0xFFFFFF, x, y)

        y += 30
        self.__draw.draw_text('Elevatie:', 'medium', 0xFFFF00, 10, y)
        self.__draw.draw_text(suntimes.altitude, 'medium', 0xFFFF00, x, y)

        y += 25
        self.__draw.draw_text('Azimut:', 'medium', 0xFFFF00, 10, y)
        self.__draw.draw_text(suntimes.azimuth, 'medium', 0xFFFF00, x, y)

        self.__draw.show()

        now = time.monotonic()
        while time.monotonic() < (now + wait_time):    
            time_label.text = self.__time_client.get_time()
            