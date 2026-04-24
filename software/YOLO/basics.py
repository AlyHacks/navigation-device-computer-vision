from ultralytics import YOLO
import cv2

#loading a pretrained model
model = YOLO('yolov8n.pt')

#running inference on a video or source
results = model.track(source=0, show=True, tracker='bytetrack.yaml') #source can be a video (0 is the default camera), image, or webcam feed, show is to display the results, and tracker is the tracking algorithm to use

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model.predict(frame)
    image = results[0].plot()
    cv2.imshow('YOLOv8 Detection', image)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()