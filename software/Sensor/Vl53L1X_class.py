import board
import busio
import adafruit_vl53l1x
import time


class VL53L1X:
    def __init__(self, i2c_bus=1, i2c_address=0x29):
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.i2c_address = i2c_address
        self.sensor = adafruit_vl53l1x.VL53L1X(i2c_bus)
    

    def read_distance(self):
        self.sensor.open()
        self.sensor.start_ranging(1)
        print("Initializing VL53L1X sensor...")
        distance = self.sensor.get_distance()
        return (f"Distance: {distance} mm")
    

    vl53l1x = VL53L1X()
    while True:
        try:
            distance = vl53l1x.read_distance()
            print(distance)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            break