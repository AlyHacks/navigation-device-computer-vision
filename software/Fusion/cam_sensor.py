from ultralytics import YOLO
import cv2

#loading a pretrained model
model = YOLO('yolov8n.pt')

#running inference on a video or source
results = model.track(source=1, show=True, tracker='bytetrack.yaml') #source can be a video image, or webcam feed, show is to display the results, and tracker is the tracking algorithm to use
cap = cv2.VideoCapture(1) #creating vid capture object named cap

yolo_timestamps = {} #empty dictionary to store timestamps and object info

while True:
    ret, frame = cap.read()
    if not ret:
        break #same as the object.py
    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)/1000 #gets the timestamp of frame
    results = model(frame)
    image = results[0].plot()
    cv2.imshow('YOLOv8 Detection', image)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            #conf = box.conf[0] #ASK WHAT THIS DOES
            ids = int(box.cls[0])
            name = model.names[ids]
            yolo_timestamps[timestamp] = (x1, y1, x2, y2, name, ids)
            if name not in yolo_timestamps:
                yolo_timestamps[name] = [] #WHAT DOES EMPTY LIST DO 
            yolo_timestamps[name].append((timestamp, (x1, y1, x2, y2)))
for obj, times in yolo_timestamps.items():
    print(f"Object:+ {obj}, Timestamps: {times}")

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

###

