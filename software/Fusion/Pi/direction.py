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

ledr = LED(5)
ledl = LED(4)

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

sensor.start_ranging()

def distance():
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
last_ten_box = deque(maxlen=10)


setup2 = time.time()
setup = setup2-setup1
print(f"SETUP TIME IS: {setup}")

while True:
    
    timestamp1 = time.time()
    
    areas = []
    areas = deque(maxlen=10)
    
    frame = picam2.capture_array()
    timestamp_c = time.monotonic_ns() #does not jump even if system clock changes
    results = model.predict(frame) #faster than .track
    camera_buffer.append((timestamp_c, frame, results))
    
    image = results[0].plot()
    cv2.imshow('YOLOv8 Detection', image)
    

    distance = distance()
    timestamp_s = time.monotonic_ns()
    
    tof_buffer.append((timestamp_s, distance))
    sensor.clear_interrupt()
    
    last_three_c = list(camera_buffer)[-3:] #takes the latest 3 camera frames
    last_s = tof_buffer[-1] #takes the last sensor frame
    last_time_s = last_s[0]
        
    timestamp2 = time.time()
    
    timestamp = timestamp2-timestamp1
    print(f"TIME FOR TIMESTAMP: {timestamp}")
    
    loop1 = time.time()
    pos1 = time.time()
    for timestamp_c, distance, results in last_three_c:#iterates througuh the 3 camera frames
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                fused["object"] = class_name  #gets object
                x1, y1, x2, y2= box.xyxy[0]
                
                x1 = x1.item()
                x2 = x2.item()
                y1 = y1.item()
                y2 = y2.item()
                
                last_ten_box.append((x1,y1,x2,y2))
                
                area = (x2-x1)*(y2-y1)
                
                areas.append(area)
                max_area = max(areas)
                
                #print(f"MAX AREAS ARE: {max_area}")
                
                max_area_index = areas.index(max_area)

                x_1 = last_ten_box[max_area_index][0]
                y_1 = last_ten_box[max_area_index][1]
                x_2 = last_ten_box[max_area_index][2]
                y_2 = last_ten_box[max_area_index][3]
                
                cx = x_1+(x_2-x_1)/2                
    
                '''
                if cx>0 and cx<=213:
                    print("ON LEFT")
                elif cx>213 and cx<=426:
                    print("CENTER")
                elif cx>426 and cx<=640:
                    print("RIGHT")
                '''
            
                
                pos2 = time.time()
                pos = pos2-pos1
                print(f"POSITION TIME IS: {pos}")
        
                buzz1 = time.time()
        
                difference = abs(timestamp_c-last_time_s) #finds the closest camrea frame timestamp to the closest sensor reading
                compare.append(difference) #stores it in a compare list to compare the three differences
                
                correct_index = compare.index(min(compare)) #finds the index of the minimum 0->-3, 1->-2, 2->-1

                
                fused["timestamp"] = last_three_c[correct_index-1][0] #gets the correct timestamp of camera frame,        
                fused["distance"] = last_s[1] #takes the distance from the last_s tuple
                distance = fused["distance"]
                
                if (cx>0 and cx<213) and distance < 1000:
                    x = cx/640 #the position of object is a fraction from 0 to 1, 0 is left#turns on the led for a time based on distance
                    ledr.on()
                    time.sleep(0.25) #turns on the led for a time based on distance
                    ledr.off()
                    time.sleep((distance*x)/100)
                elif (cx>=213 and cx<426) and distance < 1000:
                    x = cx/640 #the position of object is a fraction from 0 to 1, 0 is left
                    ledr.on()
                    time.sleep(0.25) #turns on the led for a time based on distance
                    ledl.on()
                    time.sleep(0.25) #turns on the led for a time based on distance
                    ledr.off()
                    time.sleep(distance*(x)/100) #led off based on position and distnace
                    ledl.off()
                    time.sleep(distance/100*(x))
                elif (cx>=426 and cx<640) and distance < 1000:
                    x = cx/640
                    ledl.on()
                    time.sleep(0.25)
                    ledl.off()
                    time.sleep(distance*(1-x)/100)
                    
                else:
                    ledr.off()
                    ledl.off()
                    

                
                if distance > 30:
                    ledl.on()
                    time.sleep(0.25)
                    ledl.off()
                    time.sleep(distance/100)

                buzz2 = time.time()
                buzz = buzz2-buzz1
                print(f"BUZZ TIME IS: {buzz}")
        
    
    loop2 = time.time()
    entireloop = loop2-loop1
    print(f"TOTAL LOOP TIME: {entireloop}")
    
    if cv2.waitKey(1) == ord('q'):
        print("error")
        break
    time.sleep(0.05)

picam2.stop()
cv2.destroyAllWindows()
