import smbus2

# Initialize I2C
bus = smbus2.SMBus(1)  # 1 indicates /dev/i2c-1
I2C_ADDR = 0x27        # Update with your detected address

try:
    bus.write_byte(I2C_ADDR, 0x00)  # Test write
    print("I2C communication successful!")
except Exception as e:
    print(f"I2C communication failed: {e}")