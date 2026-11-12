
import time
import vl53l5cx_ctypes as vl53l5cx
import st7789
import numpy
from PIL import Image
from matplotlib import cm
import numpy as np
from gpiozero import LED

loopcount = 0
ledl = LED(5)
ledr = LED(4)

vl53 = vl53l5cx.VL53L5CX()
# This is a visual demo, so prefer speed over accuracy
vl53.set_ranging_frequency_hz(15)
vl53.set_integration_time_ms(20)
vl53.set_resolution(8*8)
vl53.start_ranging()
last_state = None

def led_buzzer_control(column, distance, ledr, ledl):
    global last_state
    if distance < 1000 and 0 <= column <= 3:
        state = ("left", round(distance, -2))   # bucket distance to the nearest 100
    elif distance < 1000 and 3 < column <= 7:
        state = ("right", round(distance, -2))
    else:
        state = None

    if state == last_state:
        return            # nothing changed, so let the current blink keep running
    last_state = state

    ledl.off(); ledr.off()
    if state:
        led = ledl if state[0] == "left" else ledr
        led.blink(on_time=0.25, off_time=max(state[1], 50) / 1000)

try:   
    while True:
        loop1 = time.perf_counter()
        true_cnt = 0
        if vl53.data_ready():
            data = vl53.get_data()
            arr = np.flipud(np.array(data.distance_mm).reshape((8, 8))).astype('float64')

            #MINIMUM DISTANCE DETECTION
            min_distance = arr.min()
            
            min_position = np.argwhere(arr == min_distance)
            row, column = min_position[0][0], min_position[0][1]

            if min_distance == 0:
                continue
            
            print(min_distance)
            
            ny = row
            nx = column
            if ny < 0 or ny > 7 or nx < 0 or nx > 7:
                print("Invalid position")
            if nx > 0 and nx < 3:
                position = "left"
                print(position)
            elif nx > 3 and nx < 7:
                position = "right"
                print(position)
                                

            led_buzzer_control(column, min_distance, ledr, ledl)


            # Scale view to a fixed distance
        loop2 = time.perf_counter()
        print(f"Loop time {loop1-loop2}")
        time.sleep(0.01)  # Avoid polling *too* fast

except KeyboardInterrupt:
    exit()

