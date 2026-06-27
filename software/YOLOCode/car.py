from time import time
from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
from gpiozero import LED

led = LED(4) #GPIO pin 4


#need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480), "format" : "RGB888"}
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

        

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                x1, y1, x2, y2 = box.xyxy[0]

                if cls == 2:  # Assuming class 2 is the car class
                    width = x2 - x1
                    height = y2 - y1
                    area = width * height
                    if area > 1000:  # Adjust this threshold as needed
                        led.on()  # Turn on the LED
                    elif 500 < area <= 10000:  # Adjust this threshold as needed
                        led.blink(on_time=0.5, off_time=0.5)  # Blink the LED
                else:
                    led.off()  # Turn off the LED

        if cv2.waitKey(1) == ord('q'):
            break
    except KeyboardInterrupt:
        print("Exiting...")
        break   

picam2.stop()
cv2.destroyAllWindows()


