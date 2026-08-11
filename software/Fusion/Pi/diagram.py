import time
from ultralytics import YOLO
import cv2
import board
from picamera2 import Picamera2
import busio
import adafruit_vl53l1x
import numpy as np
from gpiozero import LED
from collections import deque

ledl = LED(5)
ledr = LED(4)

#creation of buffers and the fused dictionary to store the matched rgb and sensor frames
camera_buffer = []
camera_buffer = deque(maxlen=20)
distance_latest = None
fused = {"timestamp_c": 0, "timestamp_s": 0,  "object": 0, "distance": 0}
compare = []
compare = deque(maxlen=3)
correct_index = 0
frame_boundbox = []

#sensor setup
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l1x.VL53L1X(i2c)
sensor.timing_budget = 50

# need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
model = YOLO('yolov8n.pt')


#configure the picam2 settings to be the correct format of 640x480 and RGB888 for the yolo model to work properly
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
)

def sensor_reading(sensor):
    sensor.start_ranging()
    distance = sensor.distance #LiDAR frame/distance
    timestamp_s = time.monotonic_ns() #obtain the timestamp
    #distance = starting() #Don't know if this is necessary
    return distance, timestamp_s

def cam_reading(picam2):
    frame = picam2.capture_array()
    timestamp_c = time.monotonic_ns() #timestamp for the camera frame
    return frame, timestamp_c

def timestamp_compare(timestamp_c, timestamp_s, compare):
    for timestamp_c in last_three_c:
        difference = abs(timestamp_c-timestamp_s) #finds the closest camrea frame timestamp to the closest sensor reading
        compare.append(difference)
        correct_index = compare.index(min(compare))
        

while True:
    distance_latest, timestamp_s = sensor_reading(sensor)
    frame, timestamp_c = cam_reading(picam2)

    #plotting results from cam frame to yolo model and displaying it on the screen
    results = model.track(frame)
    image = results[0].plot()
    cv2.imshow('YOLOv8 Detection', image)

    camera_buffer.append((timestamp_c, frame, results))
    last_three_c = list(camera_buffer)[-3:]  # Get the last three camera frames

    timestamp_compare(timestamp_c, timestamp_s, compare)


