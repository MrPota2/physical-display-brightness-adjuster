import serial as s
import monitorcontrol as mc
import logging
import time

# Settings
ADJUST_STRENGTH = 20
DEADZONE = 0.12
CALIBRATION_VALS = 50
DIRECTION = -1


board = s.Serial("COM3", 9600)

safe_max = 37929.8
safe_min = 19586.72
safe_mid = 28408.24
vals = []


def getPot():
    while True:
        if board.in_waiting > 0:
            line = board.readline().decode("utf-8").strip()
            pot, sw = line.split(" ")
            return float(pot), int(sw)


# format the value to be between -1 and 1
def translatePot(latest):
    # check if rate of change is low enough to determine if it should be concidered the new zero
    print("Min: ", min(latest))
    print("Max: ", max(latest))
    print("difference: ", max(latest) - min(latest))
    if max(latest) - min(latest) < 1000:

        safe_mid = sum(latest) / len(latest)
        print("New Zero: ", safe_mid)


# Display pot as a value between -1 and 1
def displayPot(pot):
    return (pot - safe_mid) / (safe_max - safe_min)


def changeBrightness(pot, sw):
    monitor = mc.get_monitors()[sw]
    with monitor:
        prev_luminance = monitor.get_luminance()
        print("Step: ", int(DIRECTION * pot * ADJUST_STRENGTH))
        luminance = prev_luminance + int(DIRECTION * pot * ADJUST_STRENGTH)
        if luminance > 100:
            luminance = 100
        elif luminance < 0:
            luminance = 0
        monitor.set_luminance(luminance)


def mcTest():
    monitor = mc.get_monitors()[0]
    print(monitor.get_input_source(), monitor.get_luminance())


def startUp():
    global safe_mid
    safe_mid = getPot()[0]


def main():
    startUp()
    print("after", safe_mid)
    count = 0
    while True:
        pot, sw = getPot()
        if pot != -1:
            vals.append(pot)
            count += 1
            if count % CALIBRATION_VALS == 0:
                translatePot(vals[-CALIBRATION_VALS:])
            # Change brightness if difference is greater than 0.15
            if abs(displayPot(pot)) > DEADZONE:
                try:
                    changeBrightness(displayPot(pot), sw)
                except:
                    print("Error changing brightness")


main()
