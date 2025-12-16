import board
import neopixel
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler
from kmk.modules.led import LED
from kmk.extensions.oled_display import OLED

keyboard = KMKKeyboard()

BUTTON_PINS = [board.GP26, board.GP27, board.GP28, board.GP29, board.GP0]  
ENCODER_A_PIN = board.GP4
ENCODER_B_PIN = board.GP2
ENCODER_PRESS_PIN = board.GP1
LED_PIN = board.GP3
OLED_SDA_PIN = board.GP6
OLED_SCL_PIN = board.GP7

keyboard.matrix = KeysScanner(
    pins=BUTTON_PINS,
    value_when_pressed=False,
)

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = ((ENCODER_A_PIN, ENCODER_B_PIN, ENCODER_PRESS_PIN))
encoder_handler.map = [KC.VOLU, KC.VOLD, KC.MUTE]


oled = OLED(OLED_SDA_PIN, OLED_SCL_PIN)
keyboard.modules.append(oled)

NUM_PIXELS = 5 
pixels = neopixel.NeoPixel(LED_PIN, NUM_PIXELS, auto_write=False, pixel_order=neopixel.GRB)

def start_led(color):
    for i in range(NUM_PIXELS):
        pixels[i] = color 
    pixels.show()

start_led((237, 205, 116))

media_state = {
    "is_playing": False,
    "side_icon": "♪",
}

def render_oled(): 
    if media_state["is_playing"]:
        playing_icon = "▶"
    else:
        "⏸"

    line = f'{media_state["side_icon"]} ⏮ {playing_icon} ⏭'
    oled.display_text(line)

def media_action():
    media_state["is_playing"] = not media_state["is_playing"]
    render_oled()

keyboard.keymap = [
    [KC.MPRV, KC.Macro(Press(KC.MPLY), on_press=media_action), KC.MNXT, KC.MRWD, KC.FFWD]
]

if __name__ == '__main__':
    keyboard.go()
