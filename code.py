import board
import displayio
import digitalio
import neopixel
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_pixel_framebuf import PixelFramebuffer
import BLING
import coincap_prices

# Global vars
BLING_BRIGHTNESS = 0.01
FONT = "/fonts/5x8.pcf"
NEGLIGIBLE_CHANGE = 1
BIG_CHANGE = 3
HUGE_CHANGE = 10

font = bitmap_font.load_font(FONT)
CPC = coincap_prices.CoincapPriceChecker()

# Enable power to BLING pixel display
bling_power = digitalio.DigitalInOut(board.MATRIX_POWER)
bling_power.switch_to_output()
bling_power.value = True

# Setup BLING neopixel and PixelFrameBuffer objects
bling_pixel_width, bling_pixel_height = BLING.display.pixel_size()
bling_num_pixels = bling_pixel_width * bling_pixel_height
BLING_raw = neopixel.NeoPixel(
    board.MATRIX_DATA, bling_num_pixels, brightness=BLING_BRIGHTNESS, auto_write=False
)

# In the demo the BLING display object is named "the_bling" so you can see
# where the derived object is used more easily.
the_bling = BLING.display(matrix=BLING_raw, rotation=2)


def show_price(price, delta):

    if delta < -HUGE_CHANGE:
        FOREGROUND = (0, 0, 0)
        BACKGROUND = (255, 0, 0)
    if -HUGE_CHANGE <= delta < -BIG_CHANGE:
        FOREGROUND = (255, 0, 0)
        BACKGROUND = (0, 0, 0)
    elif -BIG_CHANGE <= delta < -NEGLIGIBLE_CHANGE:
        FOREGROUND = (228, 96, 96)
        BACKGROUND = (0, 0, 0)
    elif -NEGLIGIBLE_CHANGE < delta < NEGLIGIBLE_CHANGE:
        FOREGROUND = (255, 255, 255)
        BACKGROUND = (0, 0, 0)
    elif NEGLIGIBLE_CHANGE < delta < BIG_CHANGE:
        FOREGROUND = (0, 255, 0)
        BACKGROUND = (0, 0, 0)
    elif BIG_CHANGE < delta <= HUGE_CHANGE:
        FOREGROUND = (0, 0, 0)
        BACKGROUND = (0, 255, 0)
    elif HUGE_CHANGE < delta:
        FOREGROUND = (0, 0, 0)
        BACKGROUND = (0, 255, 0)
    else:
        FOREGROUND = (0, 0, 0)  # Default case
        BACKGROUND = (0, 255, 0)

    the_bling.fill(BACKGROUND)

    price_str = f"{price:.2f}"
    the_bling.text(
        str(price_str),
        font,
        x=1,
        y=0,
        color_foreground=FOREGROUND,
        color_background=BACKGROUND,
    )
    the_bling.show()

while True:
    price, delta = CPC.get_price("bitcoin")

    show_price(price, delta)

    time.sleep(60)
