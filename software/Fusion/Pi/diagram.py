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

entire1 = time.time()


ledl = LED(5)
ledr = LED(4)

#creation of buffers and the fused dictionary to store the matched rgb and sensor frames
camera_buffer_dict = {}
camera_buffer = []
camera_buffer = deque(maxlen=3)
distance_latest = None
fused = {"timestamp_c": 0, "timestamp_s": 0,  "object": 0, "distance": 0}
compare = []
compare = deque(maxlen=3)
correct_index = 0
frame_boundbox = []
last_ten_box = []

#sensor setup
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l1x.VL53L1X(i2c)
sensor.timing_budget = 50

# need to use picamera2 instead of cv2.VideoCapture(0) since raspi only supports picamera2 for libcamera camera access
picam2 = Picamera2() 
model = YOLO('yolov8n.pt')


#configure the picam2 settings to be the correct format of 640x480 and RGB888 for the yolo model to work properly
config1 = time.time()
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
)
config2 = time.time()
config = config2-config1
print(f"CONFIG TIME IS: {config}")

def sensor_reading(sensor):
    sensor1 = time.time()
    sensor.start_ranging()
    distance = sensor.distance #LiDAR frame/distance
    timestamp_s = time.monotonic_ns() #obtain the timestamp
    #distance = starting() #Don't know if this is necessary
    sensor2 = time.time()
    sensor_time = sensor2-sensor1
    print(f"SENSOR TIME IS: {sensor_time}")
    return distance, timestamp_s

def cam_reading(picam2):
    cam1 = time.time()
    picam2.start()
    time.sleep(2)
    frame = picam2.capture_array()
    timestamp_c = time.monotonic_ns() #timestamp for the camera frame
    cam2 = time.time()
    cam_time = cam2-cam1
    print(f"CAMERA TIME IS: {cam_time}")
    return frame, timestamp_c

def timestamp_compare(timestamp_c, timestamp_s, compare, camera_buffer_dict, distance_latest):
    compare1 = time.time()
    for timestamp_c in camera_buffer_dict.keys():
        if timestamp_c is not None:
            difference = abs(timestamp_c-timestamp_s) #finds the closest camrea frame timestamp to the closest sensor reading
            compare.append((difference, timestamp_c)) #stores the difference and the respective camera frame timestamp in a list
            #get minimum difference and its index, then retrieve timestamp
            print(compare)
            for i in compare:
                if i[0] is not None:
                    if i[0] < 10000000000:
                        minimum_difference = i[0]
            correct_timestamp_index = compare.index(minimum_difference) #finds the minimum difference between the camera frame timestamp and the sensor reading timestamp
            print(correct_timestamp_index)
            correct_timestamp = compare[correct_timestamp_index][1] #retrieves the camera frame timestamp corresponding to the minimum difference
            print(correct_timestamp)
            correct_frame = camera_buffer_dict[correct_timestamp] #finds the respective frame to the correct timestamp
            print(correct_frame)
    compare2 = time.time()
    compare_time = compare2-compare1
    print(f"COMPARE TIME IS: {compare_time}")

    return correct_timestamp, timestamp_s, correct_frame, distance_latest


def dictionary_update(correct_timestamp, timestamp_s, correct_frame, distance_latest):
    diction1 = time.time()
    fused.update({"timestamp_c": correct_timestamp, "timestamp_s": timestamp_s, "object": correct_frame, "distance": distance_latest}) #update the fused dictionary with the correct value
    diction2 = time.time()
    diction_time = diction2-diction1
    print(f"DICTIONARY TIME IS: {diction_time}")

def distance_check(distance_latest):
    dist_check1 = time.time()
    if distance_latest < 1000:
        dist_check2 = time.time()
        dist_check_time = dist_check2-dist_check1
        print(f"DISTANCE CHECK TIME IS: {dist_check_time}")
        return True
    else:
        dist_check2 = time.time()
        dist_check_time = dist_check2-dist_check1
        print(f"DISTANCE CHECK TIME IS: {dist_check_time}")
        return False

def object_detected(correct_frame):
    obj_detect1 = time.time()
    if correct_frame is not None:
        obj_detect2 = time.time()
        obj_detect_time = obj_detect2-obj_detect1
        print(f"OBJECT DETECT TIME IS: {obj_detect_time}")
        return True
    else:
        obj_detect2 = time.time()
        obj_detect_time = obj_detect2-obj_detect1
        print(f"OBJECT DETECT TIME IS: {obj_detect_time}")
        return False

