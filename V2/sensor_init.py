
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

def led_buzzer_control(column, distance, ledr, ledl):   #the position of object is a fraction from 0 to 1, 0 is left#turns on the led for a time based on distance
    if (column>=0 and column<=3) and distance < 1000:
        print("left")
        ledr.off()
        ledl.blink(on_time=0.25, off_time=(distance)/100)
    elif (column>3 and column<=7) and distance < 1000:
        print("right")
        ledl.off()
        ledr.blink(on_time=0.25, off_time=(distance/100))
    else:
        ledr.off()
        ledl.off()

try:   
    while True:
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



            for y in (-1, 0, 1):
                for x in (-1, 0, 1):

                    ny = row+y
                    nx = column+x
                    if ny < 0 or ny > 8 or nx < 0 or nx > 8:
                        continue
                    if arr[ny, nx] <= min_distance+10 and arr[ny, nx] >= min_distance-10:
                        true_cnt += 1

            if true_cnt >= 3:
                led_buzzer_control(column, min_distance, ledr, ledl)


            # Scale view to a fixed distance
        time.sleep(0.01)  # Avoid polling *too* fast

except KeyboardInterrupt:
    exit()
