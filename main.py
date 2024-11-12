import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Servo motor setup (PWM on GPIO 12)
SERVO_PIN = 12
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM frequency for servo
servo.start(0)  # Start PWM with 0 duty cycle (servo neutral)

# Ultrasonic sensor setup (HC-SR04 on GPIO 23 and 24)
TRIG_PIN = 23
ECHO_PIN = 24
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# LCD display setup (I2C on GPIO 2 and GPIO 3)
# Note: Use the 'smbus' library for I2C communication with the LCD
# This code doesn't set up GPIO 2 and 3 directly as they're managed by the I2C library

# LED setup (GPIO 4, 22, and 27 for On/Off control)
LED_PINS = [4, 22, 27]
for led in LED_PINS:
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)  # Start with LEDs off

# Tactile buttons setup (GPIO 5, 6, and 26)
BUTTON_PINS = {"press_plus": 5, "press_minus": 6, "confirm": 26}
for button in BUTTON_PINS.values():
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Use pull-down resistors


# Function to control servo
def set_servo_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)


# Function to read distance from HC-SR04
def read_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2  # Distance in cm
    return distance


# Example usage
try:
    print("Running KiLele main script")
    while True:
        # Example: Rotate servo to 90 degrees
        set_servo_angle(90)

        # Example: Measure distance
        distance = read_distance()
        print(f"Distance: {distance:.2f} cm")

        # Example: Toggle LEDs
        for led in LED_PINS:
            GPIO.output(led, not GPIO.input(led))
            time.sleep(0.5)

        # Example: Check button states
        for name, pin in BUTTON_PINS.items():
            if GPIO.input(pin) == GPIO.HIGH:
                print(f"{name} button pressed")

        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Cleanup GPIO and stop servo PWM
    servo.stop()
    GPIO.cleanup()
