import cv2

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read() #returns the frame/array of frame, and ret tells u if it worked


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

    ret, frame = cap.read()
    height, width, channels = frame.shape
    print(f"Width: {width}, Height: {height}")


cap.release()
cv2.destroyAllWindows()
