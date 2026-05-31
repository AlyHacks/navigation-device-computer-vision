import sys
sys.path.insert(0, "build/lib.linux-armv7l-2.7")
import time
import board
import busio
import adafruit_vl53l1x

class VL53L1X:
    def __init__(self, i2c_bus=1, i2c_address=0x29):
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.sensor = adafruit_vl53l1x.VL53L1X(i2c_bus=self.i2c_bus, i2c_address=self.i2c_address)
        self.sensor.open()
        self.sensor.start_ranging(1)

    def read_distance(self):
        print("Initializing VL53L1X sensor...")
        distance = self.sensor.get_distance()
        return (f"Distance: {distance} mm")

tof = VL53L1X.VL53L1X()
read_distance = tof.read_distance()
print(read_distance)
tof.stop_ranging()
