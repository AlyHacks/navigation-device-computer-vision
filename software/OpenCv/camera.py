import numpy as np
import cv2


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() #returns the frame/array of frame, and ret tells u if it worked

    width = int(cap.get(3)) #width of frame
    height = int(cap.get(4))

    image = np.zeros(frame.shape, np.uint8) #making a blank canvas using all 0 array of the same shape as the frame
    smaller_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
   
    image[:height//2, :width//2] = smaller_frame
    image[:height//2:, width//2:] = smaller_frame #colon before is top for height, left for width, and after is bottom for height, and right for width
    image[height//2:, :width//2] = smaller_frame
    image[height//2:, width//2:] = smaller_frame


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
