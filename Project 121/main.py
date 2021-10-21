from cv2 import cv2
import time
import numpy as np
#to save output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))

#code to start webcam
cap = cv2.VideoCapture(0)

#Allowing webcam to start by making code sleep for 2seconds
time.sleep(2)
bg = 0

#Capturing bg for 60 frames
for i in range(60):
    ret,bg = cap.read()
#Flipping background img since captured image's inverted
bg = np.flip(bg,axis=1)

#Reading the capture frame until the camera is open
while(cap.isOpened()):
    ret,img = cap.read()
    if not ret:
        break
    #flipping image for consistency
    img = np.flip(img,axis=1)

    #Converting color from BGR/RGB to HSV
    #hueSaturationValue
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #Generating mask to detect red
    #These values can also be changed as per color
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask_1 = cv2.inRange(hsv,lower_red,upper_red)
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask_2 = cv2.inRange(hsv,lower_red,upper_red)
    mask_1 = mask_1+mask_2
    #Open and expand image where there is mask1
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    mask_2 = cv2.bitwise_not(mask_1)
    res_1 = cv2.bitwise_and(img,img,mask=mask_2)
    res_2 = cv2.bitwise_and(bg,bg,mask=mask_1)
    final_output = cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(final_output)
    cv2.imshow('magic',final_output)
    cv2.waitKey(1)
cap.release()
output_file.release()
cv2.destroyAllWindows()