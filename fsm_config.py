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

intervals = ["4hours", "8hours", "12hours"]
selected_interval_index = 1

sizes = ["small", "medium", "big"]
selected_size_index = 1

class MenuState(State):
    
    menu_transitions = {
        0: "menu_to_interval",
        1: "menu_to_size",
        2: "menu_to_auto",
        3: "menu_to_manual",
    }

    interval_size_dict = {
        0: "4H",
        1: "8H",
        2: "12H",
    }

    size_size_dict = {
        0: "P",
        1: "M",
        2: "G",
    }

    def __init__(self):
        super().__init__("Menu State")
        self.menu_texts = {
            0: ["CONFIGURAR", "INTERVALO: " + self.interval_size_dict[selected_interval_index]],
            1: ["CONFIGURAR", "TAMANHO: " + self.size_size_dict[selected_size_index]],
            2: ["SELECIONAR", "MODO AUTO"],
            3: ["SELECIONAR", "MODO MANUAL"],
        }
        self.menu_index = 0
    
    def enter(self):
        self.menu_index = 0
        self.menu_texts = {
            0: ["CONFIGURAR", "INTERVALO: " + self.interval_size_dict[selected_interval_index]],
            1: ["CONFIGURAR", "TAMANHO: " + self.size_size_dict[selected_size_index]],
            2: ["SELECIONAR", "MODO AUTO"],
            3: ["SELECIONAR", "MODO MANUAL"],
        }
        texts = self.menu_texts[0]
        lcd.write(texts[0], texts[1])

    def do(self):
        button_changed = False

        if buttons.is_minus_pressed():
            self.menu_index -= 1
            button_changed = True
        
        if buttons.is_plus_pressed():
            self.menu_index += 1
            button_changed = True
        
        if self.menu_index > 3: self.menu_index = 0
        elif self.menu_index < 0: self.menu_index = 3

        if button_changed:
            texts = self.menu_texts[self.menu_index]
            lcd.write(texts[0], texts[1])
        
        if buttons.is_confirm_pressed():
            return self.menu_transitions[self.menu_index]


class IntervalState(State):
    interval_texts = {
        0: ["INTERVALO", "4 HORAS"],
        1: ["INTERVALO", "8 HORAS"],
        2: ["INTERVALO", "12 HORAS"],
    }

    def __init__(self):
        super().__init__("Interval State")
    
    def enter(self):
        global selected_interval_index

        texts = self.interval_texts[selected_interval_index]
        lcd.write(texts[0], texts[1])

    def do(self):
        global selected_interval_index

        button_changed = False

        if buttons.is_minus_pressed():
            button_changed = True
            selected_interval_index-= 1
        
        if buttons.is_plus_pressed():
            button_changed = True
            selected_interval_index += 1
        
        if selected_interval_index > 2: selected_interval_index = 0
        elif selected_interval_index < 0: selected_interval_index = 2

        if button_changed:
            texts = self.interval_texts[selected_interval_index]
            lcd.write(texts[0], texts[1])
        
        if buttons.is_confirm_pressed():
            return "interval_to_menu"

class SizeState(State):
    size_texts = {
        0: ["TAMANHO", "PEQUENO"],
        1: ["TAMANHO", "MEDIO"],
        2: ["TAMANHO", "GRANDE"],
    }

    def __init__(self):
        super().__init__("Size State")
    
    def enter(self):
        texts = self.size_texts[selected_size_index]
        lcd.write(texts[0], texts[1])

    def do(self):
        global selected_size_index

        button_changed = False

        if buttons.is_minus_pressed():
            button_changed = True
            selected_size_index -= 1
        
        if buttons.is_plus_pressed():
            button_changed = True
            selected_size_index += 1
        
        if selected_size_index > 2: selected_size_index = 0
        elif selected_size_index < 0: selected_size_index = 2

        if button_changed:
            texts = self.interval_texts[selected_size_index]
            lcd.write(texts[0], texts[1])
        
        if buttons.is_confirm_pressed():
            return "size_to_menu"

class AutoState(State):
    def __init__(self):
        self.open = False
        self.open_time = 0
        super().__init__("Auto State")

    def do(self):
        print("Auto state")

class ManualState(State):

    meal_size_time_dict = {
        0: 0.5,
        1: 1,
        2: 1.5,
    }

    def __init__(self):
        super().__init__("Manual State")

    def enter(self):
        global selected_interval_index
        global selected_size_index

        self.meal_interval = selected_interval_index
        self.meal_size = selected_size_index 
    
    def trigger_open_servo(self):
        if not self.open:
            print("open servo")
            leds.turn_red_led(True)
            self.open = True
            self.open_time = time.time()
            servo.left()

    def update_open_servo(self):
        if self.open:
            current_time = time.time() - self.open_time
            print("servo is open for: " + str(current_time))
            if current_time > self.meal_size_time_dict[self.meal_size]:
                print("closing servo")
                leds.turn_red_led(False)
                self.open = False
                servo.center()

    def do(self):
        if buttons.is_confirm_pressed():
            self.trigger_open_servo()

menu_state = MenuState()
interval_state = IntervalState()
size_state = SizeState()
auto_state = AutoState()
manual_state = ManualState()

menu_state.add_transition("menu_to_interval", interval_state)
menu_state.add_transition("menu_to_size", size_state)
menu_state.add_transition("menu_to_auto", auto_state)
menu_state.add_transition("menu_to_manual", manual_state)

interval_state.add_transition("interval_to_menu", menu_state)
size_state.add_transition("size_to_menu", menu_state)

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
