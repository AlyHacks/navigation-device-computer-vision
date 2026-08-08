from time import time

from ultralytics import YOLO
import cv2
from picamera2 import Picamera2

#need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480)}, format="RGB888"
    )
)


picam2.start()
time.sleep(2)  # Allow the camera to warm up


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

picam2.stop()
cv2.destroyAllWindows()


