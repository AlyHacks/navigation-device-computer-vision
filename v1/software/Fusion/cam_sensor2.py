from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
import datetime
from async_frame_reader.video_async import read_frame  

#need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
picam2.start()

#still using yolo code
model = YOLO('yolov8n.pt')

yolo_timestamps = {}

while True:
    try:
        frame = picam2.capture_array()
        results = model.predict(frame)
        image = results[0].plot()
        cv2.imshow('YOLOv8 Detection', image)

        font = cv2.FONT_HERSHEY_SIMPLEX
        dt = str(datetime.datetime.now())
        #setting the text on the image frame
        frame = cv2.putText(frame, dt, 
                            (10, 100),
                            font, 1, 
                            (210, 155, 155),
                            4, cv2.LINE_8)

        cv2.imshow("", frame)


        if cv2.waitKey(1) == ord('q'):
            break
    except KeyboardInterrupt:
        print("Exiting...")
        break   
cv2.destroyAllWindows()