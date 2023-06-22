#import tensorflow as tf
import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
#from PIL import Image
import matplotlib.pyplot as plt
import cv2 as cv2
#from rembg import remove

def bgremove2(myimage):
    # First Convert to Grayscale
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
 
    ret,baseline = cv2.threshold(myimage_grey,127,255,cv2.THRESH_TRUNC)
 
    ret,background = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY)
 
    ret,foreground = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY_INV)
 
    foreground = cv2.bitwise_and(myimage,myimage, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
 
    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
 
    # Combine the background and foreground to obtain our final image
    finalimage = background+foreground
    return finalimage

def bgremove1(myimage):
 
    # Blur to image to reduce noise
    myimage = cv2.GaussianBlur(myimage,(5,5), 0)
 
    # We bin the pixels. Result will be a value 1..5
    bins=np.array([0,51,102,153,204,255])
    myimage[:,:,:] = np.digitize(myimage[:,:,:],bins,right=True)*51
 
    # Create single channel greyscale for thresholding
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
 
    # Perform Otsu thresholding and extract the background.
    # We use Binary Threshold as we want to create an all white background
    ret,background = cv2.threshold(myimage_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
 
    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
 
    # Perform Otsu thresholding and extract the foreground.
    # We use TOZERO_INV as we want to keep some details of the foregorund
    ret,foreground = cv2.threshold(myimage_grey,0,255,cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)  #Currently foreground is only a mask
    foreground = cv2.bitwise_and(myimage,myimage, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
 
    # Combine the background and foreground to obtain our final image
    finalimage = background+foreground
 
    return finalimage

def bgremove3(myimage):
    # BG Remover 3
    myimage_hsv = cv2.cvtColor(myimage, cv2.COLOR_BGR2HSV)
     
    #Take S and remove any value that is less than half
    s = myimage_hsv[:,:,1]
    s = np.where(s < 127, 0, 1) # Any value below 127 will be excluded
 
    # We increase the brightness of the image and then mod by 255
    v = (myimage_hsv[:,:,2] + 127) % 255
    v = np.where(v > 127, 1, 0)  # Any value above 127 will be part of our mask
 
    # Combine our two masks based on S and V into a single "Foreground"
    foreground = np.where(s+v > 0, 1, 0).astype(np.uint8)  #Casting back into 8bit integer
 
    background = np.where(foreground==0,255,0).astype(np.uint8) # Invert foreground to get background in uint8
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)  # Convert background back into BGR space
    foreground=cv2.bitwise_and(myimage,myimage,mask=foreground) # Apply our foreground map to original image
    finalimage = background+foreground # Combine foreground and background
 
    return finalimage


def gaussian_filter(myImg):

    return finalImage

def sobel_filter(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #filtro di Sobel
    img_sobel_x=cv2.Sobel(img_gray,-1,1,0) #x-derivative set to 1, y-derivative set to 0
    img_sobel_y=cv2.Sobel(img_gray,-1,0,1) #x-derivative set to 0, y-derivative set to 1
    print (img_sobel_x.shape)
    print (img_sobel_y.shape)
    return img_sobel_x
    cv2.waitKey(0)

def canny(img):
    img_canny = cv2.Canny(img, 250, 255)
    return img_canny

def get_important_with_FAST(img):
    fast = cv2.FastFeatureDetector_create()
    # find and draw the keypoints
    kp = fast.detect(img,None)
    img2 = cv2.drawKeypoints(img, kp, None, color=(255,0,0))

    # Disable nonmaxSuppression
    fast.setNonmaxSuppression(0)
    kp = fast.detect(img,None)
    print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
    img3 = cv2.drawKeypoints(img, kp, None, color=(255,0,0))

    cv2.imshow("penguin_FAST1", img2)
    cv2.imshow("penguin_FAST2", img3)
    cv2.waitKey(0)
    return img3

def get_important_with_ORB(img):
    # Initiate ORB detector
    orb = cv2.ORB_create()
    # find the keypoints with ORB
    kp = orb.detect(img,None)
    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)
    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img, kp, None, color=(0,0,0), flags=0)
    cv2.imshow("penguin_ORB", img2)
    cv2.waitKey(0)

    return img2

def contorni(img_canny, starting_img, areaMin):
    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
    cv2.imshow('Canny Edges After Contouring', img_canny)
    cv2.waitKey(0)
      
    print("Number of Contours found = " + str(len(contours)))
      
    # Draw all contours
    # -1 signifies drawing all contours
    #cv2.drawContours(starting_img, contours, -1, (0, 255, 0), 3)
      
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print (area)
        if area > areaMin:
            cv2.drawContours(starting_img, [cnt], -1, (255, 0, 0), 2)
    cv2.imshow('Contours', starting_img)
    return img

img = cv2.imread("images.jpg")
#plt.imshow(img, cmap='gray');

#bg remover




outpu = canny(img)
#output = get_important_with_FAST(outpu)
#sfdj = get_important_with_ORB(outpu)
fdslfa = contorni(outpu, img, 30)
'''
gray= cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)

edges= cv2.Canny(gray, 50,200)


contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)
'''
#plt.imshow(edges, cmap='gray');
cv2.imwrite("FAST_nonmaxSuppression+canny.jpg", output)
print('Successfully saved')

