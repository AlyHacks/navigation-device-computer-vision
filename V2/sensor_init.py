
import time
import vl53l5cx_ctypes as vl53l5cx
import ST7789
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
vl53.start_ranging()

def led_buzzer_control(cx, distance, ledr, ledl):
    x = cx/640   #the position of object is a fraction from 0 to 1, 0 is left#turns on the led for a time based on distance
    if (cx>0 and cx<320) and distance < 1000:
        print("left")
        ledr.off()
        ledl.blink(on_time=0.25, off_time=(distance*x)/100)
    elif (cx>=320 and cx<640) and distance < 1000:
        print("right")
        ledl.off()
        ledr.blink(on_time=0.25, off_time=(distance/100*x))
    else:
        ledr.off()
        ledl.off()

    
while True:
    true_cnt = 0
    if vl53.data_ready():
        data = vl53.get_data()
        arr = np.flipud(np.array(data.distance_mm).reshape((8, 8))).astype('float64')

        #MINIMUM DISTANCE DETECTION
        min_distance = arr.min()
        
        min_position = np.argwhere(arr == min_distance)
        row, column = np.where(arr == min_distance)


        
        if abs(min_position-(arr[row+1, column] or arr[row-1, column] or arr[row, column+1] or arr[row, column-1])) <= 10:
            true_cnt += 1
        if true_cnt >= 3:
            if column >= 0 and column <= 3:
                print("Object is on the left side of the sensor")
            elif column >= 4 and column <= 7:
                print("Object is on the right side of the sensor")
            #obtain position of the object since 
        # Scale view relative to the furthest distance
        # distance = arr.max()

        # Scale view to a fixed distance

        # Force to int
        arr = arr.astype('uint8')


    time.sleep(0.01)  # Avoid polling *too* fast
