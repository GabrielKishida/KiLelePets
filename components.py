from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time

class LcdController:
    def __init__(self):
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
        self.lcd.clear()

    def write(self, message1, message2=None):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(message1)
        if message2:
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(message2)

class ServoController:
    SERVO_PIN = 12

    def __init__(self):
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        self.servo = GPIO.PWM(self.SERVO_PIN, 50)  # 50Hz PWM frequency for servo
        self.servo.start(0)

    def left(self):
        for i in range(0,400):
            self.servo.ChangeDutyCycle(5 + i/100)
            time.sleep(0.001)
        self.servo.ChangeDutyCycle(0)

    def center(self):
        for i in range(0,400):
            self.servo.ChangeDutyCycle(9 - i/100)
            time.sleep(0.001)
        self.servo.ChangeDutyCycle(0)
    
    def servo_stop(self):
        self.servo.stop()

class LedsController:
    LED_PINS = [22, 27, 4]

    def __init__(self):
        for led in self.LED_PINS:
            GPIO.setup(led, GPIO.OUT)
            GPIO.output(led, GPIO.LOW)

    def turn_red_led(self, on):
        GPIO.output(self.LED_PINS[0], GPIO.HIGH if on else GPIO.LOW)
    
    def turn_yellow_led(self, on):
        GPIO.output(self.LED_PINS[1], GPIO.HIGH if on else GPIO.LOW)
    
    def turn_green_led(self, on):
        GPIO.output(self.LED_PINS[2], GPIO.HIGH if on else GPIO.LOW)

class ButtonsController:
    PLUS_PIN = 5
    MINUS_PIN = 6
    CONFIRM_PIN = 26
    DEBOUNCE_DELAY = 0.2 

    def __init__(self):
        GPIO.setup(self.PLUS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.MINUS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.CONFIRM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.last_pressed_time = {
            self.PLUS_PIN: 0,
            self.MINUS_PIN: 0,
            self.CONFIRM_PIN: 0
        }

    def is_button_pressed(self, pin):
        current_time = time.time()
        if GPIO.input(pin) == GPIO.HIGH:
            if current_time - self.last_pressed_time[pin] > self.DEBOUNCE_DELAY:
                self.last_pressed_time[pin] = current_time
                return True
        return False
    
    def is_plus_pressed(self):
        return self.is_button_pressed(self.PLUS_PIN)

    def is_minus_pressed(self):
        return self.is_button_pressed(self.MINUS_PIN)

    def is_confirm_pressed(self):
        return self.is_button_pressed(self.CONFIRM_PIN)
    

class DistanceController:
    TRIG_PIN = 23
    ECHO_PIN = 24
    def __init__(self):
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

    def read_distance(self):
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.ECHO_PIN) == 0:
            start_time = time.time()

        while GPIO.input(self.ECHO_PIN) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2  # Distance in cm
        return distance
