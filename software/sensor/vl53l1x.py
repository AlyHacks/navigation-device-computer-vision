import time
import VL53L1X
from smbus2 import SMBus, i2c_msg
#figure out the i2c address of the sensor using i2cdetect -y 1
class VL53L1X:
    def __init__(self, i2c_bus=1, i2c_address=0x29):
        print("Initializing VL53L1X sensor...")
    tof = VL53L1X.VL53L1X()
    
    tof.start_ranging(1) # 1=short, 2=medium, 3=long 

    distance_in_mm = tof.get_distance()
    print(f"Distance: {distance_in_mm} mm")



    tof.stop_ranging()