def object_localization(correct_frame):
    #position function
    pos1 = time.time()
    for results in camera_buffer_dict.values():#iterates througuh the correct camera frame
        for result in results:
            if len(result.boxes) > 0:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    fused["object"] = class_name  #gets object
                    x1, y1, x2, y2= box.xyxy[0]
                    
                    x1 = x1.item()
                    x2 = x2.item()
                    y1 = y1.item()
                    y2 = y2.item()
                    
                    #max area function              
                    last_ten_box.append((x1,y1,x2,y2))   
                    area = (x2-x1)*(y2-y1)

                    areas.append(area)
                    max_area = max(areas)
                    
                    max_area_index = areas.index(max_area)

                    x_1 = last_ten_box[max_area_index][0]
                    y_1 = last_ten_box[max_area_index][1]
                    x_2 = last_ten_box[max_area_index][2]
                    y_2 = last_ten_box[max_area_index][3]
                    
                    cx = x_1+(x_2-x_1)/2  

                    pos2 = time.time()
                    pos = pos2-pos1
                    print(f"POSITION TIME IS: {pos}")
                    return cx
                    
            else:
                print("no box detected")     

def led_buzzer_control(cx, distance, ledr, ledl):
    buzz1 = time.time()
    x = cx/640   #the position of object is a fraction from 0 to 1, 0 is left#turns on the led for a time based on distance
    if (cx>0 and cx<213) and distance < 1000:
        ledr.off()
        ledl.blink(on_time=0.25, off_time=(distance*x)/100)
    elif (cx>=213 and cx<426) and distance < 1000:
        ledr.blink(on_time=0.25, off_time=(distance*x)/100)
        ledl.blink(on_time=0.25, off_time=(distance*(1-x))/100)
    elif (cx>=426 and cx<640) and distance < 1000:
        ledl.off()
        ledr.blink(on_time=0.25, off_time=(distance/100*x))
    else:
        ledr.off()
        ledl.off()

    buzz2 = time.time()
    buzz = buzz2-buzz1
    print(f"BUZZ TIME IS: {buzz}")

while True:
    loop1 = time.time()
    #capture rgb and sensor reading
    distance_latest, timestamp_s = sensor_reading(sensor)

    print("starting cam reading")
    frame, timestamp_c = cam_reading(picam2)
    print(f"{type(timestamp_c)} timestamp_c")
    print("finished cam reading")

    #plotting results from cam frame to yolo model and displaying it on the screen
    results = model.track(frame)
    image = results[0].plot()
    cv2.imshow('YOLOv8 Detection', image)

    #setting up area list that clears each time while loop iterates (or for every new frame)
    areas = []
    areas = deque(maxlen=10)

    #setting up the last three camera frames to be stored in list and dictionary for frame timestamp comparison
    cam_buffer1 = time.time()
    camera_buffer.append((timestamp_c, results)) #add the results in each corresponding key
    last_three_c = list(camera_buffer)[-3:]  #obtain values/items of dictionary and store in a list
    if len(last_three_c) == 1:
        camera_buffer_dict.update({last_three_c[0][0]: last_three_c[0][1]}) #update the dictionary with the latest camera frames as timestamp: results
    elif len(last_three_c) == 2:
        camera_buffer_dict.update({last_three_c[0][0]: last_three_c[0][1], last_three_c[1][0]: last_three_c[1][1]}) #update the dictionary with the latest camera frames as timestamp: results    
    elif len(last_three_c) == 3:
        camera_buffer_dict.update({last_three_c[0][0]: last_three_c[0][1], last_three_c[1][0]: last_three_c[1][1], last_three_c[2][0]: last_three_c[2][1]}) #update the dictionary with the latest camera frames as timestamp: results
    cam_buffer2 = time.time()   
    cam_buffer_time = cam_buffer2-cam_buffer1
    print(f"CAMERA BUFFER TIME IS: {cam_buffer_time}")

    correct_timestamp, timestamp_s, correct_frame, distance_latest = timestamp_compare(timestamp_c, timestamp_s, compare, camera_buffer_dict, distance_latest) #compare declared in beginning of the code
    dictionary_update(correct_timestamp, timestamp_s, correct_frame, distance_latest) #update the fused dictionary with the correct values

    if distance_check(distance_latest) is True:
        if object_detected(correct_frame) is True:
            # return position index from object localization
            cx = object_localization(correct_frame)
            led_buzzer_control(cx, distance_latest, ledr, ledl)
        else:
            #both buzzers output buzzzing frequency relative to distance
            ledr.blink(ontime=0.1, off_time=distance_latest/1000)
            ledl.blink(ontime=0.1, off_time=distance_latest/1000)
    else:
        ledr.off()
        ledl.off()

    loop2 = time.time()
    loops = loop2-loop1

    entire2 = time.time()
    entire = entire2-entire1

    print(f"LOOP TIME IS: {loops}")
    print(f"ENTIRE TIME IS: {entire}")
    if cv2.waitKey(1) == ord('q'):
        print("error")
        break
    time.sleep(0.05)


picam2.stop()
cv2.destroyAllWindows()
