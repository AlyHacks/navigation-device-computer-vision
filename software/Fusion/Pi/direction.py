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


ledr = LED(4)
ledl = LED(5)

camera_buffer = []
tof_buffer = []
fused = {"timestamp": 0, "distance": 0, "object": 0}
compare = []
correct_index = 0
last_ten_box = []

#for the sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l1x.VL53L1X(i2c)
sensor.timing_budget = 50

def starting():
    sensor.start_ranging()
    distance = sensor.distance
    return distance
        
#still using yolo code#
# need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
model = YOLO('yolov8n.pt')

picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
)


picam2.start()
time.sleep(2)

camera_buffer = deque(maxlen=20) #removes frames when the buffer gets too large
tof_buffer = deque(maxlen=20)
compare = deque(maxlen=3)
last_ten_box = deque(maxlen=10) #stores the last 10 boxes of the largest contour, to find the average position of the object

while True:
    areas = [] #create list to store areas of contours for each object per frame
    areas = deque(maxlen=10) #stores the last 10 areas of the largest contour, to find the average position of the object
    
    frame = picam2.capture_array()
    timestamp_c = time.monotonic_ns() #does not jump even if system clock changes
    results = model.track(frame)
    camera_buffer.append((timestamp_c, frame, results))
    image = results[0].plot()
    cv2.imshow('YOLOv8 Detection', image)
    

    distance = starting()
    timestamp_s = time.monotonic_ns()
    
    tof_buffer.append((timestamp_s, distance))
    sensor.clear_interrupt()
    
    last_three_c = list(camera_buffer)[-3:] #takes the latest 3 camera frames
    last_s = tof_buffer[-1] #takes the last sensor frame
    last_time_s = last_s[0]



    for timestamp_c, distance, results in last_three_c:#iterates througuh the 3 camera frames
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                x1, y1, x2, y2= box.xyxy[0]

                x1 = x1.item()
                x2 = x2.item()
                y1 = y1.item()
                y2 = y2.item()

                area = (x2-x1)*(y2-y1)

                last_ten_box.append((x1, y1, x2, y2)) #stores the last 10 boxes of the largest contour, to find the average position of the object

                areas.append(area)
                maximum_area = max(areas)
                maximum_area_index = areas.index(maximum_area) #find index of the maximum contour area at the frame
                
                x_1 = last_ten_box[maximum_area_index][0].item()
                y_1 = last_ten_box[maximum_area_index][1].item()
                x_2 = last_ten_box[maximum_area_index][2].item()
                y_2 = last_ten_box[maximum_area_index][3].item()

                cx = (x_2-x_1)/2 #needs to be of the max area contour, so need to find the index of the max area and use that to get the correct cx and cy

            

                fused["object"] = class_name  #gets object
                
                difference = abs(timestamp_c-last_time_s) #finds the closest camrea frame timestamp to the closest sensor reading
                compare.append(difference) #stores it in a compare list to compare the three differences
                
                correct_index = compare.index(min(compare)) #finds the index of the minimum 0->-3, 1->-2, 2->-1
                
                fused["timestamp"] = last_three_c[correct_index-1][0] #gets the correct timestamp of camera frame,        
                fused["distance"] = last_s[1] #takes the distance from the last_s tuple
                distance = fused["distance"]    

                        
                if (cx>0 and cx<320) and distance < 1000:
                    x = cx/640 #the position of object is a fraction from 0 to 1, 0 is left
                    ledr.on()
                    time.sleep(0.25) #turns on the led for a time based on distance
                    ledl.on()
                    time.sleep(0.25) #turns on the led for a time based on distance
                    ledr.off()
                    time.sleep(distance/(100*x)) #led off based on position and distnace
                    ledl.off()
                    time.sleep((distance*x)/100)
                elif cx>=320 and cx<640 and distance < 1000:
                    x = cx/640 #the position of object is a fraction from 0 to 1, 0 is left
                    ledr.on()
                    time.sleep(0.25) #turns on the led for a time based on distance
                    ledl.on()
                    time.sleep(0.25) #turns on the led for a time based on distance
                    ledr.off()
                    time.sleep((distance*(1-x))/100) #led off based on position and distnace
                    ledl.off()
                    time.sleep(distance/100*(1-x))
                else:
                    ledr.off()
                    ledl.off()


        
    if cv2.waitKey(1) == ord('q'):
        print("error")
        break
    time.sleep(0.05)

picam2.stop()
cv2.destroyAllWindows()