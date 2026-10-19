from picamera2 import Picamera2, Preview, Transform
import time
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
###


###
picam2 = Picamera2()
mode = picam2.sensor_modes[0]
camera_config = picam2.create_video_configuration(sensor={'output_size': mode['size'], 'bit_depth': mode['bit_depth']}) #det if false or true needed, if true: lets you capture faster as it processes quicler with queued frames#creates 6 buffers
picam2.configure(camera_config)
#allows you to adjust the camera settings
picam2.start_preview(
    Preview.QTGL, 
    x=100, 
    y=200, 
    width=800, 
    height=600, 
    transform=Transform(hflip=1))

def capture_and_process():
    picam2.start()
    time.sleep(2) #allow the camera to warm up
    while True:
        metadata = picam2.capture_metadata()
        print(f"Captured frame at {metadata['timestamp']}")
        results = model.predict(metadata)
        image = results[0].plot()
        cv2.imshow('YOLOv8 Detection', image)

        if cv2.waitKey(1) == ord('q'):
            break
    picam2.stop_preview()
    picam2.stop()
    cv2.destroyAllWindows()

#picam2.capture_file("test.jpg") capture a picture
#picam2.start_and_record_video("test.mp", duration=5) take a finite video

'''
tracking and synchronization are wo independent problems





'''

'''
1. capture 
    a. frames from camera
    b. depth from sensor
2. timestamp
    a. when frame recived, when did this happen? 
3. buffer
    a. store frames and depth data in a buffer, so that we can process them later, and match them with the correct timestamp
4. match
    a. match the closest sensor frame to the camera frame 
5. display


Picamera2 captures frame
        ↓
timestamp frame
        ↓
YOLO detects objects
        ↓
tracker associates detections across frames
        ↓
persistent IDs
        ↓
match with ToF frame
'''