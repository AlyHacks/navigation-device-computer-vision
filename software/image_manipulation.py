import random
import cv2


img = cv2.imread("images/tre0.0125glu0.5 wings 12-01-2024.png", 0)

#print(img.shape()) #this returns a numpy array, with the shape describing rows,columns,channels=height,width,how many pixels are represting each pixel

'''
BGR
0-255
'''
print(img[0]) #shows me the first row of our array image

for i in range (100):
    for j in range(img.shape[1]):
        img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()