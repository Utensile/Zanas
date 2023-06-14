import cv2
import numpy as np
  
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("C:/Users/simon/Desktop/testing/videoProvaLancio2.mp4")
while(1):
    ret, frame = cap.read()
    # It converts the BGR color space of image to HSV color space
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Threshold of blue in HSV space
        lower_blue = np.array([0, 100, 30])
        upper_blue = np.array([255, 255, 255])
        # preparing the mask to overlay
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-blue regions
        result = cv2.bitwise_and(frame, frame, mask = mask)
      #  cv2.imshow('frame', frame)
      #  cv2.imshow('mask', mask)
        result = cv2.resize(result, (0,0), fx= 0.5, fy=0.5)
        cv2.imshow('result', result)
        
        key = cv2.waitKey(1)

    
    if key == ord("c"): #metodo per cambiare il q a un carattere unicode
          break

  
cv2.destroyAllWindows()
cap.release()