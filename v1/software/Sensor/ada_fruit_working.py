import board
import busio
import adafruit_vl53l5cx
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l5cx.VL53L1X(i2c)

def start_ranging():
    sensor.start_ranging(1)
    distance = sensor.distance
    print(f"Distance: {distance} mm")

while True:
    start_ranging()
    time.sleep(1)
    if KeyboardInterrupt:
        break
sensor.clear_interrupt()

