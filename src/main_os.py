from microbit import *
import time, sys

clear = display.clear

pin0.set_touch_mode(pin0.CAPACITIVE)
pin1.set_touch_mode(pin1.CAPACITIVE)
pin2.set_touch_mode(pin2.CAPACITIVE)


PASSWORD = "0112"

def _generate_menu_buttons(cursor_pos):
    display.show(Image("\n".join(["4000{}".format(9 if cursor_pos == i else 0) for i in range(5)])))

def menu(options):
    clear()
    _generate_menu_buttons(0)
    pos = 0
    while True:
        if button_b.is_pressed():
            pos += 1 if pos < 4 else 0
            _generate_menu_buttons(pos)
            time.sleep(0.2)
        if button_a.is_pressed():
            pos -= 1 if pos > 0 else 0
            _generate_menu_buttons(pos)
            time.sleep(0.2)
        if pin_logo.is_touched():
            clear()
            options[pos]()
            if pos == 0:
                sys.exit(0)
            _generate_menu_buttons(0)
            pos = 0
            
        
def off():
    for i in range(5, -1, -1):
        display.show(
            Image("00000\n{}00000".format((("9" * i) + "0" * (5 - i) + "\n") * 2))
        )
        time.sleep(0.2)

def getnum():
    while True:
        if pin0.is_touched():
            return "0"
        if pin1.is_touched():
            return "1"
        if pin2.is_touched():
            return "2"
        if accelerometer.was_gesture("shake"):
            return "break"
        if pin_logo.is_touched():
            return "off"

def login():
    while True:
        breaked = False
        result = ""
        for i in range(1, 5):
            num = getnum()

            if num == "break":
                display.clear()
                breaked = True
                break

            if num == "off":
                off()
                sys.exit(0)
            
            display.show(
                Image(("8" * i) + ("0" * (5 - i)) + ("00000\n" * 4))
            )
            result += num
            time.sleep(0.2)

        if result == PASSWORD:
            return
        else:
            if not breaked:
                display.show(Image.SAD)
                time.sleep(0.3)
            display.clear()
        breaked = False