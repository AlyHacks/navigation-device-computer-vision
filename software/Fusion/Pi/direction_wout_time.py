# this code is the same as direction.py, but without the time component, so it doesn't calculate the time between each action --> cleaner code

from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
import board
import busio
import adafruit_vl53l1x
import time
from collections import deque
from gpiozero import LED
import numpy as np

setup1 = time.time()

ledl = LED(5)
ledr = LED(4)

#creation of buffers and the fused dictionary to store the matched rgb and sensor frames
camera_buffer = []
tof_buffer = []
fused = {"timestamp": 0, "distance": 0, "object": 0}
compare = []
correct_index = 0
frame_boundbox = []

#for the sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l1x.VL53L1X(i2c)
sensor.timing_budget = 50
        
#still using yolo code#
# need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
model = YOLO('yolov8n.pt')


#configure the picam2 settings to be the correct format of 640x480 and RGB888 for the yolo model to work properly
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
)

def dist(sensor):
    sensor.start_ranging()
    distance = sensor.distance
    return distance

def buzzing(cx, distance, ledr, ledl):
    buzz1 = time.time()
    x = cx/640   #the position of object is a fraction from 0 to 1, 0 is left#turns on the led for a time based on distance
    # if there is both distance and object
    if (cx>0 and cx<213) and distance < 1000:
        ledr.off()
        ledl.blink(on_time=0.25, off_time=(distance*x)/100)
    elif (cx>=213 and cx<426) and distance < 1000:
        ledr.blink(on_time=0.25, off_time=(distance*x)/100)
        ledl.blink(on_time=0.25, off_time=(distance*(1-x))/100)
    elif (cx>=426 and cx<640) and distance < 1000:
        ledl.off()
        ledr.blink(on_time=0.25, off_time=(distance/100*x))
    # if there is only distance and no object
    elif distance < 1000 and cx is None:
        ledr.blink(on_time=0.25, off_time=(distance/100))
        ledl.blink(on_time=0.25, off_time=(distance/100))
    # if there is no distance and only object
    elif (cx>0 and cx<213) and distance is None:
        ledr.off()
        ledl.blink(on_time=0.5, off_time=0.5)
    elif (cx>=213 and cx<426) and distance is None:
        ledr.blink(on_time=0.5, off_time=0.5)
        ledl.blink(on_time=0.5, off_time=0.5)
    elif (cx>=426 and cx<640) and distance is None:
        ledl.off()
        ledr.blink(on_time=0.5, off_time=0.5)
    # if there is no distance and no object
    else:
        ledr.off()
        ledl.off()

def max_area(x1, x2, y1, y2, areas, frame_boundbox):

    
    frame_boundbox.append((x1,y1,x2,y2))
                    
    area = (x2-x1)*(y2-y1)
    
    areas.append(area)
    max_area = max(areas)
    
    #print(f"MAX AREAS ARE: {max_area}")
    
    max_area_index = areas.index(max_area)

    x_1 = frame_boundbox[max_area_index][0]
    y_1 = frame_boundbox[max_area_index][1]
    x_2 = frame_boundbox[max_area_index][2]
    y_2 = frame_boundbox[max_area_index][3]
    
    cx = x_1+(x_2-x_1)/2  
    return cx, x_1, y_1, x_2, y_2

def frame_calc(timestamp_c,last_s, compare, last_time_s, last_three_c, fused):
        for frame in last_three_c:
            frame_timestamp_c = frame[0]
            
            difference = abs(frame_timestamp_c-last_time_s) #finds the closest camrea frame timestamp to the closest sensor reading
            compare.append(difference) #stores it in a compare list to compare the three differences
            
            correct_index = compare.index(min(compare)) #finds the index of the minimum 0->-3, 1->-2, 2->-1
            
            fused["timestamp"] = last_three_c[correct_index][0] #gets the correct timestamp of camera frame,        
            fused["distance"] = last_s[1] #takes the distance from the last_s tuple
            distance = fused["distance"]

            compare.clear() #clears the compare list for the next iteration
        return distance, correct_index, fused


picam2.start()
time.sleep(2)

camera_buffer = deque(maxlen=20) #removes frames when the buffer gets too large
tof_buffer = deque(maxlen=20)
compare = deque(maxlen=3)


def main(ledr, ledl, sensor, picam2, model, camera_buffer, tof_buffer, compare, frame_boundbox, fused):
    while True:
        
        distance = 0
        timestamp1 = time.time()

        areas = []
        areas = deque(maxlen=10)
        frame_boundbox = []

        frame = picam2.capture_array()
        timestamp_c = time.monotonic_ns() #does not jump even if system clock changes
        results = model.predict(frame) #change back to track if needed
        camera_buffer.append((timestamp_c, frame, results))

        #unplot to make processing faster
        #image = results[0].plot()
        #cv2.imshow('YOLOv8 Detection', image)
        
        distance = dist(sensor)
        timestamp_s = time.monotonic_ns()

        tof_buffer.append((timestamp_s, distance))
        sensor.clear_interrupt()

        last_three_c = list(camera_buffer)[-3:] #takes the latest 3 camera frames
        last_s = tof_buffer[-1] #takes the last sensor frame
        last_time_s = last_s[0]

        distance, correct_index, fused = frame_calc(timestamp_c,last_s, compare, last_time_s, last_three_c, fused)

        for timestamp_c, frame, results in last_three_c[correct_index]:#iterates througuh the correct camera frame
                for box in results.boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    fused["object"] = class_name  #gets object
                    x1, y1, x2, y2= box.xyxy[0]
                    
                    x1 = x1.item()
                    x2 = x2.item()
                    y1 = y1.item()
                    y2 = y2.item()
                    
                    cx, x_1, x_2, y_1, y_2 = max_area(x1, x2, y1, y2, areas, frame_boundbox)                       
                    buzzing(cx, distance, ledr, ledl)

        
        
        if cv2.waitKey(1) == ord('q'):
            print("error")
            break
        time.sleep(0.05)


main(ledr, ledl, sensor, picam2, model, camera_buffer, tof_buffer, compare, frame_boundbox, fused)
picam2.stop()
cv2.destroyAllWindows()

# todo: try to optimize the frame calculation process