import time
from ultralytics import YOLO
import cv2
import board
from picamera2 import Picamera2
import busio
import adafruit_vl53l1x
import numpy as np
from gpiozero import LED

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
def sensor_reading(sensor):
    sensor.start_ranging()
    distance = sensor.distance
    timestamp_s = time.monotonic_ns()
    #distance = starting() #Don't know if this is necessary
    return distance

def cam_reading(picam2):
    frame = picam2.capture_array()
    timestamp_c = time.monotonic_ns()
    return frame, timestamp_c
    return timestamp_c       





