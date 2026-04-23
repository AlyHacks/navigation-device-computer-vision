import cv2

img = cv2.imread('images/tre0.0125glu0.5 wings 12-01-2024.png', -1)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5) #this shrinks the size of the image to be 1/2 of the size
img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite("new_img.jpg", img) #creates a new file of the same image with all of the actions we put on it
'''
-1,cv2.IMREAD_COLOR: loads color image
0,cv2.IMREAD_GRAYSCALE: in grayscale mode
1, cv2.IMREAD_UNCHANGED: image as such including alpha channel
'''
cv2.imshow("Image", img)
cv2.waitKey(0) #waits an infinite amt time 0 until key presesd
cv2.destroyAllWindows() #when pressed destroy 