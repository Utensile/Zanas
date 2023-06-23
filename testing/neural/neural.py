import cv2
import matplotlib.pyplot as plt
import numpy as np

 
img = cv2.imread('prova3.jpg')


def scalaImmagine():

     
    global img
    print('Original Dimensions : ',img.shape)
    scale_percent = 20 # percent of original size
    width = 280
    height = 280
    dim = (width, height)
      
    # resize image
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
     

def init_neur():

    neurons = []
    cols = 3
    rows = 3


    for r in range(rows):
        neurons.append([0]*cols)


    #print("nuron",neurons)

def convertImage():
    global img
    result = img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Threshold of blue in HSV space

    lower_black = np.array([0,0,0])
    high_black = np.array([70,70,70])
    lower_maincolor = np.array([130, 20, 0])
    upper_maincolor  = np.array([255, 255, 70])
        # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_maincolor, upper_maincolor)
    mask2 = cv2.inRange(hsv, lower_black, high_black)
    
        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-blue regions

      #  cv2.imshow('frame', frame)
      #  cv2.imshow('mask', mask)
    #result = cv2.resize(result, (0,0), fx= 0.5, fy=0.5)
    result[mask != 0] = (0, 0, 0)

    
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Result", result)
    #frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    (thresh, img_m) = cv2.threshold(result, 10, 255, cv2.THRESH_BINARY_INV)
    return img_m

def contorni(img_m):
    global img
    #img_c = cv2.Canny(img_m, 50,200)
    cv2.imshow("canny", img_m)
    contours, hierarchy = cv2.findContours(img_m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
    items = sorted(contours, key=cv2.contourArea, reverse= False) #sorting degli elementi


    item = items[-1]
    print(cv2.contourArea(item))
    x,y,w,h= cv2.boundingRect(item)
    cX = int((x+(x+w))/2)
    cY = int((y+(y+h))/2)

    #cv2.drawContours(img, item, -1, (0, 255, 0), 3)
    
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    
    cv2.circle(img, (cX, cY), 5, (255, 255, 0), -1)
    cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0, 255), 2)
    

    cv2.imshow("Resized image", img)
    cv2.waitKey(0)

    plt.imshow(img)
    plt.show()
    cv2.destroyAllWindows()


    


def get_center():
    
    contorni(convertImage())



def main():
    scalaImmagine()
    init_neur()
    get_center()

    
    

main()
