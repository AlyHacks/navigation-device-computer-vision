import cv2
import numpy as np
#detect regions of interest
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read() 
ret, frame2 = cap.read() #ret is a bool t/f if grabbed frame, frame is actual video of pixel
if not ret:
    print("failed to grab frame") 

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2) #finds difference, or movement between different frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) #converting frame into grayscale
    blur = cv2.GaussianBlur(gray, (5,5), 0) #reducing te noise of the image, passing in the frame, size sigmay, and lastly sigma x
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) #threshold of pixels, min, max, all other pixels not within range are set to 0
    dilated = cv2.dilate(thresh, None, iterations=3) #dilation is the process of increasing the white region in the image or size of foreground object, and is used to accentuate features
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #find contours of the dilated image, and returns a list of contours and hierarchy, RETR_TREE is the contour retrieval mode, and CHAIN_APPROX_SIMPLE is the contour approximation method
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour) #finds the bounding rectangle of the contour, and returns the x and y coordinates of the top left corner, and the width and height of the rectangle    

        if cv2.contourArea(contour) < 600:
            continue
        #get the maximum amount of contour or area and define its position, or get the center of the largest area
        #if its in a certain space on the frame, then return a message saying it is on left, right etc
        for c in contours:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.drawContours(frame1, [c], -1, (0, 255, 0), 2)
            cv2.circle(frame1, (cX, cY), 7, (255, 255, 255), -1)    
        
            if cX in range (0, 320):
                print("object on left")
            elif cX in range (320, 640):
                print("object on center left")
            elif cX in range (640, 960):
                print("object on center right")
            elif cX in range (960, 1280):
                print("object on right")

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)

    cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    cv2.imshow("video", frame1)
    frame1 = frame2
    ret, frame2 = cap.read() #read the new frame in var frame2, and set vlaue as frame1 

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()

cv2.destroyAllWindows()
