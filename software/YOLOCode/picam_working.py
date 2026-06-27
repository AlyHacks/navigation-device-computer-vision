from ultralytics import YOLO
import cv2
from picamera2 import Picamera2

#need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
picam2.start()

#still using yolo code
model = YOLO('yolov8n.pt')

while True:
    try:
        frame = picam2.capture_array()
        results = model.predict(frame)
        image = results[0].plot()
        cv2.imshow('YOLOv8 Detection', image)

        if cv2.waitKey(1) == ord('q'):
            break
    except KeyboardInterrupt:
        print("Exiting...")
        break   
cv2.destroyAllWindows()