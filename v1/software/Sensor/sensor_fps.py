import busio
import adafruit_vl53l1x
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l1x.VL53L1X(i2c)
sensor.timing_budget = 50

frame_count = 0
starting = time.monotonic()

def start():
    distance = sensor.distance
    return(f"Distance: {distance} mm")
        
sensor.start_ranging()

while True:
    if sensor.data_ready:
        try:
            frame_count += 1
            current_time = time.monotonic()
            elapsed_time = current_time - starting
        time.sleep(0.05)")errupt:t()tonic()_time

