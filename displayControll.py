import serial as s
import serial.tools.list_ports as list_ports
import monitorcontrol as mc
from time import sleep

SERIAL_NUMBER = "454741505687539A"  # Serial number of the Raspberry Pi Pico


def find_pico_com_port():
    """Automatically find the COM port of the Raspberry Pi Pico."""
    ports = list_ports.comports()
    for port in ports:
        if (
            port.serial_number is not None and SERIAL_NUMBER in port.serial_number.upper()
        ):  # Check for Pico in the port description
            return port.device
    raise Exception("Raspberry Pi Pico not found. Please ensure it is connected.")


def getPot(board):
    while True:
        try:
            if board.in_waiting > 0:
                line = board.readline().decode("utf-8").strip()
                pot, sw = line.split(" ")
                return int(round(float(pot))), int(sw)
        except Exception as e:
            raise e
        sleep(0.1)


def changeBrightness(pot, sw):
    try:
        monitor = mc.get_monitors()[sw]
        with monitor:
            prev_luminance = monitor.get_luminance()
            luminance = prev_luminance + pot
            if luminance > 100:
                luminance = 100
            elif luminance < 0:
                luminance = 0
            monitor.set_luminance(luminance)
    except mc.VCPError as e:
        return


def main():
    print("Starting display control")
    board = None
    while True:
        if board is None or not board.is_open:
            print("Finding Pico COM port...")
            try:
                com_port = find_pico_com_port()
                board = s.Serial(com_port, 9600, timeout=1)
                print("Pico COM port found:", com_port)
            except Exception as e:
                print("Error finding Pico COM port:", e)
                sleep(5)
                continue

        try:
            pot, sw = getPot(board)
            print(pot, sw)
            changeBrightness(-pot, sw)
        except (s.SerialException, OSError) as e:
            print("Lost connection to Pico. Reconnecting...")
            try:
                board.close()
            except:
                pass
            board = None
            sleep(2)
        except Exception as e:
            continue


main()
