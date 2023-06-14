import cv2
import numpy as np


vid = cv2.VideoCapture("C:/Users/simon/Desktop/testing/videoProvaLancio2.mp4")

if vid.isOpened() == False:
    print("ERRoR")

object_detector = cv2.createBackgroundSubtractorMOG2()
while True:
    ret, frame = vid.read()
    posx = 0
    posy = 0
    
    frame_resized = cv2.resize(frame,(0,0), fx=0.2, fy= 0.2)
    #b, g, r = cv2.split(frame_resized)
    h = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))#printo la altezza del frame
    w = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))

    ''''

    for i in range(w):
        for j in range(h):

            #rgba(153,118,18,255)
            
            if(60 <= r <= 250 and 80 <= g <= 250 and 0 <= b <= 60):
                print(r, g, b)
                frame_resized[w, h]  = (0,0,255)

        '''
    hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        
        # Threshold of blue in HSV space
    lower_blue = np.array([0, 100, 30])
    upper_blue = np.array([255, 255, 60])
        # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(frame_resized, frame_resized, mask = mask)
      #  cv2.imshow('frame', frame)
      #  cv2.imshow('mask', mask)
    #result = cv2.resize(result, (0,0), fx= 0.5, fy=0.5)

    #frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    (thresh, frame_bw) = cv2.threshold(result, 50, 255, cv2.THRESH_BINARY)
    frame_bw = object_detector.apply(result)
    conturns, _ =  cv2.findContours(frame_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in conturns:

        area = cv2.contourArea(cnt) #calcoli l'area

        if  area > 2:
            cv2.drawContours(result, [cnt], -1, (255, 0, 0), 2)

   



    cv2.imshow('Frame', result)
    key = cv2.waitKey(1) #()tempo in secondi -> aspetto ogni tot secondi che un tasto sia premuto       
    if key == ord("q"): #metodo per cambiare il q a un carattere unicode
        break
     
# When everything done, release the video capture object
vid.release()
 
# Closes all the frames
cv2.destroyAllWindows()














