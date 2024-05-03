from machine import Pin, ADC
import utime

# Settings
ADJUST_STRENGTH = 20
DEADZONE = 0.12
CALIBRATION_VALS = 50
DIRECTION = -1

# Setup ADC for potentiometer
pot = ADC(27)  # Assuming ADC0 is pin 26
led = Pin(25, Pin.OUT)  # Setup Pin for LED
# Setup Pin for switch
switch = Pin(14, Pin.IN, Pin.PULL_UP)

safe_max = 37929.8
safe_min = 19586.72
safe_mid = 28408.24
vals = []


def translatePot(latest):
    global safe_mid
    # check if rate of change is low enough to determine if it should be concidered the new zero
    if max(latest) - min(latest) < 1000:
        safe_mid = sum(latest) / len(latest)


def displayPot(pot):
    return (pot - safe_mid) / (safe_max - safe_min)


def sendBrightness(pot, sw):
    print((DIRECTION * pot * ADJUST_STRENGTH), sw)


safe_mid = pot.read_u16()

count = 0
while True:
    pot_value = pot.read_u16()  # Read potentiometer value
    screen_selected = switch.value()  # Read switch state
    vals.append(pot_value)
    count += 1
    if count > CALIBRATION_VALS:
        translatePot(vals[-CALIBRATION_VALS:])
        count = 0
    if abs(displayPot(pot_value)) > DEADZONE:
        sendBrightness(displayPot(pot_value), screen_selected)
    utime.sleep(0.2)
    if displayPot(pot_value) > 0:
        led.value(1)
    else:
        led.value(0)
