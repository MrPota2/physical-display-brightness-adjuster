from machine import Pin, ADC
import utime

# Setup ADC for potentiometer
pot = ADC(27)  # Assuming ADC0 is pin 26
led = Pin(25, Pin.OUT)  # Setup Pin for LED
# Setup Pin for switch
switch = Pin(14, Pin.IN, Pin.PULL_UP)


while True:
    pot_value = pot.read_u16()  # Read potentiometer value
    screen_selected = switch.value()  # Read switch state
    print(pot_value,screen_selected)
    utime.sleep(0.2)
    if pot_value/65535 < 0.45:
        led.value(1)
    else:
        led.value(0)
