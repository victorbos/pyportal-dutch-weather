import board
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes import rect
from auto_brightness import AutoBrightness

class Draw:
    def __init__(self):
        self.__fonts = {
            'small':  bitmap_font.load_font('fonts/Roboto-Light-12.bdf'),
            'medium': bitmap_font.load_font('fonts/Roboto-Light-16.bdf'),
            "large": bitmap_font.load_font('fonts/Roboto-Medium-22.bdf'),
            'x-large': bitmap_font.load_font('fonts/Roboto-Bold-48.bdf')
        }
        self.__display_group = displayio.Group(max_size=50)
        
        self.__auto_brightness = AutoBrightness()

    def show(self):
        board.DISPLAY.show(self.__display_group)
        self.__auto_brightness.set()

    def reset(self):
        self.__auto_brightness.dim()
        while self.__display_group:
            self.__display_group.pop()

    def draw_icon(self, icon):
        icon = "icons/" + icon + ".bmp"
        bitmap = displayio.OnDiskBitmap(open(icon, "rb"))
        self.__display_group.append(displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter()))

    def draw_text(self, text, font, color, x, y):
        txt = label.Label(font=self.__fonts[font], text=text, color=color)
        txt.x=x
        txt.y=y
        self.__display_group.append(txt)
        return txt

    def draw_wrapped(self, text, font, color, x, start_y, max_chars, spacing):
        lines = self.wrap_nicely(text, max_chars)
        line_number = 0
        for line in lines:
            self.draw_text(line, font, color, x, start_y + (line_number * spacing))
            line_number = line_number + 1

    def wrap_nicely(self, string, max_chars):
        """A helper that will return a list of lines with word-break wrapping.
        :param str string: The text to be wrapped.
        :param int max_chars: The maximum number of characters on a line before wrapping.
        """
        string = string.replace('\n', '').replace('\r', '') # strip confusing newlines
        words = string.split(' ')
        the_lines = []
        the_line = ""
        for w in words:
            if len(the_line+' '+w) <= max_chars:
                the_line += ' '+w
            else:
                the_lines.append(the_line)
                the_line = ''+w
        if the_line:      # last line remaining
            the_lines.append(the_line)
        # remove first space from first line:
        the_lines[0] = the_lines[0][1:]
        return the_lines
    
    def draw_bar(self, x, y, width, height, fill):
        bar = rect.Rect(x, y, width, height, fill=fill)
        self.__display_group.append(bar)

    
