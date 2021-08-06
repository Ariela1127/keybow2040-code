import board
import time
from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15

keymap = {0: Keycode.ONE,
          1: Keycode.FOUR,
          2: Keycode.SEVEN,
          3: "595",
          4: Keycode.TWO,
          5: Keycode.FIVE,
          6: Keycode.EIGHT,
          7: "695",
          8: Keycode.THREE,
          9: Keycode.SIX,
          10: Keycode.NINE,
          11: "795",
          12: Keycode.ZERO,
          13: Keycode.KEYPAD_ASTERISK,
          14: Keycode.ENTER,
          15: Keycode.ESCAPE}

special_key_indexes = [3, 7, 11]
modifier_key_indexes = [13, 14, 15]

rgb = (140, 0, 255)
special_rgb = (0, 255, 200)
modifier_rgb = (255, 157, 0)

short_debounce = 0.03
long_debounce = 0.15
debounce = 0.03
fired = False

# To prevent the strings (as opposed to single key presses) that are sent from
# refiring on a single key press, the debounce time for the strings has to be
# longer.
while True:
    keybow.update()

    for k in keymap.keys():
        if k in special_key_indexes:
            keys[k].set_led(*special_rgb)
        elif k in modifier_key_indexes:
            keys[k].set_led(*modifier_rgb)
        else:
            keys[k].set_led(*rgb)

        if keys[k].pressed:
            key_press = keymap[k]

            # If the key hasn't just fired (prevents refiring)
            if not fired:
                fired = True

                if k in special_key_indexes:
                    debounce = long_debounce
                    layout.write(key_press)
                else:
                    debounce = short_debounce
                    keyboard.send(key_press)

    # If enough time has passed, reset the fired variable
    if fired and time.monotonic() - keybow.time_of_last_press > debounce:
        fired = False
