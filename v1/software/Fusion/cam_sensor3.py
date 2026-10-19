from ultralytics import YOLO
import cv2
from picamera2 import Picamera2

import board
import busio
import adafruit_vl53l1x
import time



#for the sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l1x.VL53L1X(i2c)

#still using yolo code#
# need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
model = YOLO('yolov8n.pt')
picam2.start()

#for the sensor, to start ranging 
def start_ranging():
    sensor.start_ranging(1)
    distance = sensor.distance
    print(f"Distance: {distance} mm")

while True:
    try:
        frame = picam2.capture_array()
        results = model.predict(frame)
        image = results[0].plot()
        cv2.imshow('YOLOv8 Detection', image)

        print(start_ranging())
        sensor.clear_interrupt()


        if cv2.waitKey(1) == ord('q'):
            break
    except KeyboardInterrupt:
        print("Exiting...")
        break   
    time.sleep(0.05)
cv2.destroyAllWindows()
