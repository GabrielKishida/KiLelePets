import RPi.GPIO as GPIO
import time
from components import LcdController, ServoController, LedsController, ButtonsController, DistanceController
from fsm import FSM, State

GPIO.setmode(GPIO.BCM)
lcd = LcdController()
servo = ServoController()
leds = LedsController()
buttons = ButtonsController()
distance = DistanceController()

class MenuState(State):
    
    menu_transitions = {
        0: "menu_to_interval",
        1: "menu_to_size",
        2: "menu_to_auto",
        3: "menu_to_manual",
    }

    menu_texts = {
        0: ["CONFIGURAR", "INTERVALO"],
        1: ["CONFIGURAR", "TAMANHO"],
        2: ["SELECIONAR", "MODO AUTO"],
        3: ["SELECIONAR", "MODO MANUAL"],
    }

    def __init__(self):
        super().__init__("Menu State")
        self.menu_index = 0

    def do(self):
        if self.menu_index > 3: self.menu_index = 0
        elif self.menu_index < 0: self.menu_index = 3
        
        texts = self.menu_texts[self.menu_index]
        lcd.write(texts[0], texts[1])

        if buttons.is_minus_pressed():
            self.menu_index -= 1
        
        if buttons.is_plus_pressed():
            self.menu_index += 1
        
        if buttons.is_confirm_pressed():
            return self.menu_transitions[self.menu_index]


class IntervalState(State):
    def do(self):
        print("Interval State")

class SizeState(State):
    def do(self):
        print("Size State")

class AutoState(State):
    def do(self):
        print("Auto State")

class ManualState(State):
    def do(self):
        print("Manual State")

menu_state = MenuState()
interval_state = IntervalState("Interval")
size_state = SizeState("Size")
auto_state = AutoState("Auto")
manual_state = ManualState("Manual")

menu_state.add_transition("menu_to_interval", interval_state)
menu_state.add_transition("menu_to_size", size_state)
menu_state.add_transition("menu_to_auto", auto_state)
menu_state.add_transition("menu_to_manual", manual_state)

fsm_config = FSM(menu_state)

try:
    print("Running KiLele main script")
    while True:
        fsm_config.update()

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Cleanup GPIO and stop servo PWM
    servo.servo_stop()
    GPIO.cleanup()
