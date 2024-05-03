import serial as s
import monitorcontrol as mc

board = s.Serial("COM3", 9600)


def getPot():
    while True:
        if board.in_waiting > 0:
            line = board.readline().decode("utf-8").strip()
            pot, sw = line.split(" ")
            return int(round(float(pot))), int(sw)


def changeBrightness(pot, sw):
    monitor = mc.get_monitors()[sw]
    with monitor:
        prev_luminance = monitor.get_luminance()
        luminance = prev_luminance + pot
        if luminance > 100:
            luminance = 100
        elif luminance < 0:
            luminance = 0
        monitor.set_luminance(luminance)


def main():
    while True:
        pot, sw = getPot()
        # Change brightness if difference is greater than 0.15
        try:
            changeBrightness(pot, sw)
        except Exception as e:
            print("Error changing brightness:", e)


main()
