import smbus2
import time

# I2C setup
I2C_ADDR = 0x27  # Change this to your LCD's I2C address
LCD_WIDTH = 16   # Maximum characters per line

# LCD Constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_BACKLIGHT = 0x08  # On
ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Initialize I2C
bus = smbus2.SMBus(1)  # I2C bus (1 for Raspberry Pi Zero 2 W)

def lcd_write_byte(bits, mode):
    """Send byte to data pins."""
    high_bits = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low_bits = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, high_bits)
    lcd_toggle_enable(high_bits)

    # Low bits
    bus.write_byte(I2C_ADDR, low_bits)
    lcd_toggle_enable(low_bits)

def lcd_toggle_enable(bits):
    """Toggle the enable pin."""
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, bits | ENABLE)
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, bits & ~ENABLE)
    time.sleep(E_DELAY)

def lcd_initialize():
    """Initialize the display."""
    lcd_write_byte(0x33, LCD_CMD)  # Initialize
    lcd_write_byte(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_write_byte(0x06, LCD_CMD)  # Cursor move direction
    lcd_write_byte(0x0C, LCD_CMD)  # Turn on, no cursor, no blink
    lcd_write_byte(0x28, LCD_CMD)  # 2 line, 5x7 matrix
    lcd_write_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(E_DELAY)

def lcd_message(message, line):
    """Display message on the LCD."""
    if line == 1:
        lcd_write_byte(LCD_LINE_1, LCD_CMD)
    elif line == 2:
        lcd_write_byte(LCD_LINE_2, LCD_CMD)

    message = message.ljust(LCD_WIDTH, " ")
    for char in message:
        lcd_write_byte(ord(char), LCD_CHR)


# Example usage
try:
    lcd_initialize()
    print("Running KiLele main script")
    while True:

        lcd_message("Hello, World!", 1)
        lcd_message("Raspberry Pi!", 2)
        time.sleep(5)

        lcd_message("Goodbye!", 1)
        lcd_message("", 2)

except KeyboardInterrupt:
    print("Program stopped by user")

