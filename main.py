import RPi.GPIO as GPIO
import time
from components import LcdController, ServoController, LedsController, ButtonsController, DistanceController

lcd = LcdController()
servo = ServoController()
leds = LedsController()
buttons = ButtonsController()
distance = DistanceController()

try:
    print("Running KiLele main script")
    while True:
        leds.turn_green_led(True)
        leds.turn_yellow_led(True)
        leds.turn_red_led(True)
        time.sleep(1)
        leds.turn_red_led(False)
        time.sleep(1)
        leds.turn_yellow_led(False)
        time.sleep(1)
        leds.turn_green_led(False)
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Cleanup GPIO and stop servo PWM
    servo.servo_stop()
    GPIO.cleanup()
