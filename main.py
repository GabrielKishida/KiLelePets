import RPi.GPIO as GPIO
import time
from components import LcdController, ServoController, LedsController, ButtonsController, DistanceController

GPIO.setmode(GPIO.BCM)
lcd = LcdController()
servo = ServoController()
leds = LedsController()
buttons = ButtonsController()
distance = DistanceController()

try:
    print("Running KiLele main script")
    plus_count = 0
    minus_count = 0
    confirm_count = 0
    while True:
        if buttons.is_confirm_pressed():
            confirm_count += 1
            print("confirm count: " + str(confirm_count))
        if buttons.is_plus_pressed():
            plus_count += 1
            print("plus count: " + str(plus_count))
        if buttons.is_minus_pressed():
            minus_count += 1
            print("minus count: " + str(minus_count))

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Cleanup GPIO and stop servo PWM
    servo.servo_stop()
    GPIO.cleanup()
