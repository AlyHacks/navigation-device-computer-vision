
import time
import board
import busio
import adafruit_vl53l1x

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l1x.VL53L1X(i2c)
sensor.timing_budget = 50

def start():
    distance = sensor.distance
    return(f'distance is {distance} mm')

sensor.start_ranging()

while True:
    if sensor.data_ready:
        try:
            print(start())
            sensor.clear_interrupt()
        except KeyboardInterrupt:
                print("Exiting...")
                break
        time.sleep(0.1)