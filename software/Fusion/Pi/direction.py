from ultralytics import YOLO
import cv2
from picamera2 import Picamera2

import board
import busio
import adafruit_vl53l1x
import time
from collections import deque
from gpiozero import LED

led = LED(4)

camera_buffer = []
tof_buffer = []
fused = {"timestamp": 0, "distance": 0, "object": 0}
compare = []
correct_index = 0

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

while True:
    try:
        frame = picam2.capture_array()
        timestamp_c = time.monotonic_ns() #does not jump even if system clock changes
        results = model.track(frame)
        camera_buffer.append((timestamp_c, frame, results))
        image = results[0].plot()
        print(frame.shape)
        cv2.imshow('YOLOv8 Detection', image)
        

        distance = starting()
        timestamp_s = time.monotonic_ns()
        
        tof_buffer.append((timestamp_s, distance))
        sensor.clear_interrupt()
        
        last_three_c = list(camera_buffer)[-3:] #takes the latest 3 camera frames
        last_s = tof_buffer[-1] #takes the last sensor frame
                                     
        for timestamp, distance, results in last_three_c: #iterates througuh the 3 camera frames
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    x1, y1, x2, y2= box.xyxy[0]
                    print(x1, y1, x2, y2)
            
            
            difference = abs(timestamp_c-timestamp_s) #finds the closest camrea frame timestamp to the closest sensor reading
            compare.append(difference) #stores it in a compare list to compare the three differences
            correct_index = compare.index(min(compare)) #finds the index of the minimum 0->-3, 1->-2, 2->-1
            

            print("compare:", compare)
            
            fused["timestamp"] = last_three_c[correct_index][0] #gets the correct timestamp of camera frame,        
            fused["distance"] = last_s[1] #takes the distance from the last_s tuple
            fused["object"] = class_name #gets object
            
            print(fused)
        
        if x1 in range (0, 213):
            print("object on left")
        elif x1 in range (213, 426):
            print("object on center left")
        elif x1 in range (426, 640):
            print("object on center right")

        if fused["distance"] < 1000:
            led.on()
            time.sleep(0.25) #turns on the led for a time based on distance
            led.off()
            time.sleep(fused["distance"]/100) #turns off the led for a time based on distance
        else:
            led.off()
                
        
        
        
    except KeyboardInterrupt:
        print("error")
        break
    time.sleep(0.05)

picam2.stop()
cv2.destroyAllWindows()